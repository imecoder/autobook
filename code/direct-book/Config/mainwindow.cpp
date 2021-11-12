#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QtWidgets>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButtonRead_clicked()
{
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

    QJsonObject jsonObject ;

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

