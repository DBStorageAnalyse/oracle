# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys
import unload_ctl


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.init()
        MainWindow.resize(860, 560)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./icons/db.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tab = QtWidgets.QWidget()
        self.tabWidget.setMovable(1)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 80))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 80))
        self.groupBox.setTitle("")
        self.color = QtGui.QColor(150, 150, 150)  # 颜色(190, 180, 150) (140, 140, 140)　(190, 200, 200)
        self.groupBox.setStyleSheet('QGroupBox{border: 2px groove grey; border-radius:5px;\
        border-style: outset;background-color:%s}' % self.color.name())  # 利用样式
        self.pushButton = QtWidgets.QPushButton(self.groupBox)  # 添加文件
        self.pushButton.setGeometry(QtCore.QRect(20, 30, 75, 23))
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)  # 移除文件
        self.pushButton_2.setGeometry(QtCore.QRect(120, 30, 75, 23))
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)  # 清空列表
        self.pushButton_3.setGeometry(QtCore.QRect(220, 30, 75, 23))
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)  # 开始解析
        self.pushButton_4.setGeometry(QtCore.QRect(320, 30, 75, 23))
        self.pushButton_4.setDisabled(1)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox)  # 停止解析
        self.pushButton_4.setDisabled(1)
        self.pushButton_5.setGeometry(QtCore.QRect(420, 30, 75, 23))
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.tab)  # file table
        self.gridLayout_2.addWidget(self.tableWidget, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.progressBar = QtWidgets.QProgressBar(self.tab_2)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 4))  # 进度条宽度
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.gridLayout_3.addWidget(self.progressBar, 2, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.tab_2)  # 分隔条
        self.splitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter.setLineWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(3)  # 分隔条的 宽度
        self.treeWidget1 = QtWidgets.QTreeWidget(self.splitter)  # 标签2的 tree
        self.treeWidget1.setHeaderHidden(1)
        self.tableWidget2 = QtWidgets.QTableWidget(self.splitter)  # 标签2的 表2
        self.tableWidget2.setColumnCount(0)
        self.tableWidget2.setRowCount(0)
        self.gridLayout_3.addWidget(self.splitter, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.splitter.setStretchFactor(1, 2)  # 设置分隔条显示比例

        self.tab_3 = QtWidgets.QWidget()  # 标签3,HEX
        # self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()  # 标签4,高级信息
        self.tabWidget.addTab(self.tab_4, "")
        self.text_1 = QtWidgets.QTextEdit(self.tab_4)
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_4.addWidget(self.text_1, 0, 0, 1, 1)
        self.tab_5 = QtWidgets.QWidget()
        self.label = QtWidgets.QLabel(self.tab_5)
        self.label.setGeometry(QtCore.QRect(50, 70, 86, 116))
        self.label_2 = QtWidgets.QLabel(self.tab_5)
        self.label_2.setGeometry(QtCore.QRect(200, 160, 286, 131))
        self.color = QtGui.QColor(140, 140, 140)  # 关于的颜色 (190, 180, 150)　(190, 200, 200) (140, 140, 140)
        self.label_2.setStyleSheet('QLabel{border:2px groove grey; border-radius:5px;\
        border-style: outset;background-color:%s}' % self.color.name())  #
        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 831, 23))
        MainWindow.setMenuBar(self.menubar)

        self.expdbAction = QtWidgets.QAction(MainWindow)  # expdbAction =================
        self.expdbAction.triggered.connect(MainWindow.helpAbout)
        self.expinfoAction = QtWidgets.QAction(MainWindow)  # expinfoAction =================
        self.expinfoAction.triggered.connect(MainWindow.helpAbout)
        self.selectallAction = QtWidgets.QAction(MainWindow)  # selectallAction =================
        self.selectallAction.triggered.connect(MainWindow.selectall)
        self.notselectAction = QtWidgets.QAction(MainWindow)  # notselectAction =================
        self.notselectAction.triggered.connect(MainWindow.notselect)

        self.pushButton.clicked.connect(self.fileOpen)  # 添加文件
        self.pushButton_2.clicked.connect(self.fileDel)  # 移除文件
        self.pushButton_3.clicked.connect(self.allDel)  # 清空列表
        self.pushButton_4.clicked.connect(self.unload)  # 开始解析
        self.pushButton_5.clicked.connect(self.helpAbout)  # 停止解析
        self.treeWidget1.itemClicked.connect(self.showSelected)  # 左键单击事件
        self.treeWidget1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # tree 的 右键菜单开关

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)  # 初始显示的标签索引
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "控制文件 解析工具  V%s" % self.version))
        self.pushButton.setText(_translate("MainWindow", "添加文件"))
        self.pushButton_2.setText(_translate("MainWindow", "移出文件"))
        self.pushButton_3.setText(_translate("MainWindow", "清空列表"))
        self.pushButton_4.setText(_translate("MainWindow", "开始解析"))
        self.pushButton_5.setText(_translate("MainWindow", "停止解析"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "选择文件"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "解析文件"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "HEX"))
        self.label.setText(_translate("MainWindow", ""))
        about = 'CTL Unload V%s\t\n\n\n解析ctl文件\n支持10g/11g/12c各版本的ctl\n支持解析大、小端平台的ctl\n可运行于unix/linux/win平台' % self.version
        self.label_2.setText(_translate("MainWindow", "%s" % about))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "高级信息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "关于"))

        self.expdbAction.setText(_translate("MainWindow", "expdb"))  # 菜单栏  子菜单
        self.expinfoAction.setText(_translate("MainWindow", "expinfo"))  # 菜单栏  子菜单
        self.selectallAction.setText(_translate("MainWindow", "selectall"))  # 菜单栏  子菜单
        self.notselectAction.setText(_translate("MainWindow", "notselect"))  # 菜单栏  子菜单

    def init(self):
        self.version = '1.1.0'
        self.file_infos = []
        self.ora = unload_ctl.Unload_DB()

    def fileOpen(self):
        fn, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Files...", None, "ctl-Files (*.ctl);;All Files (*)")
        files = self.ora.file_init(fn)
        for file in files:
            self.file_infos.append(file)
        if len(self.file_infos) == 0:
            return
        self.file_infos.sort(key=lambda x: (x.f_no))  # 排序 磁盘和磁盘组。多关键字排序
        self.file_tab()  # 显示磁盘信息
        self.pushButton_4.setDisabled(0)

    def fileDel(self):
        aa1 = self.tableWidget.currentRow()
        if len(self.file_infos) == 0:
            return
        del self.file_infos[aa1]
        self.file_tab()

    def allDel(self):
        self.file_infos = []
        self.file_tab()
        self.pushButton_4.setDisabled(1)

    def stop_unload(self):
        if self.out_file != 0 and self.out_file.is_alive() == True:
            QtWidgets.QMessageBox.about(self, "提示", "停止解析 ... \n")

    # 显示文件列表
    def file_tab(self):
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setAlternatingRowColors(True)  # 隔行变色
        self.tableWidget.setRowCount(len(self.file_infos))
        header = ['file_path', 'file#', 'type', 'db_name', 'f_size(M)', 'blk_sum', 'blk_size', 'version', 'endian',
                  'dbid']
        self.tableWidget.setHorizontalHeaderLabels(header)
        self.tableWidget.setColumnWidth(0, 200);
        self.tableWidget.setColumnWidth(1, 40);
        self.tableWidget.setColumnWidth(2, 40)
        self.tableWidget.setColumnWidth(3, 70);
        self.tableWidget.setColumnWidth(4, 70);
        self.tableWidget.setColumnWidth(5, 70);
        self.tableWidget.setColumnWidth(6, 60);
        self.tableWidget.setColumnWidth(7, 70);
        self.tableWidget.setColumnWidth(8, 50);

        for i in range(len(self.file_infos)):
            endian = {'<': 'little', '>': 'big'};
            big_ts = {0: 'no', 1: 'yes'}
            file_info1 = self.file_infos[i]
            self.tableWidget.setRowHeight(i, 20)
            self.tableWidget.setItem(i, 0, Qt.QTableWidgetItem("%s" % (file_info1.f_name)))
            self.tableWidget.setItem(i, 1, Qt.QTableWidgetItem("%s" % (file_info1.f_no)))
            self.tableWidget.setItem(i, 2, Qt.QTableWidgetItem("%s" % (file_info1.f_type)))
            self.tableWidget.setItem(i, 3, Qt.QTableWidgetItem("%s" % (file_info1.SID)))
            self.tableWidget.setItem(i, 4, Qt.QTableWidgetItem(
                "%s" % (file_info1.blk_sum * file_info1.blk_size / 1024 / 1024)))
            self.tableWidget.setItem(i, 5, Qt.QTableWidgetItem("%s" % (file_info1.blk_sum)))
            self.tableWidget.setItem(i, 6, Qt.QTableWidgetItem("%s" % (file_info1.blk_size)))
            self.tableWidget.setItem(i, 7, Qt.QTableWidgetItem("%s" % (file_info1.version)))
            self.tableWidget.setItem(i, 8, Qt.QTableWidgetItem("%s" % (endian[file_info1.endian])))
            self.tableWidget.setItem(i, 9, Qt.QTableWidgetItem("%s" % (file_info1.DBID)))

    # 开始解析
    def unload(self):
        self.tabWidget.setCurrentIndex(1)  # 切换标签
        self.file_data = self.ora.unload_db(self.file_infos)  # 解析 ********
        self.showtree()

    def showtree(self):
        sid = self.file_infos[0].SID
        Item_db = QtWidgets.QTreeWidgetItem(self.treeWidget1)  # 根节 库名/用户名
        Item_db.setText(0, '%s' % sid)
        icon_db = QtGui.QIcon()
        icon_db.addPixmap(QtGui.QPixmap("./icons/db.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Item_db.setIcon(0, icon_db)  # 设置图标
        Item_db.setExpanded(True)  # db结点展开

        icon_user = QtGui.QIcon()
        icon_user.addPixmap(QtGui.QPixmap("./icons/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Item_data = QtWidgets.QTreeWidgetItem(Item_db)  # 父节 用户名
        Item_data.setText(0, 'data_file')
        Item_data.setIcon(0, icon_user)  # 设置图标
        Item_redo = QtWidgets.QTreeWidgetItem(Item_db)  # 父节 用户名
        Item_redo.setText(0, 'redo_file')
        Item_redo.setIcon(0, icon_user)  # 设置图标
        Item_temp = QtWidgets.QTreeWidgetItem(Item_db)  # 父节 用户名
        Item_temp.setText(0, 'temp_file')
        Item_temp.setIcon(0, icon_user)  # 设置图标
        Item_db_info = QtWidgets.QTreeWidgetItem(Item_db)  # 父节 用户名
        Item_db_info.setText(0, 'db_info')
        Item_db_info.setIcon(0, icon_user)  # 设置图标

    # tree 的鼠标左键
    def showSelected(self):
        item = self.treeWidget1.currentItem()
        par = item.text(0)
        self.file_info = []
        if 'data_file' == par:
            for i in range(len(self.file_data)):
                if self.file_data[i].f_type == 4:
                    self.file_info.append(self.file_data[i])
        if 'redo_file' == par:
            for i in range(len(self.file_data)):
                if self.file_data[i].f_type == 3:  # and self.file_data[i].flags&2!=10
                    self.file_info.append(self.file_data[i])
        if 'temp_file' == par:
            for i in range(len(self.file_data)):
                if self.file_data[i].f_type == 7:
                    self.file_info.append(self.file_data[i])
        # if 'db_info' == par:
        #     for i in range(len(self.file_data)):
        #         if self.file_data[i].f_type == 3:
        #             self.file_info.append(self.file_data[i])
        self.tab_show(self.file_info)

    # table2
    def tab_show(self, data):
        self.tabWidget.setCurrentIndex(1)  # 初始显示的标签索引
        self.tableWidget2.setAlternatingRowColors(True)  # 隔行变色
        self.tableWidget2.setColumnCount(8)
        self.tableWidget2.setRowCount(len(data))
        header = ['文件号', '文件名', 'blk_size', 'blk_sum', '文件大小(B)', 'version', '创建时间', '修改时间']
        self.tableWidget2.setHorizontalHeaderLabels(header)
        self.tableWidget2.setColumnWidth(0, 50);
        self.tableWidget2.setColumnWidth(1, 200);
        self.tableWidget2.setColumnWidth(2, 60)
        self.tableWidget2.setColumnWidth(3, 60);
        self.tableWidget2.setColumnWidth(4, 80);
        self.tableWidget2.setColumnWidth(5, 60)

        for i in range(len(data)):
            self.tableWidget2.setRowHeight(i, 20)
            self.tableWidget2.setItem(i, 0, Qt.QTableWidgetItem("%s" % data[i].f_no))
            self.tableWidget2.setItem(i, 1, Qt.QTableWidgetItem("%s" % data[i].f_name))
            self.tableWidget2.setItem(i, 2, Qt.QTableWidgetItem("%s" % (data[i].blk_size)))
            self.tableWidget2.setItem(i, 3, Qt.QTableWidgetItem("%s" % (data[i].blk_sum)))
            self.tableWidget2.setItem(i, 4, Qt.QTableWidgetItem("%s" % data[i].blk_size))
            self.tableWidget2.setItem(i, 5, Qt.QTableWidgetItem("%s" % data[i].blk_size))
            self.tableWidget2.setItem(i, 6, Qt.QTableWidgetItem("%s" % data[i].blk_size))

    def selectall(self):
        self.tableWidget2.selectAll()  # 全选

    def notselect(self):
        self.tableWidget2.clearSelection()  # 清除选择

    def closeEvent(self, e):
        e.accept()
        # if self.file_infos == []:
        #     e.accept()
        # else:
        #     ret = QtWidgets.QMessageBox.question(self,"Question",self.tr(" 是否确定要退出程序 ?\t"),
        #         QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel,QtWidgets.QMessageBox.Ok)
        #     if ret == QtWidgets.QMessageBox.Ok:
        #         e.accept()
        #     else: e.ignore()

    def helpAbout(self):  # 测试用
        QtWidgets.QMessageBox.about(self, "About", "\tctl unload  \t\n")


class myui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myui, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = myui()
    ui.show()
    sys.exit(app.exec_())
