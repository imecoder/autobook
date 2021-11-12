#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

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

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
