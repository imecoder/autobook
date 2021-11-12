/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.2.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QTableView>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QVBoxLayout *verticalLayout;
    QGroupBox *groupBox;
    QHBoxLayout *horizontalLayout;
    QLabel *label;
    QComboBox *mode;
    QSpacerItem *horizontalSpacer;
    QLabel *label_2;
    QComboBox *manual;
    QSpacerItem *horizontalSpacer_2;
    QLabel *label_3;
    QLineEdit *branch_size;
    QSpacerItem *horizontalSpacer_3;
    QGroupBox *groupBox_2;
    QVBoxLayout *verticalLayout_2;
    QWidget *widget_15;
    QHBoxLayout *horizontalLayout_2;
    QWidget *widget_2;
    QHBoxLayout *horizontalLayout_4;
    QLabel *label_20;
    QLineEdit *lineEdit_20;
    QSpacerItem *horizontalSpacer_8;
    QWidget *widget_3;
    QHBoxLayout *horizontalLayout_9;
    QLabel *label_24;
    QLineEdit *lineEdit_24;
    QSpacerItem *horizontalSpacer_10;
    QWidget *widget_6;
    QHBoxLayout *horizontalLayout_10;
    QLabel *label_25;
    QLineEdit *lineEdit_25;
    QSpacerItem *horizontalSpacer_11;
    QWidget *widget_7;
    QHBoxLayout *horizontalLayout_11;
    QLabel *label_26;
    QLineEdit *lineEdit_26;
    QSpacerItem *horizontalSpacer_13;
    QWidget *widget_8;
    QHBoxLayout *horizontalLayout_12;
    QLabel *label_27;
    QLineEdit *lineEdit_27;
    QSpacerItem *horizontalSpacer_12;
    QWidget *widget_10;
    QHBoxLayout *horizontalLayout_15;
    QLabel *label_29;
    QLineEdit *lineEdit_29;
    QSpacerItem *horizontalSpacer_18;
    QWidget *widget_9;
    QHBoxLayout *horizontalLayout_14;
    QLabel *label_28;
    QLineEdit *lineEdit_28;
    QWidget *widget;
    QHBoxLayout *horizontalLayout_3;
    QSpacerItem *horizontalSpacer_14;
    QPushButton *pushButton_8;
    QSpacerItem *horizontalSpacer_15;
    QPushButton *pushButton_9;
    QSpacerItem *horizontalSpacer_16;
    QPushButton *pushButton_10;
    QSpacerItem *horizontalSpacer_17;
    QGroupBox *groupBox_9;
    QVBoxLayout *verticalLayout_3;
    QTableView *tableView;
    QPushButton *pushButton_4;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1166, 501);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        verticalLayout = new QVBoxLayout(centralwidget);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        groupBox = new QGroupBox(centralwidget);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(groupBox->sizePolicy().hasHeightForWidth());
        groupBox->setSizePolicy(sizePolicy);
        QFont font;
        font.setFamilies({QString::fromUtf8("Agency FB")});
        font.setPointSize(10);
        groupBox->setFont(font);
        horizontalLayout = new QHBoxLayout(groupBox);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        label = new QLabel(groupBox);
        label->setObjectName(QString::fromUtf8("label"));
        label->setMinimumSize(QSize(50, 30));
        label->setFont(font);

        horizontalLayout->addWidget(label);

        mode = new QComboBox(groupBox);
        mode->addItem(QString());
        mode->addItem(QString());
        mode->setObjectName(QString::fromUtf8("mode"));
        mode->setMinimumSize(QSize(200, 30));
        mode->setFont(font);

        horizontalLayout->addWidget(mode);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);

        label_2 = new QLabel(groupBox);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setMinimumSize(QSize(60, 30));
        label_2->setFont(font);

        horizontalLayout->addWidget(label_2);

        manual = new QComboBox(groupBox);
        manual->addItem(QString());
        manual->addItem(QString());
        manual->setObjectName(QString::fromUtf8("manual"));
        manual->setMinimumSize(QSize(80, 30));
        manual->setFont(font);

        horizontalLayout->addWidget(manual);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_2);

        label_3 = new QLabel(groupBox);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setMinimumSize(QSize(60, 30));
        label_3->setFont(font);

        horizontalLayout->addWidget(label_3);

        branch_size = new QLineEdit(groupBox);
        branch_size->setObjectName(QString::fromUtf8("branch_size"));
        branch_size->setMinimumSize(QSize(100, 30));
        branch_size->setFont(font);

        horizontalLayout->addWidget(branch_size);

        horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_3);


        verticalLayout->addWidget(groupBox);

        groupBox_2 = new QGroupBox(centralwidget);
        groupBox_2->setObjectName(QString::fromUtf8("groupBox_2"));
        groupBox_2->setFont(font);
        verticalLayout_2 = new QVBoxLayout(groupBox_2);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        widget_15 = new QWidget(groupBox_2);
        widget_15->setObjectName(QString::fromUtf8("widget_15"));
        widget_15->setMaximumSize(QSize(16777215, 16777215));
        widget_15->setFont(font);
        horizontalLayout_2 = new QHBoxLayout(widget_15);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        widget_2 = new QWidget(widget_15);
        widget_2->setObjectName(QString::fromUtf8("widget_2"));
        horizontalLayout_4 = new QHBoxLayout(widget_2);
        horizontalLayout_4->setSpacing(0);
        horizontalLayout_4->setObjectName(QString::fromUtf8("horizontalLayout_4"));
        horizontalLayout_4->setContentsMargins(0, 5, 0, 0);
        label_20 = new QLabel(widget_2);
        label_20->setObjectName(QString::fromUtf8("label_20"));
        label_20->setMinimumSize(QSize(38, 30));
        label_20->setFont(font);

        horizontalLayout_4->addWidget(label_20);

        lineEdit_20 = new QLineEdit(widget_2);
        lineEdit_20->setObjectName(QString::fromUtf8("lineEdit_20"));
        lineEdit_20->setMinimumSize(QSize(60, 30));
        lineEdit_20->setMaximumSize(QSize(80, 16777215));
        lineEdit_20->setFont(font);

        horizontalLayout_4->addWidget(lineEdit_20);


        horizontalLayout_2->addWidget(widget_2);

        horizontalSpacer_8 = new QSpacerItem(22, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_8);

        widget_3 = new QWidget(widget_15);
        widget_3->setObjectName(QString::fromUtf8("widget_3"));
        horizontalLayout_9 = new QHBoxLayout(widget_3);
        horizontalLayout_9->setSpacing(0);
        horizontalLayout_9->setObjectName(QString::fromUtf8("horizontalLayout_9"));
        horizontalLayout_9->setContentsMargins(0, 5, 0, 0);
        label_24 = new QLabel(widget_3);
        label_24->setObjectName(QString::fromUtf8("label_24"));
        label_24->setMinimumSize(QSize(38, 30));
        label_24->setFont(font);

        horizontalLayout_9->addWidget(label_24);

        lineEdit_24 = new QLineEdit(widget_3);
        lineEdit_24->setObjectName(QString::fromUtf8("lineEdit_24"));
        lineEdit_24->setMinimumSize(QSize(60, 30));
        lineEdit_24->setMaximumSize(QSize(60, 16777215));
        lineEdit_24->setFont(font);

        horizontalLayout_9->addWidget(lineEdit_24);


        horizontalLayout_2->addWidget(widget_3);

        horizontalSpacer_10 = new QSpacerItem(22, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_10);

        widget_6 = new QWidget(widget_15);
        widget_6->setObjectName(QString::fromUtf8("widget_6"));
        horizontalLayout_10 = new QHBoxLayout(widget_6);
        horizontalLayout_10->setSpacing(0);
        horizontalLayout_10->setObjectName(QString::fromUtf8("horizontalLayout_10"));
        horizontalLayout_10->setContentsMargins(0, 5, 0, 0);
        label_25 = new QLabel(widget_6);
        label_25->setObjectName(QString::fromUtf8("label_25"));
        label_25->setMinimumSize(QSize(38, 30));
        label_25->setFont(font);

        horizontalLayout_10->addWidget(label_25);

        lineEdit_25 = new QLineEdit(widget_6);
        lineEdit_25->setObjectName(QString::fromUtf8("lineEdit_25"));
        lineEdit_25->setMinimumSize(QSize(60, 30));
        lineEdit_25->setMaximumSize(QSize(60, 16777215));
        lineEdit_25->setFont(font);

        horizontalLayout_10->addWidget(lineEdit_25);


        horizontalLayout_2->addWidget(widget_6);

        horizontalSpacer_11 = new QSpacerItem(22, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_11);

        widget_7 = new QWidget(widget_15);
        widget_7->setObjectName(QString::fromUtf8("widget_7"));
        horizontalLayout_11 = new QHBoxLayout(widget_7);
        horizontalLayout_11->setSpacing(0);
        horizontalLayout_11->setObjectName(QString::fromUtf8("horizontalLayout_11"));
        horizontalLayout_11->setContentsMargins(0, 5, 0, 0);
        label_26 = new QLabel(widget_7);
        label_26->setObjectName(QString::fromUtf8("label_26"));
        label_26->setMinimumSize(QSize(38, 30));
        label_26->setFont(font);

        horizontalLayout_11->addWidget(label_26);

        lineEdit_26 = new QLineEdit(widget_7);
        lineEdit_26->setObjectName(QString::fromUtf8("lineEdit_26"));
        lineEdit_26->setMinimumSize(QSize(60, 30));
        lineEdit_26->setMaximumSize(QSize(60, 16777215));
        lineEdit_26->setFont(font);

        horizontalLayout_11->addWidget(lineEdit_26);


        horizontalLayout_2->addWidget(widget_7);

        horizontalSpacer_13 = new QSpacerItem(22, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_13);

        widget_8 = new QWidget(widget_15);
        widget_8->setObjectName(QString::fromUtf8("widget_8"));
        horizontalLayout_12 = new QHBoxLayout(widget_8);
        horizontalLayout_12->setSpacing(0);
        horizontalLayout_12->setObjectName(QString::fromUtf8("horizontalLayout_12"));
        horizontalLayout_12->setContentsMargins(0, 5, 0, 0);
        label_27 = new QLabel(widget_8);
        label_27->setObjectName(QString::fromUtf8("label_27"));
        label_27->setMinimumSize(QSize(38, 30));
        label_27->setFont(font);

        horizontalLayout_12->addWidget(label_27);

        lineEdit_27 = new QLineEdit(widget_8);
        lineEdit_27->setObjectName(QString::fromUtf8("lineEdit_27"));
        lineEdit_27->setMinimumSize(QSize(60, 30));
        lineEdit_27->setMaximumSize(QSize(60, 16777215));
        lineEdit_27->setFont(font);

        horizontalLayout_12->addWidget(lineEdit_27);


        horizontalLayout_2->addWidget(widget_8);

        horizontalSpacer_12 = new QSpacerItem(22, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_12);

        widget_10 = new QWidget(widget_15);
        widget_10->setObjectName(QString::fromUtf8("widget_10"));
        horizontalLayout_15 = new QHBoxLayout(widget_10);
        horizontalLayout_15->setSpacing(0);
        horizontalLayout_15->setObjectName(QString::fromUtf8("horizontalLayout_15"));
        horizontalLayout_15->setContentsMargins(0, 5, 0, 0);
        label_29 = new QLabel(widget_10);
        label_29->setObjectName(QString::fromUtf8("label_29"));
        label_29->setMinimumSize(QSize(38, 30));
        label_29->setFont(font);

        horizontalLayout_15->addWidget(label_29);

        lineEdit_29 = new QLineEdit(widget_10);
        lineEdit_29->setObjectName(QString::fromUtf8("lineEdit_29"));
        lineEdit_29->setMinimumSize(QSize(120, 30));
        lineEdit_29->setMaximumSize(QSize(120, 16777215));
        lineEdit_29->setFont(font);

        horizontalLayout_15->addWidget(lineEdit_29);


        horizontalLayout_2->addWidget(widget_10);

        horizontalSpacer_18 = new QSpacerItem(22, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_18);

        widget_9 = new QWidget(widget_15);
        widget_9->setObjectName(QString::fromUtf8("widget_9"));
        horizontalLayout_14 = new QHBoxLayout(widget_9);
        horizontalLayout_14->setSpacing(0);
        horizontalLayout_14->setObjectName(QString::fromUtf8("horizontalLayout_14"));
        horizontalLayout_14->setContentsMargins(0, 5, 0, 0);
        label_28 = new QLabel(widget_9);
        label_28->setObjectName(QString::fromUtf8("label_28"));
        label_28->setMinimumSize(QSize(70, 30));
        label_28->setFont(font);

        horizontalLayout_14->addWidget(label_28);

        lineEdit_28 = new QLineEdit(widget_9);
        lineEdit_28->setObjectName(QString::fromUtf8("lineEdit_28"));
        lineEdit_28->setMinimumSize(QSize(120, 30));
        lineEdit_28->setMaximumSize(QSize(120, 16777215));
        lineEdit_28->setFont(font);

        horizontalLayout_14->addWidget(lineEdit_28);


        horizontalLayout_2->addWidget(widget_9);


        verticalLayout_2->addWidget(widget_15);

        widget = new QWidget(groupBox_2);
        widget->setObjectName(QString::fromUtf8("widget"));
        widget->setMinimumSize(QSize(0, 30));
        horizontalLayout_3 = new QHBoxLayout(widget);
        horizontalLayout_3->setSpacing(0);
        horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
        horizontalLayout_3->setContentsMargins(0, 0, 0, 0);
        horizontalSpacer_14 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_14);

        pushButton_8 = new QPushButton(widget);
        pushButton_8->setObjectName(QString::fromUtf8("pushButton_8"));
        pushButton_8->setMinimumSize(QSize(300, 30));

        horizontalLayout_3->addWidget(pushButton_8);

        horizontalSpacer_15 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_15);

        pushButton_9 = new QPushButton(widget);
        pushButton_9->setObjectName(QString::fromUtf8("pushButton_9"));
        pushButton_9->setMinimumSize(QSize(300, 30));

        horizontalLayout_3->addWidget(pushButton_9);

        horizontalSpacer_16 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_16);

        pushButton_10 = new QPushButton(widget);
        pushButton_10->setObjectName(QString::fromUtf8("pushButton_10"));
        pushButton_10->setMinimumSize(QSize(300, 30));

        horizontalLayout_3->addWidget(pushButton_10);

        horizontalSpacer_17 = new QSpacerItem(52, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_17);


        verticalLayout_2->addWidget(widget);


        verticalLayout->addWidget(groupBox_2);

        groupBox_9 = new QGroupBox(centralwidget);
        groupBox_9->setObjectName(QString::fromUtf8("groupBox_9"));
        groupBox_9->setFont(font);
        verticalLayout_3 = new QVBoxLayout(groupBox_9);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        tableView = new QTableView(groupBox_9);
        tableView->setObjectName(QString::fromUtf8("tableView"));

        verticalLayout_3->addWidget(tableView);


        verticalLayout->addWidget(groupBox_9);

        pushButton_4 = new QPushButton(centralwidget);
        pushButton_4->setObjectName(QString::fromUtf8("pushButton_4"));
        pushButton_4->setFont(font);

        verticalLayout->addWidget(pushButton_4);

        MainWindow->setCentralWidget(centralwidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        groupBox->setTitle(QCoreApplication::translate("MainWindow", "\345\237\272\346\234\254\351\205\215\347\275\256", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "\346\250\241\345\274\217", nullptr));
        mode->setItemText(0, QCoreApplication::translate("MainWindow", "1. \345\210\267\347\245\250+\345\215\240\347\245\250+\345\277\253\351\200\237\351\242\204\345\256\232", nullptr));
        mode->setItemText(1, QCoreApplication::translate("MainWindow", "2. \345\210\267\347\245\250+\345\215\240\347\245\250", nullptr));

        label_2->setText(QCoreApplication::translate("MainWindow", "\346\211\213/\350\207\252\345\212\250", nullptr));
        manual->setItemText(0, QCoreApplication::translate("MainWindow", "\350\207\252\345\212\250", nullptr));
        manual->setItemText(1, QCoreApplication::translate("MainWindow", "\346\211\213\345\212\250", nullptr));

        label_3->setText(QCoreApplication::translate("MainWindow", "\345\210\206\346\224\257\346\225\260", nullptr));
        groupBox_2->setTitle(QCoreApplication::translate("MainWindow", "\351\205\215\347\275\256\350\256\242\347\245\250", nullptr));
        label_20->setText(QCoreApplication::translate("MainWindow", "\346\227\245\346\234\237", nullptr));
        label_24->setText(QCoreApplication::translate("MainWindow", "\350\265\267\345\247\213", nullptr));
        label_25->setText(QCoreApplication::translate("MainWindow", "\347\273\210\347\202\271", nullptr));
        label_26->setText(QCoreApplication::translate("MainWindow", "\350\210\252\345\217\270", nullptr));
        label_27->setText(QCoreApplication::translate("MainWindow", "\350\210\252\347\217\255", nullptr));
        label_29->setText(QCoreApplication::translate("MainWindow", "\347\224\250\346\210\267", nullptr));
        label_28->setText(QCoreApplication::translate("MainWindow", "\350\201\224\347\263\273\346\226\271\345\274\217", nullptr));
        pushButton_8->setText(QCoreApplication::translate("MainWindow", "\346\267\273\345\212\240", nullptr));
        pushButton_9->setText(QCoreApplication::translate("MainWindow", "\344\277\256\346\224\271", nullptr));
        pushButton_10->setText(QCoreApplication::translate("MainWindow", "\345\210\240\351\231\244", nullptr));
        groupBox_9->setTitle(QCoreApplication::translate("MainWindow", "\351\205\215\347\275\256\345\210\227\350\241\250", nullptr));
        pushButton_4->setText(QCoreApplication::translate("MainWindow", "\344\277\235\345\255\230", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
