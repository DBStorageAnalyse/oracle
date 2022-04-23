# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys, random, hashlib, os  # ,gc
import asm_unload


# import objgraph

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
        self.tab_1 = QtWidgets.QWidget()
        self.tabWidget.setMovable(1)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_1)
        self.groupBox = QtWidgets.QGroupBox(self.tab_1)
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
        self.progressBar_1 = QtWidgets.QProgressBar(self.tab_1)
        self.progressBar_1.setMaximumSize(QtCore.QSize(16777215, 4))  # 进度条宽度
        self.progressBar_1.setProperty("value", 0)
        self.progressBar_1.setTextVisible(False)
        self.gridLayout_2.addWidget(self.progressBar_1, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.tab_1)  # file table
        self.gridLayout_2.addWidget(self.tableWidget, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.progressBar = QtWidgets.QProgressBar(self.tab_2)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 4))  # 进度条宽度
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.gridLayout_3.addWidget(self.progressBar, 2, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.tab_2)
        self.splitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter.setLineWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(4)  # 分隔条的 宽度
        self.treeWidget1 = QtWidgets.QTreeWidget(self.splitter)  # 标签2的 tree
        self.treeWidget1.setHeaderHidden(1)
        self.tableWidget2 = QtWidgets.QTableWidget(self.splitter)  # 标签2的 表2
        self.tableWidget2.setColumnCount(0)
        self.tableWidget2.setRowCount(0)
        self.gridLayout_3.addWidget(self.splitter, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.splitter.setStretchFactor(1, 2)  # 设置显示比例

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
        self.label_2.setStyleSheet(
            'QLabel{border:2px groove grey; border-radius:5px;border-style: outset;background-color:%s}' % self.color.name())
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_5)  # 关于->教程
        self.pushButton_8.setGeometry(QtCore.QRect(200, 292, 142, 30))
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_5)  # 关于->注册
        self.pushButton_9.setGeometry(QtCore.QRect(343, 292, 143, 30))
        style_1 = "QPushButton:hover{background-color:gray;}""QPushButton:pressed{border-style: inset;}" \
                  "QPushButton{border:2px groove grey; border-radius:2px;border-style: outset;background-color:%s;}" % self.color.name()
        self.pushButton_8.setStyleSheet(style_1)
        self.pushButton_9.setStyleSheet(style_1)

        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 831, 23))
        MainWindow.setMenuBar(self.menubar)

        self.expdbAction = QtWidgets.QAction(MainWindow)  # expdbAction =================
        self.expdbAction.triggered.connect(MainWindow.helpAbout)
        self.selectallAction = QtWidgets.QAction(MainWindow)  # selectallAction =================
        self.selectallAction.triggered.connect(MainWindow.selectall)
        self.notselectAction = QtWidgets.QAction(MainWindow)  # notselectAction =================
        self.notselectAction.triggered.connect(MainWindow.notselect)

        self.expallAction = QtWidgets.QAction(MainWindow)  # expallAction =================
        self.expinfoAction = QtWidgets.QAction(MainWindow)  # expinfoAction =================
        self.expfileAction = QtWidgets.QAction(MainWindow)  # expfileAction =================
        self.expfileinfoAction = QtWidgets.QAction(MainWindow)  # expfileAction =================

        self.expallAction.triggered.connect(self.expall)
        self.expinfoAction.triggered.connect(self.expallinfo)
        self.expfileAction.triggered.connect(self.expfile)
        self.expfileinfoAction.triggered.connect(self.expfileinfo)

        self.pushButton.clicked.connect(self.fileOpen)  # 添加文件
        self.pushButton_2.clicked.connect(self.fileDel)  # 移除文件
        self.pushButton_3.clicked.connect(self.allDel)  # 清空列表
        self.pushButton_4.clicked.connect(self.asm_unload)  # 开始解析
        self.pushButton_5.clicked.connect(self.stop_unload)  # 停止解析
        self.pushButton_8.clicked.connect(self.help)  # 教程
        self.pushButton_9.clicked.connect(self.regist)  # 注册
        self.treeWidget1.itemClicked.connect(self.showSelected)  # 左键单击事件
        self.treeWidget1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # tree 的 右键菜单开关
        self.treeWidget1.customContextMenuRequested['QPoint'].connect(self.on_treeWidget1)  # tree 的右键菜单
        self.tableWidget2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # table 右键菜单开关
        self.tableWidget2.customContextMenuRequested['QPoint'].connect(self.on_tableWidget2)  # table 右键菜单

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)  # 初始显示的标签索引
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ASM 解析工具  V%s" % self.version))
        self.pushButton.setText(_translate("MainWindow", "添加文件"))
        self.pushButton_2.setText(_translate("MainWindow", "移出文件"))
        self.pushButton_3.setText(_translate("MainWindow", "清空列表"))
        self.pushButton_4.setText(_translate("MainWindow", "开始解析"))
        self.pushButton_5.setText(_translate("MainWindow", "停止解析"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "选择源盘"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "解析ASM"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "HEX"))
        self.label.setText(_translate("MainWindow", ""))
        about = 'ASM Unload V%s\t\n\n\n解析ASM磁盘,获取文件\n支持10g/11g/12c版本的ASM\n支持解析大、小端平台的ASM\n此版本可运行在64位Windows系统中\n注册单次有效,程序重启需重新获取注册码注册' % self.version
        self.label_2.setText(_translate("MainWindow", "%s" % about))
        self.pushButton_8.setText(_translate("MainWindow", "教程"))
        self.pushButton_9.setText(_translate("MainWindow", "注册"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "高级信息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "关于"))

        self.expdbAction.setText(_translate("MainWindow", "expdb"))  # 菜单栏  子菜单
        self.expallAction.setText(_translate("MainWindow", "expall"))  # 菜单栏  子菜单
        self.expinfoAction.setText(_translate("MainWindow", "expinfo"))  # 菜单栏  子菜单
        self.selectallAction.setText(_translate("MainWindow", "selectall"))  # 菜单栏  子菜单
        self.notselectAction.setText(_translate("MainWindow", "notselect"))  # 菜单栏  子菜单
        self.expfileAction.setText(_translate("MainWindow", "expfile"))  # 菜单栏  子菜单
        self.expfileinfoAction.setText(_translate("MainWindow", "expfileinfo"))  # 菜单栏  子菜单

    def init(self):
        self.version = '1.6.0'
        self.disks = []
        self.asm = asm_unload.ASM()
        self.out_file = 0
        self.reg = 0

    def fileOpen(self):
        fn, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Files...", None, "ASM-Files (*);;All Files (*)")
        disks = self.asm.disk_init(fn)
        for disk in disks:
            self.disks.append(disk)
        if len(self.disks) == 0:
            return
        self.disks.sort(key=lambda x: (x.grpname, x.dsknum))  # 排序 磁盘和磁盘组。多关键字排序
        self.disk_tab()  # 显示磁盘信息
        self.pushButton_4.setDisabled(0)

    def fileDel(self):
        aa1 = self.tableWidget.currentRow()
        if len(self.disks) == 0:
            return
        del self.disks[aa1]
        self.disk_tab()

    def allDel(self):
        self.disks = []
        self.disk_tab()
        self.pushButton_4.setDisabled(1)

    def stop_unload(self):
        if self.out_file != 0 and self.out_file.is_alive() == True:
            QtWidgets.QMessageBox.about(self, "提示", "停止解析 ... \n")

    # 磁盘列表
    def disk_tab(self):
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setAlternatingRowColors(True)  # 隔行变色
        self.tableWidget.setRowCount(len(self.disks))
        # info 列是 大小端和 AU大小(M), 兼容版本列可以去掉
        header = ['file_path', '磁盘号', '磁盘名', '磁盘组名', 'info', '磁盘大小(G)', '兼容版本', '状态', '冗余级别', '创建时间', '挂载时间']
        self.tableWidget.setHorizontalHeaderLabels(header)
        self.tableWidget.setColumnWidth(1, 50)  # 设置固定列宽
        self.tableWidget.setColumnWidth(3, 60);
        self.tableWidget.setColumnWidth(4, 50);
        self.tableWidget.setColumnWidth(5, 80)
        self.tableWidget.setColumnWidth(6, 70);
        self.tableWidget.setColumnWidth(7, 40);
        self.tableWidget.setColumnWidth(8, 60)
        self.tableWidget.setColumnWidth(9, 126);
        self.tableWidget.setColumnWidth(10, 126)
        for i in range(len(self.disks)):
            file_info1 = self.disks[i]
            self.tableWidget.setRowHeight(i, 20)
            self.tableWidget.setItem(i, 0, Qt.QTableWidgetItem("%s" % (file_info1.file.name)))
            self.tableWidget.setItem(i, 1, Qt.QTableWidgetItem("%s" % (file_info1.dsknum)))
            self.tableWidget.setItem(i, 2, Qt.QTableWidgetItem("%s" % (file_info1.dskname)))
            self.tableWidget.setItem(i, 3, Qt.QTableWidgetItem("%s" % (file_info1.grpname)))
            self.tableWidget.setItem(i, 4, Qt.QTableWidgetItem(
                "%s" % (file_info1.frm + ', ' + str(int(file_info1.ausize / 1024 / 1024)) + 'M')))
            self.tableWidget.setItem(i, 5, Qt.QTableWidgetItem("%s" % (file_info1.dsksize)))
            self.tableWidget.setItem(i, 6, Qt.QTableWidgetItem("%s" % (file_info1.compat)))
            self.tableWidget.setItem(i, 7, Qt.QTableWidgetItem("%s" % (file_info1.hdrsts)))
            self.tableWidget.setItem(i, 8, Qt.QTableWidgetItem("%s" % (file_info1.grptyp)))
            self.tableWidget.setItem(i, 9, Qt.QTableWidgetItem("%s" % (file_info1.crestmp)))
            self.tableWidget.setItem(i, 10, Qt.QTableWidgetItem("%s" % (file_info1.mntstmp)))

    # 开始解析ASM
    def asm_unload(self):
        self.tabWidget.setCurrentIndex(1)  # 切换标签
        self.progressBar_1.setProperty("value", 60)
        self.file_data, self.alias_data, self.disk_data = self.asm.asm(self.disks)
        self.progressBar_1.setProperty("value", 100)
        if len(self.file_data) == 0:
            Item_db = QtWidgets.QTreeWidgetItem(self.treeWidget1)  # 根节 库名/用户名
            Item_db.setText(0, '%s' % ('没有取到disk0中的file1,解析终止'))
            return
        if len(self.alias_data) == 0:
            return
        self.asm.disk_file_list(self.disks, self.file_data)  # 磁盘信息存入数据库

        Item_db = QtWidgets.QTreeWidgetItem(self.treeWidget1)  # 根节 库名/用户名
        Item_db.setText(0, '%s' % (self.alias_data[0].name))
        icon_db = QtGui.QIcon()
        icon_db.addPixmap(QtGui.QPixmap("./icons/db.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Item_db.setIcon(0, icon_db)  # 设置图标
        Item_db.setExpanded(True)  # db结点展开
        for i in range(len(self.alias_data)):  # 文件类型
            if self.alias_data[i].level == 2:
                file_name = self.alias_data[i].name
                Item_user = QtWidgets.QTreeWidgetItem(Item_db)  # 父节 用户名
                Item_user.setText(0, '%s' % file_name)
                icon_user = QtGui.QIcon()
                icon_user.addPixmap(QtGui.QPixmap("./icons/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                Item_user.setIcon(0, icon_user)  # 设置图标
        self.Extend_info()

    # tree 的鼠标左键
    def showSelected(self):
        item = self.treeWidget1.currentItem()
        par = item.text(0)
        self.file_info = []
        if 'metafile' == par:
            for i in range(len(self.file_data)):
                if self.file_data[i].file_no in (1, 2, 6):  # and self.file_data[i].flags&2!=10
                    self.file_info.append(self.file_data[i])
                #    print('file_no:%d,file_name:%s,size: %d'%(self.file_data[i].file_no,par,self.file_data[i].lobytes))
        if 'datafile' == par:
            for i in range(len(self.file_data)):
                if self.file_data[i].fileType not in (3, 1, 6, 13, 15):  # and self.file_data[i].flags&2!=10
                    self.file_info.append(self.file_data[i])
                #    print('file_no:%d,file_name:%s,size: %d'%(self.file_data[i].file_no,par,self.file_data[i].lobytes))
        if 'controlfile' == par:
            for i in range(len(self.file_data)):
                if self.file_data[i].fileType == 1:
                    self.file_info.append(self.file_data[i])
                #    print('file_no:%d,file_name:%s,size: %d'%(self.file_data[i].file_no,par,self.file_data[i].lobytes))
        if 'onlinelog' == par:
            for i in range(len(self.file_data)):
                if self.file_data[i].fileType == 3:
                    self.file_info.append(self.file_data[i])
                #    print('file_no:%d,file_name:%s,size: %d'%(self.file_data[i].file_no,par,self.file_data[i].lobytes))
        if 'tempfile' == par:
            for i in range(len(self.file_data)):
                if self.file_data[i].fileType == 6:
                    self.file_info.append(self.file_data[i])
                #    print('file_no:%d,file_name:%s,size: %d'%(self.file_data[i].file_no,par,self.file_data[i].lobytes))
        if 'parameterfile' == par:
            for i in range(len(self.file_data)):
                if self.file_data[i].fileType == 13:
                    self.file_info.append(self.file_data[i])
                #    print('file_no:%d,file_name:%s,size: %d'%(self.file_data[i].file_no,par,self.file_data[i].lobytes))
        self.tab_show(self.file_info)

    # table2
    def tab_show(self, data):
        self.tabWidget.setCurrentIndex(1)  # 初始显示的标签索引
        self.tableWidget2.setAlternatingRowColors(True)  # 隔行变色
        self.tableWidget2.setColumnCount(8)
        self.tableWidget2.setRowCount(len(data))
        header = ['磁盘组', '文件号', '文件名', '文件大小(B)', '大小(G)', '扩展数量', '创建时间', '修改时间']
        self.tableWidget2.setHorizontalHeaderLabels(header)
        self.tableWidget2.setColumnWidth(0, 44)
        self.tableWidget2.setColumnWidth(1, 44)  # 设置固定列宽
        self.tableWidget2.setColumnWidth(2, 180)
        self.tableWidget2.setColumnWidth(3, 90)
        self.tableWidget2.setColumnWidth(4, 60)
        self.tableWidget2.setColumnWidth(5, 60)
        for i in range(len(data)):
            self.tableWidget2.setRowHeight(i, 20)
            self.tableWidget2.setItem(i, 0, Qt.QTableWidgetItem("%s" % '0'))
            self.tableWidget2.setItem(i, 1, Qt.QTableWidgetItem("%s" % data[i].file_no))
            self.tableWidget2.setItem(i, 2, Qt.QTableWidgetItem("%s" % data[i].name))
            self.tableWidget2.setItem(i, 3,
                                      Qt.QTableWidgetItem("%s" % (data[i].lobytes + data[i].hibytes * 4294967296)))
            self.tableWidget2.setItem(i, 4, Qt.QTableWidgetItem(
                "%7.3f" % ((data[i].lobytes + data[i].hibytes * 4294967296) / 1024.0 / 1024.0 / 1024.0)))
            self.tableWidget2.setItem(i, 5, Qt.QTableWidgetItem("%s" % data[i].xtntcnt))
            self.tableWidget2.setItem(i, 6, Qt.QTableWidgetItem("%s" % data[i].crets_hi))
            self.tableWidget2.setItem(i, 7, Qt.QTableWidgetItem("%s" % data[i].modts_hi))

    #  tree的右键菜单
    def on_treeWidget1(self):  # on_treeWidget1_customContextMenuRequested
        menu_tab0 = QtWidgets.QMenu(self)  # db 层
        menu_tab0.addAction(self.expdbAction)
        menu_tab1 = QtWidgets.QMenu(self)  # 类型层
        menu_tab1.addAction(self.expallAction)
        menu_tab1.addAction(self.expinfoAction)
        item = self.treeWidget1.currentItem()
        if item != None:
            if item.parent() == None:
                menu_tab0.exec_(QtGui.QCursor.pos())
            else:
                menu_tab1.exec_(QtGui.QCursor.pos())

    # table2 的右键菜单
    def on_tableWidget2(self, pos):
        menu_1 = QtWidgets.QMenu(self)
        menu_1.addAction(self.expfileAction)
        menu_1.addAction(self.expfileinfoAction)
        menu_1.addAction(self.selectallAction)
        menu_1.addAction(self.notselectAction)
        item = self.tableWidget2.currentItem()
        if item != None:
            menu_1.exec_(QtGui.QCursor.pos())

    def selectall(self):
        self.tableWidget2.selectAll()  # 全选

    def notselect(self):
        self.tableWidget2.clearSelection()  # 清除选择

    # 导出选中文件
    def expfile(self):
        if self.reg == 0:
            self.register()
            return
        items = self.tableWidget2.selectedItems()
        row_no = []
        for item1 in items:
            aa0 = item1.row()
            row_no.append(aa0)
        new_row_no = list(set(row_no))  # 去重
        new_row_no.sort(key=row_no.index)  # 排序
        file_nos = []
        for aa1 in new_row_no:
            aa2 = self.tableWidget2.item(aa1, 1).text()
            file_nos.append(aa2)
        file_in = []
        for file_no in file_nos:
            for file in self.file_info:
                if file.file_no == int(file_no):
                    file_in.append(file)
        if self.out_file != 0 and self.out_file.is_alive() == True:
            QtWidgets.QMessageBox.about(self, "提示", "有文件正在导出,请等待导出完成 ...\t\n")
            return
        out_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory...", None)  # 选择文件夹对话框
        if out_path == '':
            return
        self.out_file = asm_unload.OUT_FILE(self.disks, file_in, out_path, '')
        self.progressBar.setProperty("value", 50)
        self.out_file.start()
        if self.out_file.isAlive == True:
            self.progressBar.setProperty("value", 50)
        elif self.out_file.isAlive == False:
            self.progressBar.setProperty("value", 100)

    # 导出 选中文件的指针信息到db
    def expfileinfo(self):  # 导出所有的此类文件
        if self.reg == 0:
            self.register()
            return
        items = self.tableWidget2.selectedItems()
        row_no = []
        for item1 in items:
            aa0 = item1.row()
            row_no.append(aa0)
        new_row_no = list(set(row_no))  # 去重
        new_row_no.sort(key=row_no.index)  # 排序
        file_nos = []
        for aa1 in new_row_no:
            aa2 = self.tableWidget2.item(aa1, 1).text()
            file_nos.append(aa2)
        file_in = []
        for file_no in file_nos:
            for file in self.file_info:
                if file.file_no == int(file_no):
                    file_in.append(file)

        if self.out_file != 0 and self.out_file.is_alive() == True:
            QtWidgets.QMessageBox.about(self, "提示", "有文件正在导出,请等待导出完成 ...\t\n")
            return
        out_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select DB Directory...", None)  # 选择文件夹对话框
        if out_path == '':
            return
        db = out_path + '/out.db'
        self.out_file = asm_unload.OUT_FILE(self.disks, file_in, out_path, db)
        self.out_file.start()

    # 导出所有的此类文件
    def expall(self):  # 导出所有的此类文件
        if self.reg == 0:
            self.register()
            return
        if self.out_file != 0 and self.out_file.is_alive() == True:
            QtWidgets.QMessageBox.about(self, "提示", "有文件正在导出,请等待导出完成 ...\t\n")
            return
        out_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory...", None)  # 选择文件夹对话框
        if out_path == '':
            return
        self.out_file = asm_unload.OUT_FILE(self.disks, self.file_info, out_path, '')
        self.progressBar.setProperty("value", 20)
        self.out_file.start()

        if self.out_file.is_alive() == True:
            self.progressBar.setProperty("value", 50)
        else:
            self.progressBar.setProperty("value", 100)

    # 导出所有的此类文件的指针信息到db
    def expallinfo(self):  # 导出所有的此类文件
        if self.reg == 0:
            self.register()
            return
        if self.out_file != 0 and self.out_file.is_alive() == True:
            QtWidgets.QMessageBox.about(self, "提示", "有文件正在导出,请等待导出完成 ...\t\n")
            return
        out_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select DB Directory...", None)  # 选择文件夹对话框
        if out_path == '':
            return
        db = out_path + '/out.db'
        #   db = r'.\out.db'
        self.out_file = asm_unload.OUT_FILE(self.disks, self.file_info, out_path, db)
        self.out_file.start()

    def progress(self, progress_val):
        self.progressBar.setValue(progress_val)

    def Extend_info(self):  # 测试用
        self.text_1.append('磁盘组名称:%s ,数据库名称:%s\n' % (self.disks[0].grpname, self.alias_data[0].name))
        ss = '缺盘号：'
        for disk_data in self.disk_data:
            dd = 0;
            for disk in self.disks:
                if disk_data.dsknum == disk.dsknum:
                    dd = 1;
                    break
            if dd == 0:
                ss = ss + str(disk_data.dsknum) + ','
        self.text_1.append(
            '磁盘组中 磁盘总数：%d,缺盘数：%d, %s\n' % (len(self.disk_data), len(self.disk_data) - len(self.disks), ss))

        all_size = 0;
        aa = 0
        for file_data in self.file_data:
            if file_data.file_no < 100:
                aa += 1
                continue
            all_size += (file_data.lobytes + file_data.hibytes * 4294967296) / 1024.0 / 1024.0 / 1024.0
        self.text_1.append('磁盘组中 文件总数量：%d,总大小：%d G\n' % (len(self.file_data) - aa, all_size))

        memm_size = sys.getsizeof(self.file_data) + sys.getsizeof(self.alias_data) + sys.getsizeof(
            self.disk_data) + sys.getsizeof(self.disks)  # 占用内存大小
        memm_size = memm_size / 1024.0
        #  print('内存占用：%d,%d,%d,%d \n'%(sys.getsizeof(self.file_data),sys.getsizeof(self.alias_data),sys.getsizeof(self.disk_data),sys.getsizeof(self.disks)))
        self.text_1.append('内存占用：%.2fK\n' % (memm_size))

    def closeEvent(self, e):
        if self.disks == []:
            e.accept()
        else:
            ret = QtWidgets.QMessageBox.question(self, "Question", self.tr(" 是否确定要退出程序 ?\t"),
                                                 QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                                 QtWidgets.QMessageBox.Ok)
            if ret == QtWidgets.QMessageBox.Ok:
                e.accept()
            else:
                e.ignore()

    def regist(self):
        if self.reg == 0:
            self.register()
        else:
            QtWidgets.QMessageBox.about(self.reg_widget, "注册", "已经注册成功  \t\t\n")

    def help(self):
        os.popen(r'oracle_unload_dbf instructions(使用说明书).pdf')
        return

    def register(self):
        # 弹出导出配置界面
        self.reg_widget = QtWidgets.QWidget()
        self.reg_widget.setGeometry(QtCore.QRect(385, 100, 500, 180))
        self.reg_widget.setWindowTitle('注册')
        self.label_20 = QtWidgets.QLabel(self.reg_widget)
        self.label_20.setGeometry(QtCore.QRect(10, 20, 50, 23))
        self.label_20.setText('原始码')
        self.label_21 = QtWidgets.QLabel(self.reg_widget)
        self.label_21.setGeometry(QtCore.QRect(10, 60, 50, 23))
        self.label_21.setText('注册码')
        self.lineEdit_20 = QtWidgets.QLineEdit(self.reg_widget)
        self.lineEdit_20.setGeometry(QtCore.QRect(80, 20, 400, 23))
        num1 = random.randint(1000000000, 99999999999)
        md5 = hashlib.md5()
        md5.update(str(num1).encode())
        reg1 = md5.hexdigest()
        self.lineEdit_20.setText(reg1)
        self.lineEdit_20.setReadOnly(1)
        self.lineEdit_21 = QtWidgets.QLineEdit(self.reg_widget)
        self.lineEdit_21.setGeometry(QtCore.QRect(80, 60, 400, 23))
        self.label_22 = QtWidgets.QLabel(self.reg_widget)
        self.label_22.setGeometry(QtCore.QRect(10, 90, 500, 23))
        self.label_22.setText('* 发送原始码,获取注册码进行注册. 注册单次有效,程序重启需重新获取注册码注册！')
        self.pushButton_20 = QtWidgets.QPushButton(self.reg_widget)
        self.pushButton_20.setGeometry(QtCore.QRect(80, 130, 160, 23))
        self.pushButton_20.setText('注册')
        self.pushButton_21 = QtWidgets.QPushButton(self.reg_widget)
        self.pushButton_21.setGeometry(QtCore.QRect(300, 130, 100, 23))
        self.pushButton_21.setText('取消')
        self.reg_widget.show()
        self.pushButton_20.clicked.connect(self.register1)  # 怎么获取返回值
        self.pushButton_21.clicked.connect(self.register2)

    def register1(self):
        num1 = self.lineEdit_20.text()  # 随机码
        num2 = self.lineEdit_21.text()  # 验证码
        md5 = hashlib.md5()
        reg = str('105946*')
        md5.update(reg.encode())
        reg0 = md5.hexdigest()
        md5.update(reg0.encode())
        reg0 = md5.hexdigest()
        md5.update(num1.encode())
        reg1 = md5.hexdigest()
        sha1 = hashlib.sha1()
        sha1.update(str(reg0 + reg1).encode())
        reg2 = sha1.hexdigest()
        if num2 == reg2:
            self.reg = 1
            QtWidgets.QMessageBox.about(self.reg_widget, "注册", "注册成功  \t\t\n")
            self.reg_widget.close()
        else:
            QtWidgets.QMessageBox.about(self.reg_widget, "注册", "注册码错误，注册失败  \t\n")

    def register2(self):
        self.reg_widget.close()

    def helpAbout(self):  # 测试用
        QtWidgets.QMessageBox.about(self, "About", "\tASM  \t\n")


class myui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myui, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = myui()
    ui.show()
    sys.exit(app.exec_())
