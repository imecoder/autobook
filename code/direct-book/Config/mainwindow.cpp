#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QtWidgets>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
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
    if( !file.open(QIODevice::ReadWrite)) {
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

    QJsonObject jsonObject = document.object();
    qDebug() << "jsonObject[mode]=" << jsonObject["mode"].toInt();
    qDebug() << "jsonObject[manual]=" << jsonObject["manual"].toBool();
    qDebug() << "jsonObject[branch_size]=" << jsonObject["branch_size"].toInt();

    ui->comboBoxMode->setCurrentIndex(jsonObject["mode"].toInt());
    ui->lineEditBranchSize->setText(QString::number(jsonObject["branch_size"].toInt()));
    if (!jsonObject["manual"].toBool() )
        ui->comboBoxManual->setCurrentIndex(0);
    else
        ui->comboBoxManual->setCurrentIndex(1);

}

void MainWindow::readBook() {
    QFile file("config.book.json");
    if( !file.open(QIODevice::ReadWrite)) {
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

    QJsonObject jsonObject = document.object();
    qDebug() << "jsonObject=" << jsonObject;

    ui->lineEditDate->setText(jsonObject["date"].toString());
    ui->lineEditFrom->setText(jsonObject["from"].toString());
    ui->lineEditTo->setText(jsonObject["to"].toString());
    ui->lineEditComp->setText(jsonObject["comp"].toString());
    ui->lineEditFlight->setText(jsonObject["flight"].toString());
    ui->lineEditSpace->setText(jsonObject["space"].toString());
    ui->lineEditUser->setText(jsonObject["user"].toString());
    ui->lineEditContact->setText(jsonObject["contact"].toString());
}

void MainWindow::on_pushButtonRead_clicked()
{

}


void MainWindow::on_pushButtonSave_clicked()
{

}


void MainWindow::on_pushButtonBookAdd_clicked()
{

}


void MainWindow::on_pushButtonBookModify_clicked()
{

}


void MainWindow::on_pushButtonBookDelete_clicked()
{

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
    header<<QString::fromLocal8Bit("�û���")\
         <<QString::fromLocal8Bit("����")\
        <<QString::fromLocal8Bit("���ι���Ա")\
       <<QString::fromLocal8Bit("�Ʒѷ�ʽ")\
      <<QString::fromLocal8Bit("����");
    ui->tableWidgetBookList->setHorizontalHeaderLabels(header);
    ui->tableWidgetBookList->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
}

void  MainWindow::on_tableWidgetBookList_clicked(int row,int column)
{
    QTableWidgetItem * item = new QTableWidgetItem;
    item = ui->tableWidgetBookList->item(row,0);
    m_pAccountSelected = m_mAccount[item->text().toStdString()] ;

    if ( m_accountLogin.m_sName == "admin" )
    {
        ui->pushButtonAddUser->show();
        ui->pushButtonDelUser->show();
    }
    else
    {
        if ( m_accountLogin.m_sType == "1" )
        {
            ui->pushButtonAddUser->show();
            ui->pushButtonDelUser->show();
        }
        else
        {
            ui->pushButtonAddUser->hide();
            ui->pushButtonDelUser->hide();
        }
    }

    ui->pushButtonUpdate->show();
    ui->widgetAccountEdit->show();
    ui->pushButtonAddConfirm->hide();
    ui->pushButtonUpdateConfirm->hide();
    ui->widgetAccountEdit->setEnabled(false);

    clear_WidgetAccountEdit();
    fill_WidgetAccountEdit() ;

    clear_TableWidgetRecordList();
    fill_TableWidgetRecordList();
}

void MainWindow::fillTableWidgetBookList(const string& sSearchName)
{
    for ( int i = 0 ; i < (int)root["data"].size() ; i++ )
    {
        int row = ui->tableWidgetBookList->rowCount();
        ui->tableWidgetBookList->insertRow(row);
        ui->tableWidgetBookList->setItem(row, 0, new QTableWidgetItem(pAccount->m_sName.c_str()) );
        if ( pAccount->m_sType == "1")
            ui->tableWidgetBookList->setItem(row, 1, new QTableWidgetItem((QString::fromLocal8Bit("��������Ա"))));
        else if ( pAccount->m_sType == "2")
            ui->tableWidgetBookList->setItem(row, 1, new QTableWidgetItem((QString::fromLocal8Bit("��ͨ�û�"))));

        ui->tableWidgetBookList->setItem(row, 2, new QTableWidgetItem(pAccount->m_sParent.c_str()) );

        if ( pAccount->m_sPayType == "0" )
        {
            ui->tableWidgetBookList->setItem(row, 3, new QTableWidgetItem(QString::fromLocal8Bit("�����Ʒ�")));
            QString valueLeft;
            valueLeft += pAccount->m_sValueLeft.c_str();
            valueLeft += "B" ;
            ui->tableWidgetBookList->setItem(row, 4, new QTableWidgetItem(valueLeft));
        }
        else
        {
            ui->tableWidgetBookList->setItem(row, 3, new QTableWidgetItem(QString::fromLocal8Bit("ʱ���Ʒ�")));
            QString valueLeft;
            valueLeft += pAccount->m_sValueLeft.c_str();
            valueLeft += QString::fromLocal8Bit("��") ;
            ui->tableWidgetBookList->setItem(row, 4, new QTableWidgetItem(valueLeft));
        }
    }
}
