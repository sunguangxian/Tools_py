# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'string_transfer.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textBrowser_src = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_src.setReadOnly(False)
        self.textBrowser_src.setObjectName("textBrowser_src")
        self.horizontalLayout_2.addWidget(self.textBrowser_src)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_copy_dst = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_copy_dst.setObjectName("pushButton_copy_dst")
        self.verticalLayout.addWidget(self.pushButton_copy_dst)
        self.pushButton_hex_to_string = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_hex_to_string.setObjectName("pushButton_hex_to_string")
        self.verticalLayout.addWidget(self.pushButton_hex_to_string)
        self.pushButton_clear_src = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_clear_src.setObjectName("pushButton_clear_src")
        self.verticalLayout.addWidget(self.pushButton_clear_src)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.textBrowser_dst = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_dst.setObjectName("textBrowser_dst")
        self.horizontalLayout_2.addWidget(self.textBrowser_dst)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HEX-字符互转"))
        self.textBrowser_src.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_copy_dst.setText(_translate("MainWindow", "复制输出结果"))
        self.pushButton_hex_to_string.setText(_translate("MainWindow", "HEX转字符串"))
        self.pushButton_clear_src.setText(_translate("MainWindow", "清除输入框"))
        self.textBrowser_dst.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
