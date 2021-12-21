#!/usr/bin/python
from mylimit import *
from myhelp import *

ret, base_config = get_config("config.base.json")
if ret == False:
    exit(0)

ret, book_config_list = get_config("config.book.json")
if ret == False:
    exit(0)



def parse_flight(attrlist, book_comp, book_flight):
    # 查找 book_comp, book_flight
    comp_flight_location = len(attrlist)
    for i in range(len(attrlist)):
        # logger.warning(str(i) + ' ' + attrlist[i]["text"] + attrlist[i+1]["text"])
        if "text" in attrlist[i] \
                and attrlist[i]["text"] == book_comp \
                and "text" in attrlist[i + 1] \
                and attrlist[i + 1]["text"].strip() == book_flight:
            comp_flight_location = i
            break

    if comp_flight_location >= len(attrlist):
        logger.warning('未找到航班 [' + book_comp + book_flight + ']')
        return False, 0, 0

    line = attrlist[comp_flight_location - 8]["text"]
    # logger.warning("comp_flight_location = %d" % comp_flight_location )
    logger.warning('找到航班 [' + book_comp + book_flight + ']，位于行 [' + line + ']')
    return True, line, comp_flight_location


def parse_space_end_location(attrlist, line, comp_flight_location):
    lineplus = str(int(line) + 1)
    lineplus_start_location = comp_flight_location
    for i in range(comp_flight_location, len(attrlist)):
        if "text" in attrlist[i] and attrlist[i]["text"] == lineplus:
            lineplus_start_location = i
            break

    end_location = len(attrlist)
    if lineplus_start_location < len(attrlist):
        # logger.warning("lineplus_start_location = %d" % lineplus_start_location)
        # logger.warning('找到第二个航班')
        end_location = lineplus_start_location - 1

    return end_location


def parse_space(attrlist, book_space_list, line_start_location, line_end_location, book_comp, book_flight):
    space_list = {}

    # 枚举所有的座舱类型
    for book_space in book_space_list:

        space_list[book_space] = {
            "location": -1,
            "status": 'N'
        }

        # 查找座舱所在位置, 以及座舱的状态
        for i in range(line_start_location, line_end_location):

            if "extended" not in attrlist[i]:
                continue

            if "bic" not in attrlist[i]["extended"]:
                continue

            if attrlist[i]["extended"]["bic"] != book_space:
                continue

            space_list[book_space]["location"] = i
            status = attrlist[i]["extended"]["status"]
            space_list[book_space]["status"] = status

            logger.warning('找到航班 [' + book_comp + book_flight + ']的座舱[' + book_space + status + ']')
            break

    return space_list


def space_status_all_N(space_list):
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location != -1 and status != 'N':
            return False

    return True


def space_status_has_C(space_list):
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location != -1 and status == 'C':
            return True

    return False


def callback(session_id, book_config, message):
    # 航班过去，重新回去刷票
    if 'DEPARTED' in message["text"]:
        logger.warning("[任务退出] 请确认是否航班已经过期")
        return

    # 掉线，重新回去登录和刷票
    if 'SYSTEM ERROR' in message["text"] \
            or 'Session does not exist' in message["text"]:
        logger.warning('[任务退出] 掉线重新登录')
        set_run_status(RunStatus.LOGIN)
        return

    attrlist = message["masks"]["special"]["attrList"]

    # 查询匹配的航班，失败重新回去刷票
    ret, line, comp_flight_location = parse_flight(
        attrlist,
        book_config['comp'],
        book_config['flight']
    )
    if ret == False:
        logger.warning('[任务退出] 未找到匹配航班')
        return

    # 航班行的开始位置
    line_start_location = comp_flight_location + 2

    # 查找匹配的航班结束的位置，即text: line + 1 位置
    line_end_location = parse_space_end_location(
        attrlist,
        line,
        comp_flight_location
    )

    # 查找 book_space_list 的位置, 及状态
    space_list = parse_space(
        attrlist,
        book_config["space"],
        line_start_location,
        line_end_location,
        book_config["comp"],
        book_config["flight"]
    )

    # 如果所有仓位状态都是N，重新回去刷票
    if space_status_all_N(space_list) == True:
        logger.warning('[任务退出] 所有仓位都是N的状态')
        return

    # 处理所有的占座及订座

    # 处理有座状态
    flag_has_ticket = False
    for book_space in space_list:
        location = space_list[book_space]["location"]
        status = space_list[book_space]["status"]
        if location == line_end_location or status == 'N':
            continue

        # 当前仓位无票
        if not (status >= "1" and status <= "9"):
            continue

        # 有位置, 立即占票及订票
        flag_has_ticket = True
        logger.warning("航班 [" + book_config["comp"] + book_config["flight"] + "] 有票 : " + attrlist[location]["text"])

        # 占票
        occupy_ticket(session_id, book_space, line)

        # 占票成功，直接回主线程，继续后续订票流程
        if get_run_status() == RunStatus.OCCUPIED:
            logger.warning('[任务退出]')
            return

        # 占票失败，尝试占票下一个仓位

    # 有位置的情况下，但未能占票或订票成功，重新去刷票
    if flag_has_ticket == True:
        logger.warning('[任务退出] 占票失败')
        return

    # 刷票+占票模式，不进行快速预定，重新去刷票
    if base_config["mode"] == 0:
        logger.warning('[任务退出]')
        return

    # 刷票+占票+快速预定模式下，带有C 候补关闭 状态 的票, 执行快速预订
    if space_status_has_C(space_list):
        set_run_status(RunStatus.OVER)
        os.system(r"start /b quick_booking.exe")
        logger.warning('[任务退出] 所有座舱关闭状态，已经启动快速预定程序')
        return

    # 候补状态，L, 0 等等重新刷票

    logger.warning('[任务退出]')



def occupy_ticket(session_id, book_space, line):
    if get_run_status() == RunStatus.OCCUPIED:
        logger.warning("前述执行已占票")
        return

    occupy_cmd = '01' + book_space + line
    ret, message = execute_instruction(session_id, occupy_cmd)
    if ret == False:
        logger.warning('占票失败')
        return

    if 'text' not in message:
        logger.warning('占票失败')
        return

    # 已经了占票的
    if 'UNABLE - DUPLICATE SEGMENT' in message['text']:
        logger.warning('前期占票命令已经执行')
        set_run_status(RunStatus.OCCUPIED)
        return

    # 占票失败，重新回去刷票
    if 'HL' in message["text"] or \
            'LL' in message["text"]:
        logger.warning('占票失败')
        three_i_command(session_id)
        return

    if 'HS' not in message["text"]:
        logger.warning('占票失败')
        return

    # HS
    logger.warning('占票成功')
    set_run_status(RunStatus.OCCUPIED)




def main():
    branch_size = base_config["branch_size"]

    for book_config in book_config_list:

        logger.warning('')
        logger.warning('')
        logger.warning('开始订票 = ' + json.dumps(book_config))

        set_run_status(RunStatus.LOGIN)

        while True:

            session_id, sock = login(base_config['debug'])

            send_thread = SendThread(sock, session_id, base_config['debug'])
            recv_thread = RecvThread(sock, session_id, book_config, callback, base_config['debug'])
            send_thread.start()
            recv_thread.start()
            logger.warning('读写线程已启动')

            set_run_status(RunStatus.QUERY)

            while True:

                if limit() == True:
                    exit(0)

                if get_run_status() == RunStatus.LOGIN:
                    break

                if get_run_status() == RunStatus.QUERY:
                    command = (
                        'A{}{}{}/{}'
                    ).format(
                        book_config['date'],
                        book_config['from'],
                        book_config['to'],
                        book_config['comp'],
                    )

                    send_queue.put(command)

                    time.sleep(1 / branch_size)
                    continue

                if get_run_status() == RunStatus.OCCUPIED:
                    # 后续订票
                    if base_config["manual"] == True:
                        munual_booking(session_id)
                        # 继续下一个用户的订票
                        break

                    if auto_booking(session_id, book_config) == True:
                        # 继续下一个用户的订票
                        break

                    # 自动订票失败，重新刷票
                    set_run_status(RunStatus.QUERY)
                    time.sleep(1 / branch_size)
                    continue

                if get_run_status() == RunStatus.OVER:
                    break

            logger.warning('等待读写线程退出')
            send_thread.join()
            recv_thread.join()

            if get_run_status() == RunStatus.OVER:
                break

    logger.warning("退出主线程")


if __name__ == '__main__':
    main()
