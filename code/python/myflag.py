import threading

# 舱位记录标志
flagSpace = True
mutexSpace = threading.Lock()

def set_flag_space(flag) :
    with mutexSpace :
        global flagSpace
        flagSpace = flag

def get_flag_space() :
    with mutexSpace :
        global flagSpace
        return flagSpace

# 舱位占有标志
flagOccupied = False
mutexOccupied = threading.Lock()

def set_flag_occupied(flag) :
    with mutexOccupied :
        global flagOccupied
        flagOccupied = flag

def get_flag_occupied() :
    with mutexOccupied :
        global flagOccupied
        return flagOccupied

# # 舱票已定标志
# flagBooked = False
# mutexBooked = threading.Lock()
#
# def set_flag_booked(flag) :
#     with mutexBooked :
#         global flagBooked
#         flagBooked = flag
#
# def get_flag_booked() :
#     with mutexBooked :
#         global flagBooked
#         return flagBooked

# 手动输入订票信息标志
# flagManual = False
# mutexManual = threading.Lock()
# def set_flag_manual(flag) :
#     with mutexManual :
#         global flagManual
#         flagManual = flag
#
# def get_flag_manual() :
#     with mutexManual :
#         global flagManual
#         return flagManual
