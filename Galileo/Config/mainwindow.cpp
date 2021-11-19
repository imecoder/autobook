#include "mainwindow.h"
#include "ui_mainwindow.h"



MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , currentRow(-1)
{
    ui->setupUi(this);

    connect( ui->tableWidgetBookList,SIGNAL(cellClicked(int,int)),
             this,SLOT(on_tableWidgetBookList_clicked(int,int)));

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::readBase() {
    QFile file("config.base.json");
    if( !file.open(QIODevice::ReadOnly)) {
        QMessageBox::information(NULL, "config.base.json", "打开文件失败!", QMessageBox::Yes);
        close();
    }

    QString data = file.readAll();
    file.close();

    QJsonParseError parseJsonErr;
    QJsonDocument document = QJsonDocument::fromJson(data.toUtf8(), &parseJsonErr);
    if( parseJsonErr.error != QJsonParseError::NoError) {
        QMessageBox::information(NULL, "config.base.json", "解析json失败!", QMessageBox::Yes);
        close();
    }

    jsonBaseConfig = document.object();

    fillBaseConfig();
}

void MainWindow::writeBase() {
    QFile file("config.base.json");
    if( !file.open(QIODevice::WriteOnly)) {
        QMessageBox::information(NULL, "config.base.json", "打开文件失败!", QMessageBox::Yes);
        close();
    }


    jsonBaseConfig["mode"] = ui->comboBoxMode->currentIndex();
    if ( ui->comboBoxManual->currentIndex() == 0 )
        jsonBaseConfig["manual"] = false ;
    else jsonBaseConfig["manual"] = true ;
    jsonBaseConfig["branch_size"] = ui->lineEditBranchSize->text().toInt();

    QJsonDocument document ;
    document.setObject(jsonBaseConfig);

    qDebug() <<"jsonBaseConfig = " << jsonBaseConfig;

    file.write(document.toJson());
    file.close();
}

void MainWindow::readBook() {
    QFile file("config.book.json");
    if( !file.open(QIODevice::ReadOnly)) {
        QMessageBox::information(NULL, "config.book.json", "打开文件失败!", QMessageBox::Yes);
        close();
    }

    QString data = file.readAll();
    file.close();

    QJsonParseError parseJsonErr;
    QJsonDocument document = QJsonDocument::fromJson(data.toUtf8(), &parseJsonErr);
    if( parseJsonErr.error != QJsonParseError::NoError) {
        QMessageBox::information(NULL, "config.book.json", "解析json失败!", QMessageBox::Yes);
        close();
    }

    jsonBookConfig = document.array();

    clearTableWidgetBookList();
    fillTableWidgetBookList();
}

void MainWindow::writeBook() {
    QFile file("config.book.json");
    if( !file.open(QIODevice::WriteOnly)) {
        QMessageBox::information(NULL, "config.book.json", "打开文件失败!", QMessageBox::Yes);
        close();
    }


    QJsonDocument document ;
    document.setArray(jsonBookConfig);
    qDebug() <<"jsonBookConfig = " << jsonBookConfig;

    file.write(document.toJson());
    file.close();
}


void MainWindow::fillBaseConfig() {
    ui->comboBoxMode->setCurrentIndex(jsonBaseConfig["mode"].toInt());
    ui->lineEditBranchSize->setText(QString::number(jsonBaseConfig["branch_size"].toInt()));
    if (!jsonBaseConfig["manual"].toBool() )
        ui->comboBoxManual->setCurrentIndex(0);
    else
        ui->comboBoxManual->setCurrentIndex(1);
}


void MainWindow::fillBookConfig() {
    QTableWidgetItem * item = new QTableWidgetItem;
    item = ui->tableWidgetBookList->item(currentRow,0);
    ui->lineEditDate->setText(ui->tableWidgetBookList->item(currentRow,0)->text());
    ui->lineEditFrom->setText(ui->tableWidgetBookList->item(currentRow,1)->text());
    ui->lineEditTo->setText(ui->tableWidgetBookList->item(currentRow,2)->text());
    ui->lineEditComp->setText(ui->tableWidgetBookList->item(currentRow,3)->text());
    ui->lineEditFlight->setText(ui->tableWidgetBookList->item(currentRow,4)->text());
    ui->lineEditSpace->setText(ui->tableWidgetBookList->item(currentRow,5)->text());
    ui->lineEditUser->setText(ui->tableWidgetBookList->item(currentRow,6)->text());
    ui->lineEditContact->setText(ui->tableWidgetBookList->item(currentRow,7)->text());
}


void MainWindow::on_pushButtonRead_clicked()
{
    clearBookConfig();
    readBase();
    readBook();
}


void MainWindow::on_pushButtonSave_clicked()
{

    clearBookConfig();
    writeBase();
    writeBook();
    QMessageBox::information(NULL, "保存完毕", "文件保存成功!", QMessageBox::Yes);
}


void MainWindow::on_pushButtonBookAdd_clicked()
{
    if ( ui->lineEditDate->text().isEmpty()
         || ui->lineEditFrom->text().isEmpty()
         || ui->lineEditTo->text().isEmpty()
         || ui->lineEditComp->text().isEmpty()
         || ui->lineEditFlight->text().isEmpty()
         || ui->lineEditSpace->text().isEmpty()
         || ui->lineEditUser->text().isEmpty()
         || ui->lineEditContact->text().isEmpty()) {
        QMessageBox::information(NULL, "添加失败", "请确认是否存在空的情况!", QMessageBox::Yes);
        return;
    }

    QJsonObject jsonObject;
    jsonObject.insert("date", ui->lineEditDate->text());
    jsonObject.insert("from", ui->lineEditFrom->text());
    jsonObject.insert("to", ui->lineEditTo->text());
    jsonObject.insert("comp", ui->lineEditComp->text());
    jsonObject.insert("flight", ui->lineEditFlight->text());
    jsonObject.insert("space", ui->lineEditSpace->text());
    jsonObject.insert("user", ui->lineEditUser->text());
    jsonObject.insert("contact", ui->lineEditContact->text());

    jsonBookConfig.append(jsonObject);

    clearBookConfig();
    clearTableWidgetBookList();
    fillTableWidgetBookList();
}


void MainWindow::on_pushButtonBookModify_clicked()
{

    if ( ui->lineEditDate->text().isEmpty()
         || ui->lineEditFrom->text().isEmpty()
         || ui->lineEditTo->text().isEmpty()
         || ui->lineEditComp->text().isEmpty()
         || ui->lineEditFlight->text().isEmpty()
         || ui->lineEditSpace->text().isEmpty()
         || ui->lineEditUser->text().isEmpty()
         || ui->lineEditContact->text().isEmpty()) {
        QMessageBox::information(NULL, "修改失败", "请确认是否存在空的情况!", QMessageBox::Yes);
        return;
    }

    qDebug() <<"jsonBookConfig = " << jsonBookConfig;
    jsonBookConfig.removeAt(currentRow);


    QJsonObject jsonObject;
    jsonObject.insert("date", ui->lineEditDate->text());
    jsonObject.insert("from", ui->lineEditFrom->text());
    jsonObject.insert("to", ui->lineEditTo->text());
    jsonObject.insert("comp", ui->lineEditComp->text());
    jsonObject.insert("flight", ui->lineEditFlight->text());
    jsonObject.insert("space", ui->lineEditSpace->text());
    jsonObject.insert("user", ui->lineEditUser->text());
    jsonObject.insert("contact", ui->lineEditContact->text());

    jsonBookConfig.append(jsonObject);

    clearBookConfig();
    clearTableWidgetBookList();
    fillTableWidgetBookList();
}


void MainWindow::on_pushButtonBookDelete_clicked()
{
    clearBookConfig();
    jsonBookConfig.removeAt(currentRow);
    clearTableWidgetBookList();
    fillTableWidgetBookList();
}

void MainWindow::clearBookConfig() {
    ui->lineEditDate->clear();
    ui->lineEditFrom->clear();
    ui->lineEditTo->clear();
    ui->lineEditComp->clear();
    ui->lineEditFlight->clear();
    ui->lineEditSpace->clear();
    ui->lineEditUser->clear();
    ui->lineEditContact->clear();
}

void MainWindow::clearTableWidgetBookList()
{
    for ( int row = 0 ; row < ui->tableWidgetBookList->rowCount(); row++ )
    {
        for ( int colume = 0 ; colume < 8 ; colume++ )
            delete ui->tableWidgetBookList->item(row,colume) ;
        ui->tableWidgetBookList->removeRow(row);
    }

    ui->tableWidgetBookList->setRowCount(0);
    ui->tableWidgetBookList->clear();
    ui->tableWidgetBookList->clearContents();
    ui->tableWidgetBookList->setEditTriggers(QAbstractItemView::NoEditTriggers);
    ui->tableWidgetBookList->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui->tableWidgetBookList->setSelectionMode(QAbstractItemView::SingleSelection);
    ui->tableWidgetBookList->horizontalHeader()->setStretchLastSection(true);
    QStringList header;
    header<< "日期"<<"起始"<<"目的"<<"航司"<<"航班"<<"仓位"<<"用户"<<"联系方式";
    ui->tableWidgetBookList->setHorizontalHeaderLabels(header);
    ui->tableWidgetBookList->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);

    currentRow = -1 ;
}

void  MainWindow::on_tableWidgetBookList_clicked(int row,int column)
{
    currentRow = row;
    fillBookConfig();
}

void MainWindow::fillTableWidgetBookList()
{
    for ( int i = 0 ; i < (int)jsonBookConfig.size() ; i++ ) {
        int row = ui->tableWidgetBookList->rowCount();
        ui->tableWidgetBookList->insertRow(row);
        QJsonValue jsonValue = jsonBookConfig.at(i);
        QJsonObject jsonObject = jsonValue.toObject();
        ui->tableWidgetBookList->setItem(row, 0, new QTableWidgetItem(jsonObject["date"].toString()) );
        ui->tableWidgetBookList->setItem(row, 1, new QTableWidgetItem(jsonObject["from"].toString()) );
        ui->tableWidgetBookList->setItem(row, 2, new QTableWidgetItem(jsonObject["to"].toString()) );
        ui->tableWidgetBookList->setItem(row, 3, new QTableWidgetItem(jsonObject["comp"].toString()) );
        ui->tableWidgetBookList->setItem(row, 4, new QTableWidgetItem(jsonObject["flight"].toString()) );
        ui->tableWidgetBookList->setItem(row, 5, new QTableWidgetItem(jsonObject["space"].toString()) );
        ui->tableWidgetBookList->setItem(row, 6, new QTableWidgetItem(jsonObject["user"].toString()) );
        ui->tableWidgetBookList->setItem(row, 7, new QTableWidgetItem(jsonObject["contact"].toString()) );
    }

    currentRow = -1 ;
}
