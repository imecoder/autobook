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
#include <QtWidgets/QTableWidget>
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
    QWidget *widget_5;
    QHBoxLayout *horizontalLayout_6;
    QLabel *label;
    QComboBox *comboBoxMode;
    QSpacerItem *horizontalSpacer;
    QWidget *widget_12;
    QHBoxLayout *horizontalLayout_7;
    QLabel *label_2;
    QComboBox *comboBoxManual;
    QSpacerItem *horizontalSpacer_2;
    QWidget *widget_13;
    QHBoxLayout *horizontalLayout_8;
    QLabel *label_3;
    QLineEdit *lineEditBranchSize;
    QSpacerItem *horizontalSpacer_3;
    QWidget *widget_14;
    QHBoxLayout *horizontalLayout_16;
    QLabel *label_4;
    QComboBox *comboBoxDebug;
    QSpacerItem *horizontalSpacer_5;
    QSpacerItem *horizontalSpacer_4;
    QGroupBox *groupBox_2;
    QVBoxLayout *verticalLayout_2;
    QWidget *widget_15;
    QHBoxLayout *horizontalLayout_2;
    QWidget *widget_2;
    QHBoxLayout *horizontalLayout_4;
    QLabel *label_20;
    QLineEdit *lineEditDate;
    QSpacerItem *horizontalSpacer_8;
    QWidget *widget_3;
    QHBoxLayout *horizontalLayout_9;
    QLabel *label_24;
    QLineEdit *lineEditFrom;
    QSpacerItem *horizontalSpacer_10;
    QWidget *widget_6;
    QHBoxLayout *horizontalLayout_10;
    QLabel *label_25;
    QLineEdit *lineEditTo;
    QSpacerItem *horizontalSpacer_11;
    QWidget *widget_7;
    QHBoxLayout *horizontalLayout_11;
    QLabel *label_26;
    QLineEdit *lineEditComp;
    QSpacerItem *horizontalSpacer_13;
    QWidget *widget_8;
    QHBoxLayout *horizontalLayout_12;
    QLabel *label_27;
    QLineEdit *lineEditFlight;
    QSpacerItem *horizontalSpacer_22;
    QWidget *widget_11;
    QHBoxLayout *horizontalLayout_13;
    QLabel *label_30;
    QLineEdit *lineEditSpace;
    QSpacerItem *horizontalSpacer_12;
    QWidget *widget_10;
    QHBoxLayout *horizontalLayout_15;
    QLabel *label_29;
    QLineEdit *lineEditUser;
    QSpacerItem *horizontalSpacer_18;
    QWidget *widget_9;
    QHBoxLayout *horizontalLayout_14;
    QLabel *label_28;
    QLineEdit *lineEditContact;
    QWidget *widget;
    QHBoxLayout *horizontalLayout_3;
    QSpacerItem *horizontalSpacer_14;
    QPushButton *pushButtonBookAdd;
    QSpacerItem *horizontalSpacer_15;
    QPushButton *pushButtonBookModify;
    QSpacerItem *horizontalSpacer_16;
    QPushButton *pushButtonBookDelete;
    QSpacerItem *horizontalSpacer_17;
    QGroupBox *groupBox_9;
    QVBoxLayout *verticalLayout_3;
    QTableWidget *tableWidgetBookList;
    QWidget *widget_4;
    QHBoxLayout *horizontalLayout_5;
    QSpacerItem *horizontalSpacer_19;
    QPushButton *pushButtonRead;
    QSpacerItem *horizontalSpacer_20;
    QPushButton *pushButtonSave;
    QSpacerItem *horizontalSpacer_21;

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
        font.setFamilies({QString::fromUtf8("Microsoft YaHei UI")});
        font.setPointSize(9);
        groupBox->setFont(font);
        horizontalLayout = new QHBoxLayout(groupBox);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        widget_5 = new QWidget(groupBox);
        widget_5->setObjectName(QString::fromUtf8("widget_5"));
        widget_5->setMinimumSize(QSize(270, 30));
        widget_5->setMaximumSize(QSize(270, 30));
        horizontalLayout_6 = new QHBoxLayout(widget_5);
        horizontalLayout_6->setSpacing(0);
        horizontalLayout_6->setObjectName(QString::fromUtf8("horizontalLayout_6"));
        horizontalLayout_6->setContentsMargins(10, 0, 0, 0);
        label = new QLabel(widget_5);
        label->setObjectName(QString::fromUtf8("label"));
        label->setEnabled(true);
        label->setMinimumSize(QSize(40, 30));
        label->setMaximumSize(QSize(40, 30));
        label->setFont(font);

        horizontalLayout_6->addWidget(label);

        comboBoxMode = new QComboBox(widget_5);
        comboBoxMode->addItem(QString());
        comboBoxMode->addItem(QString());
        comboBoxMode->setObjectName(QString::fromUtf8("comboBoxMode"));
        comboBoxMode->setMinimumSize(QSize(160, 24));
        comboBoxMode->setMaximumSize(QSize(160, 24));
        comboBoxMode->setFont(font);

        horizontalLayout_6->addWidget(comboBoxMode);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_6->addItem(horizontalSpacer);


        horizontalLayout->addWidget(widget_5);

        widget_12 = new QWidget(groupBox);
        widget_12->setObjectName(QString::fromUtf8("widget_12"));
        widget_12->setMinimumSize(QSize(200, 30));
        widget_12->setMaximumSize(QSize(200, 30));
        horizontalLayout_7 = new QHBoxLayout(widget_12);
        horizontalLayout_7->setSpacing(0);
        horizontalLayout_7->setObjectName(QString::fromUtf8("horizontalLayout_7"));
        horizontalLayout_7->setContentsMargins(0, 0, 0, 0);
        label_2 = new QLabel(widget_12);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setMinimumSize(QSize(50, 30));
        label_2->setMaximumSize(QSize(50, 30));
        label_2->setFont(font);

        horizontalLayout_7->addWidget(label_2);

        comboBoxManual = new QComboBox(widget_12);
        comboBoxManual->addItem(QString());
        comboBoxManual->addItem(QString());
        comboBoxManual->setObjectName(QString::fromUtf8("comboBoxManual"));
        comboBoxManual->setMinimumSize(QSize(80, 24));
        comboBoxManual->setMaximumSize(QSize(16777215, 24));
        comboBoxManual->setFont(font);

        horizontalLayout_7->addWidget(comboBoxManual);

        horizontalSpacer_2 = new QSpacerItem(67, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_7->addItem(horizontalSpacer_2);


        horizontalLayout->addWidget(widget_12);

        widget_13 = new QWidget(groupBox);
        widget_13->setObjectName(QString::fromUtf8("widget_13"));
        widget_13->setMinimumSize(QSize(180, 30));
        widget_13->setMaximumSize(QSize(180, 30));
        horizontalLayout_8 = new QHBoxLayout(widget_13);
        horizontalLayout_8->setSpacing(0);
        horizontalLayout_8->setObjectName(QString::fromUtf8("horizontalLayout_8"));
        horizontalLayout_8->setContentsMargins(0, 0, 0, 0);
        label_3 = new QLabel(widget_13);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setMinimumSize(QSize(50, 30));
        label_3->setMaximumSize(QSize(50, 30));
        label_3->setFont(font);

        horizontalLayout_8->addWidget(label_3);

        lineEditBranchSize = new QLineEdit(widget_13);
        lineEditBranchSize->setObjectName(QString::fromUtf8("lineEditBranchSize"));
        lineEditBranchSize->setMinimumSize(QSize(50, 24));
        lineEditBranchSize->setMaximumSize(QSize(50, 24));
        lineEditBranchSize->setFont(font);

        horizontalLayout_8->addWidget(lineEditBranchSize);

        horizontalSpacer_3 = new QSpacerItem(77, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_8->addItem(horizontalSpacer_3);


        horizontalLayout->addWidget(widget_13);

        widget_14 = new QWidget(groupBox);
        widget_14->setObjectName(QString::fromUtf8("widget_14"));
        widget_14->setMinimumSize(QSize(160, 30));
        widget_14->setMaximumSize(QSize(160, 30));
        horizontalLayout_16 = new QHBoxLayout(widget_14);
        horizontalLayout_16->setSpacing(0);
        horizontalLayout_16->setObjectName(QString::fromUtf8("horizontalLayout_16"));
        horizontalLayout_16->setContentsMargins(0, 0, 0, 0);
        label_4 = new QLabel(widget_14);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setMinimumSize(QSize(60, 30));
        label_4->setMaximumSize(QSize(16777215, 30));
        label_4->setFont(font);

        horizontalLayout_16->addWidget(label_4);

        comboBoxDebug = new QComboBox(widget_14);
        comboBoxDebug->addItem(QString());
        comboBoxDebug->addItem(QString());
        comboBoxDebug->setObjectName(QString::fromUtf8("comboBoxDebug"));
        comboBoxDebug->setMinimumSize(QSize(50, 24));
        comboBoxDebug->setMaximumSize(QSize(16777215, 24));
        comboBoxDebug->setFont(font);

        horizontalLayout_16->addWidget(comboBoxDebug);

        horizontalSpacer_5 = new QSpacerItem(44, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_16->addItem(horizontalSpacer_5);


        horizontalLayout->addWidget(widget_14);

        horizontalSpacer_4 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_4);


        verticalLayout->addWidget(groupBox);

        groupBox_2 = new QGroupBox(centralwidget);
        groupBox_2->setObjectName(QString::fromUtf8("groupBox_2"));
        groupBox_2->setFont(font);
        verticalLayout_2 = new QVBoxLayout(groupBox_2);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        widget_15 = new QWidget(groupBox_2);
        widget_15->setObjectName(QString::fromUtf8("widget_15"));
        widget_15->setMaximumSize(QSize(16777215, 16777215));
        QFont font1;
        font1.setFamilies({QString::fromUtf8("Agency FB")});
        font1.setPointSize(10);
        widget_15->setFont(font1);
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

        lineEditDate = new QLineEdit(widget_2);
        lineEditDate->setObjectName(QString::fromUtf8("lineEditDate"));
        lineEditDate->setMinimumSize(QSize(60, 24));
        lineEditDate->setMaximumSize(QSize(80, 16777215));
        lineEditDate->setFont(font);

        horizontalLayout_4->addWidget(lineEditDate);


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

        lineEditFrom = new QLineEdit(widget_3);
        lineEditFrom->setObjectName(QString::fromUtf8("lineEditFrom"));
        lineEditFrom->setMinimumSize(QSize(60, 24));
        lineEditFrom->setMaximumSize(QSize(60, 16777215));
        lineEditFrom->setFont(font);

        horizontalLayout_9->addWidget(lineEditFrom);


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

        lineEditTo = new QLineEdit(widget_6);
        lineEditTo->setObjectName(QString::fromUtf8("lineEditTo"));
        lineEditTo->setMinimumSize(QSize(60, 24));
        lineEditTo->setMaximumSize(QSize(60, 16777215));
        lineEditTo->setFont(font);

        horizontalLayout_10->addWidget(lineEditTo);


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

        lineEditComp = new QLineEdit(widget_7);
        lineEditComp->setObjectName(QString::fromUtf8("lineEditComp"));
        lineEditComp->setMinimumSize(QSize(60, 24));
        lineEditComp->setMaximumSize(QSize(60, 16777215));
        lineEditComp->setFont(font);

        horizontalLayout_11->addWidget(lineEditComp);


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

        lineEditFlight = new QLineEdit(widget_8);
        lineEditFlight->setObjectName(QString::fromUtf8("lineEditFlight"));
        lineEditFlight->setMinimumSize(QSize(60, 24));
        lineEditFlight->setMaximumSize(QSize(60, 16777215));
        lineEditFlight->setFont(font);

        horizontalLayout_12->addWidget(lineEditFlight);


        horizontalLayout_2->addWidget(widget_8);

        horizontalSpacer_22 = new QSpacerItem(22, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_22);

        widget_11 = new QWidget(widget_15);
        widget_11->setObjectName(QString::fromUtf8("widget_11"));
        horizontalLayout_13 = new QHBoxLayout(widget_11);
        horizontalLayout_13->setSpacing(0);
        horizontalLayout_13->setObjectName(QString::fromUtf8("horizontalLayout_13"));
        horizontalLayout_13->setContentsMargins(0, 5, 0, 0);
        label_30 = new QLabel(widget_11);
        label_30->setObjectName(QString::fromUtf8("label_30"));
        label_30->setMinimumSize(QSize(38, 30));
        label_30->setFont(font);

        horizontalLayout_13->addWidget(label_30);

        lineEditSpace = new QLineEdit(widget_11);
        lineEditSpace->setObjectName(QString::fromUtf8("lineEditSpace"));
        lineEditSpace->setMinimumSize(QSize(40, 24));
        lineEditSpace->setMaximumSize(QSize(40, 16777215));
        lineEditSpace->setFont(font);

        horizontalLayout_13->addWidget(lineEditSpace);


        horizontalLayout_2->addWidget(widget_11);

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

        lineEditUser = new QLineEdit(widget_10);
        lineEditUser->setObjectName(QString::fromUtf8("lineEditUser"));
        lineEditUser->setMinimumSize(QSize(120, 24));
        lineEditUser->setMaximumSize(QSize(120, 16777215));
        lineEditUser->setFont(font);

        horizontalLayout_15->addWidget(lineEditUser);


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

        lineEditContact = new QLineEdit(widget_9);
        lineEditContact->setObjectName(QString::fromUtf8("lineEditContact"));
        lineEditContact->setMinimumSize(QSize(180, 24));
        lineEditContact->setMaximumSize(QSize(180, 16777215));
        lineEditContact->setFont(font);

        horizontalLayout_14->addWidget(lineEditContact);


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

        pushButtonBookAdd = new QPushButton(widget);
        pushButtonBookAdd->setObjectName(QString::fromUtf8("pushButtonBookAdd"));
        pushButtonBookAdd->setMinimumSize(QSize(300, 24));
        pushButtonBookAdd->setFont(font);

        horizontalLayout_3->addWidget(pushButtonBookAdd);

        horizontalSpacer_15 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_15);

        pushButtonBookModify = new QPushButton(widget);
        pushButtonBookModify->setObjectName(QString::fromUtf8("pushButtonBookModify"));
        pushButtonBookModify->setMinimumSize(QSize(300, 24));
        pushButtonBookModify->setFont(font);

        horizontalLayout_3->addWidget(pushButtonBookModify);

        horizontalSpacer_16 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_16);

        pushButtonBookDelete = new QPushButton(widget);
        pushButtonBookDelete->setObjectName(QString::fromUtf8("pushButtonBookDelete"));
        pushButtonBookDelete->setMinimumSize(QSize(300, 24));
        pushButtonBookDelete->setFont(font);

        horizontalLayout_3->addWidget(pushButtonBookDelete);

        horizontalSpacer_17 = new QSpacerItem(52, 27, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_17);


        verticalLayout_2->addWidget(widget);


        verticalLayout->addWidget(groupBox_2);

        groupBox_9 = new QGroupBox(centralwidget);
        groupBox_9->setObjectName(QString::fromUtf8("groupBox_9"));
        groupBox_9->setFont(font);
        verticalLayout_3 = new QVBoxLayout(groupBox_9);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        tableWidgetBookList = new QTableWidget(groupBox_9);
        if (tableWidgetBookList->columnCount() < 8)
            tableWidgetBookList->setColumnCount(8);
        QFont font2;
        font2.setPointSize(9);
        QTableWidgetItem *__qtablewidgetitem = new QTableWidgetItem();
        __qtablewidgetitem->setFont(font2);
        tableWidgetBookList->setHorizontalHeaderItem(0, __qtablewidgetitem);
        QTableWidgetItem *__qtablewidgetitem1 = new QTableWidgetItem();
        __qtablewidgetitem1->setFont(font);
        tableWidgetBookList->setHorizontalHeaderItem(1, __qtablewidgetitem1);
        QTableWidgetItem *__qtablewidgetitem2 = new QTableWidgetItem();
        __qtablewidgetitem2->setFont(font);
        tableWidgetBookList->setHorizontalHeaderItem(2, __qtablewidgetitem2);
        QTableWidgetItem *__qtablewidgetitem3 = new QTableWidgetItem();
        __qtablewidgetitem3->setFont(font);
        tableWidgetBookList->setHorizontalHeaderItem(3, __qtablewidgetitem3);
        QTableWidgetItem *__qtablewidgetitem4 = new QTableWidgetItem();
        __qtablewidgetitem4->setFont(font);
        tableWidgetBookList->setHorizontalHeaderItem(4, __qtablewidgetitem4);
        QTableWidgetItem *__qtablewidgetitem5 = new QTableWidgetItem();
        __qtablewidgetitem5->setFont(font);
        tableWidgetBookList->setHorizontalHeaderItem(5, __qtablewidgetitem5);
        QTableWidgetItem *__qtablewidgetitem6 = new QTableWidgetItem();
        __qtablewidgetitem6->setFont(font);
        tableWidgetBookList->setHorizontalHeaderItem(6, __qtablewidgetitem6);
        QTableWidgetItem *__qtablewidgetitem7 = new QTableWidgetItem();
        __qtablewidgetitem7->setFont(font);
        tableWidgetBookList->setHorizontalHeaderItem(7, __qtablewidgetitem7);
        tableWidgetBookList->setObjectName(QString::fromUtf8("tableWidgetBookList"));
        tableWidgetBookList->setFont(font);

        verticalLayout_3->addWidget(tableWidgetBookList);


        verticalLayout->addWidget(groupBox_9);

        widget_4 = new QWidget(centralwidget);
        widget_4->setObjectName(QString::fromUtf8("widget_4"));
        horizontalLayout_5 = new QHBoxLayout(widget_4);
        horizontalLayout_5->setObjectName(QString::fromUtf8("horizontalLayout_5"));
        horizontalSpacer_19 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_5->addItem(horizontalSpacer_19);

        pushButtonRead = new QPushButton(widget_4);
        pushButtonRead->setObjectName(QString::fromUtf8("pushButtonRead"));
        pushButtonRead->setMinimumSize(QSize(200, 0));
        pushButtonRead->setFont(font);

        horizontalLayout_5->addWidget(pushButtonRead);

        horizontalSpacer_20 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_5->addItem(horizontalSpacer_20);

        pushButtonSave = new QPushButton(widget_4);
        pushButtonSave->setObjectName(QString::fromUtf8("pushButtonSave"));
        pushButtonSave->setMinimumSize(QSize(200, 0));
        pushButtonSave->setFont(font);

        horizontalLayout_5->addWidget(pushButtonSave);

        horizontalSpacer_21 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_5->addItem(horizontalSpacer_21);


        verticalLayout->addWidget(widget_4);

        MainWindow->setCentralWidget(centralwidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "\350\207\252\345\212\250\350\256\242\347\245\250\351\205\215\347\275\256", nullptr));
        groupBox->setTitle(QCoreApplication::translate("MainWindow", "\345\237\272\346\234\254\351\205\215\347\275\256", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "\346\250\241\345\274\217", nullptr));
        comboBoxMode->setItemText(0, QCoreApplication::translate("MainWindow", "\345\210\267\347\245\250+\345\215\240\347\245\250", nullptr));
        comboBoxMode->setItemText(1, QCoreApplication::translate("MainWindow", "\345\210\267\347\245\250+\345\215\240\347\245\250+\345\277\253\351\200\237\351\242\204\345\256\232", nullptr));

        label_2->setText(QCoreApplication::translate("MainWindow", "\346\211\213/\350\207\252\345\212\250", nullptr));
        comboBoxManual->setItemText(0, QCoreApplication::translate("MainWindow", "\350\207\252\345\212\250", nullptr));
        comboBoxManual->setItemText(1, QCoreApplication::translate("MainWindow", "\346\211\213\345\212\250", nullptr));

        label_3->setText(QCoreApplication::translate("MainWindow", "\345\210\206\346\224\257\346\225\260", nullptr));
        label_4->setText(QCoreApplication::translate("MainWindow", "\350\260\203\350\257\225\346\250\241\345\274\217", nullptr));
        comboBoxDebug->setItemText(0, QCoreApplication::translate("MainWindow", "\346\230\257", nullptr));
        comboBoxDebug->setItemText(1, QCoreApplication::translate("MainWindow", "\345\220\246", nullptr));

        groupBox_2->setTitle(QCoreApplication::translate("MainWindow", "\351\205\215\347\275\256\350\256\242\347\245\250", nullptr));
        label_20->setText(QCoreApplication::translate("MainWindow", "\346\227\245\346\234\237", nullptr));
        label_24->setText(QCoreApplication::translate("MainWindow", "\350\265\267\345\247\213", nullptr));
        label_25->setText(QCoreApplication::translate("MainWindow", "\347\273\210\347\202\271", nullptr));
        label_26->setText(QCoreApplication::translate("MainWindow", "\350\210\252\345\217\270", nullptr));
        label_27->setText(QCoreApplication::translate("MainWindow", "\350\210\252\347\217\255", nullptr));
        label_30->setText(QCoreApplication::translate("MainWindow", "\344\273\223\344\275\215", nullptr));
        label_29->setText(QCoreApplication::translate("MainWindow", "\347\224\250\346\210\267", nullptr));
        label_28->setText(QCoreApplication::translate("MainWindow", "\350\201\224\347\263\273\346\226\271\345\274\217", nullptr));
        pushButtonBookAdd->setText(QCoreApplication::translate("MainWindow", "\346\267\273\345\212\240", nullptr));
        pushButtonBookModify->setText(QCoreApplication::translate("MainWindow", "\344\277\256\346\224\271", nullptr));
        pushButtonBookDelete->setText(QCoreApplication::translate("MainWindow", "\345\210\240\351\231\244", nullptr));
        groupBox_9->setTitle(QCoreApplication::translate("MainWindow", "\351\205\215\347\275\256\345\210\227\350\241\250", nullptr));
        QTableWidgetItem *___qtablewidgetitem = tableWidgetBookList->horizontalHeaderItem(0);
        ___qtablewidgetitem->setText(QCoreApplication::translate("MainWindow", "\346\227\245\346\234\237", nullptr));
        QTableWidgetItem *___qtablewidgetitem1 = tableWidgetBookList->horizontalHeaderItem(1);
        ___qtablewidgetitem1->setText(QCoreApplication::translate("MainWindow", "\350\265\267\345\247\213", nullptr));
        QTableWidgetItem *___qtablewidgetitem2 = tableWidgetBookList->horizontalHeaderItem(2);
        ___qtablewidgetitem2->setText(QCoreApplication::translate("MainWindow", "\347\233\256\347\232\204", nullptr));
        QTableWidgetItem *___qtablewidgetitem3 = tableWidgetBookList->horizontalHeaderItem(3);
        ___qtablewidgetitem3->setText(QCoreApplication::translate("MainWindow", "\350\210\252\345\217\270", nullptr));
        QTableWidgetItem *___qtablewidgetitem4 = tableWidgetBookList->horizontalHeaderItem(4);
        ___qtablewidgetitem4->setText(QCoreApplication::translate("MainWindow", "\350\210\252\347\217\255", nullptr));
        QTableWidgetItem *___qtablewidgetitem5 = tableWidgetBookList->horizontalHeaderItem(5);
        ___qtablewidgetitem5->setText(QCoreApplication::translate("MainWindow", "\344\273\223\344\275\215", nullptr));
        QTableWidgetItem *___qtablewidgetitem6 = tableWidgetBookList->horizontalHeaderItem(6);
        ___qtablewidgetitem6->setText(QCoreApplication::translate("MainWindow", "\347\224\250\346\210\267", nullptr));
        QTableWidgetItem *___qtablewidgetitem7 = tableWidgetBookList->horizontalHeaderItem(7);
        ___qtablewidgetitem7->setText(QCoreApplication::translate("MainWindow", "\350\201\224\347\263\273\346\226\271\345\274\217", nullptr));
        pushButtonRead->setText(QCoreApplication::translate("MainWindow", "\350\257\273\345\217\226", nullptr));
        pushButtonSave->setText(QCoreApplication::translate("MainWindow", "\344\277\235\345\255\230", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
