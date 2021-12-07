#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtWidgets>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_pushButtonRead_clicked();

    void on_pushButtonSave_clicked();

    void on_pushButtonBookAdd_clicked();

    void on_pushButtonBookModify_clicked();

    void on_pushButtonBookDelete_clicked();

    void on_tableWidgetBookList_clicked(int row,int column);

private:
    Ui::MainWindow *ui;
    QJsonObject jsonBaseConfig;
    QJsonArray jsonBookConfig;
    int currentRow;

    void readBase();
    void writeBase();
    void readBook();
    void writeBook();

    void fillBaseConfig();
    void clearBookConfig();
    void fillBookConfig();
    void clearTableWidgetBookList();
    void fillTableWidgetBookList();


};
#endif // MAINWINDOW_H
