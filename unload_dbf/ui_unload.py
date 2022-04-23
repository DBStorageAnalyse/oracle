# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys, random, hashlib, os, time
import unload_dbf  # , cx_Oracle


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.init()
        MainWindow.resize(860, 560)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./icons/db.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)  # 设置边缘宽度
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_1 = QtWidgets.QWidget()
        self.tabWidget.setMovable(1)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_1)
        self.groupBox = QtWidgets.QGroupBox(self.tab_1)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 80))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 80))
        self.groupBox.setTitle("")
        self.color = QtGui.QColor(150, 150, 150)  # 颜色(190, 180, 150) (140, 140, 140)　(190, 200, 200)
        self.groupBox.setStyleSheet(
            'QGroupBox{border: 2px groove grey; border-radius:5px;border-style: outset;background-color:%s}' % self.color.name())  # 利用样式
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
        self.tableWidget = QtWidgets.QTableWidget(self.tab_1)  # file table
        self.gridLayout_2.addWidget(self.tableWidget, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()

        self.progressBar = QtWidgets.QProgressBar(self.tab_1)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 30))  # 进度条1宽度
        self.progressBar.setTextVisible(False)
        self.lable_1 = QtWidgets.QLabel(self.progressBar)
        self.lable_1.setFixedSize(QtCore.QSize(500, 20))
        self.gridLayout_2.addWidget(self.progressBar, 3, 0, 1, 1)
        self.gridLayout_2.setContentsMargins(2, 4, 2, 0)  # 设置边缘宽度

        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)  # 设置边缘宽度
        self.progressBar_2 = QtWidgets.QProgressBar(self.tab_1)
        self.progressBar_2.setMaximumSize(QtCore.QSize(16777215, 4))  # 进度条2宽度
        self.progressBar_2.setProperty("value", 100)
        self.progressBar_2.setTextVisible(False)
        self.gridLayout_3.addWidget(self.progressBar_2, 2, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.tab_2)
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
            'QLabel{border:2px groove grey; border-radius:5px;border-style: outset;background-color:%s}' % self.color.name())  #
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
        self.expuser_2_db_Action = QtWidgets.QAction(MainWindow)  # expallAction =================
        self.expuser_2_db_Action.triggered.connect(MainWindow.expuser_2_db)
        self.expinfo_Action = QtWidgets.QAction(MainWindow)  # expinfoAction =================
        self.expinfo_Action.triggered.connect(MainWindow.expuser_info)
        self.exptab_2_db_Action = QtWidgets.QAction(MainWindow)  # expinfoAction =================
        self.exptab_2_db_Action.triggered.connect(MainWindow.exptab_2_db)
        self.exptab_2_sql_Action = QtWidgets.QAction(MainWindow)  # expinfoAction =================
        self.exptab_2_sql_Action.triggered.connect(MainWindow.exptab_2_sql)
        self.selectallAction = QtWidgets.QAction(MainWindow)  # selectallAction =================
        self.selectallAction.triggered.connect(MainWindow.selectall)
        self.notselectAction = QtWidgets.QAction(MainWindow)  # notselectAction =================
        self.notselectAction.triggered.connect(MainWindow.notselect)

        self.pushButton.clicked.connect(self.fileOpen)  # 添加文件
        self.pushButton_2.clicked.connect(self.fileDel)  # 移除文件
        self.pushButton_3.clicked.connect(self.allDel)  # 清空列表
        self.pushButton_4.clicked.connect(self.unload)  # 开始解析
        self.pushButton_5.clicked.connect(self.db_link)  # 停止解析  db_link    helpAbout
        self.pushButton_8.clicked.connect(self.help)  # 教程
        self.pushButton_9.clicked.connect(self.regist)  # 注册
        self.treeWidget1.itemClicked.connect(self.showSelected)  # 单击事件
        self.treeWidget1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # tree 的 右键菜单开关
        self.treeWidget1.customContextMenuRequested['QPoint'].connect(self.on_treeWidget1)  # tree 的右键菜单
        self.tableWidget2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # table 右键菜单开关
        self.tableWidget2.customContextMenuRequested['QPoint'].connect(self.on_tableWidget2)  # table 右键菜单

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)  # 初始显示的标签索引
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "北亚 Oracle 解析工具  V%s" % self.version))
        self.pushButton.setText(_translate("MainWindow", "添加文件"))
        self.pushButton_2.setText(_translate("MainWindow", "移出文件"))
        self.pushButton_3.setText(_translate("MainWindow", "清空列表"))
        self.pushButton_4.setText(_translate("MainWindow", "开始解析"))
        self.pushButton_5.setText(_translate("MainWindow", "停止解析"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "选择文件"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "解析文件"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "HEX"))
        self.label.setText(_translate("MainWindow", ""))
        about = 'Oracle Unload V%s\t\n\n\n解析Oracle 数据文件\n支持10g/11g/12c各版本的DBF\n支持解析大、小端平台的DBF\n此版本只能运行在64位Windows系统中\n注册单次有效,程序重启需重新获取注册码注册' % self.version
        self.label_2.setText(_translate("MainWindow", "%s" % about))
        self.pushButton_8.setText(_translate("MainWindow", "教程"))
        self.pushButton_9.setText(_translate("MainWindow", "注册"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "高级信息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "关于"))

        self.expdbAction.setText(_translate("MainWindow", "expdb"))  # 菜单栏  子菜单
        self.expuser_2_db_Action.setText(_translate("MainWindow", "expuser_2_db"))  # 菜单栏  子菜单
        self.expinfo_Action.setText(_translate("MainWindow", "expuser_info"))  # 菜单栏  子菜单
        self.exptab_2_db_Action.setText(_translate("MainWindow", "exptab_2_db"))  # 菜单栏  子菜单
        self.exptab_2_sql_Action.setText(_translate("MainWindow", "exptab_2_sql"))  # 菜单栏  子菜单
        self.selectallAction.setText(_translate("MainWindow", "selectall"))  # 菜单栏  子菜单
        self.notselectAction.setText(_translate("MainWindow", "notselect"))  # 菜单栏  子菜单
        self.exptab_2_db_Action.setText(_translate("MainWindow", "exptab_2_db"))  # 菜单栏  子菜单

    def init(self):
        self.version = '1.9.0'
        self.file_infos = []
        self.ora = unload_dbf.Unload_DB(self)
        self.reg = 1  # 默认是注册了的

    def fileOpen(self):
        fn, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Files...", None,
                                                       "All Files (*);;DB-Files (*.dbf *.ora)")
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
        self.tableWidget.setColumnCount(13)
        self.tableWidget.setAlternatingRowColors(True)  # 隔行变色
        self.tableWidget.setRowCount(len(self.file_infos))
        header = ['file_path', 'file#', 'type', 'dbid', 'db_name', 'f_size(M)', 'blk_sum', 'blk_size', 'ts#', 'ts_name',
                  'version', 'endian', 'big_ts']
        self.tableWidget.setHorizontalHeaderLabels(header)
        self.tableWidget.setColumnWidth(0, 160);
        self.tableWidget.setColumnWidth(1, 40);
        self.tableWidget.setColumnWidth(2, 36);
        self.tableWidget.setColumnWidth(3, 40);
        self.tableWidget.setColumnWidth(4, 70);
        self.tableWidget.setColumnWidth(5, 70);
        self.tableWidget.setColumnWidth(6, 70);
        self.tableWidget.setColumnWidth(7, 60);
        self.tableWidget.setColumnWidth(8, 30);
        self.tableWidget.setColumnWidth(9, 80);
        self.tableWidget.setColumnWidth(10, 70);
        self.tableWidget.setColumnWidth(11, 50);
        self.tableWidget.setColumnWidth(12, 50);
        for i in range(len(self.file_infos)):
            endian = {'<': 'little', '>': 'big'};
            big_ts = {0: 'no', 1: 'yes'}
            file_info1 = self.file_infos[i]
            self.tableWidget.setRowHeight(i, 20)
            self.tableWidget.setItem(i, 0, Qt.QTableWidgetItem("%s" % (file_info1.f_name)))
            self.tableWidget.setItem(i, 1, Qt.QTableWidgetItem("%s" % (file_info1.f_no)))
            self.tableWidget.setItem(i, 2, Qt.QTableWidgetItem("%s" % (file_info1.f_type)))
            self.tableWidget.setItem(i, 3, Qt.QTableWidgetItem("%s" % (file_info1.DBID)))
            self.tableWidget.setItem(i, 4, Qt.QTableWidgetItem("%s" % (file_info1.SID)))
            self.tableWidget.setItem(i, 5, Qt.QTableWidgetItem(
                "%s" % (file_info1.blk_sum * file_info1.blk_size / 1024 / 1024)))
            self.tableWidget.setItem(i, 6, Qt.QTableWidgetItem("%s" % (file_info1.blk_sum)))
            self.tableWidget.setItem(i, 7, Qt.QTableWidgetItem("%s" % (file_info1.blk_size)))
            self.tableWidget.setItem(i, 8, Qt.QTableWidgetItem("%s" % (file_info1.ts_id)))
            self.tableWidget.setItem(i, 9, Qt.QTableWidgetItem("%s" % (file_info1.ts_name)))
            self.tableWidget.setItem(i, 10, Qt.QTableWidgetItem("%s" % (file_info1.version)))
            self.tableWidget.setItem(i, 11, Qt.QTableWidgetItem("%s" % (endian[file_info1.endian])))
            self.tableWidget.setItem(i, 12, Qt.QTableWidgetItem("%s" % (big_ts[file_info1.big_ts])))

    # 开始解析
    def unload(self):
        self.ora.file_infos = self.file_infos
        self.ora.start()  # 解析 ********
        self.ora.PUP.connect(self.progressBar.setValue)  # 传递参数
        self.ora.LUP.connect(self.lable_1.setText)
        self.ora.PUP.connect(self.aa_1)  # 判断scan 进程完成，进行下边的操作

    def aa_1(self, press):
        if press == 100:
            time.sleep(1)
            self.tables, self.table_22, self.db1 = self.ora.tables, self.ora.table_22, self.ora.db1
            self.tabWidget.setCurrentIndex(1)  # 切换标签
            self.showtree()

    # 显示数据库对象列表
    def showtree(self):
        data_1 = self.tables  # 表结构数据 （list）
        Item_db = QtWidgets.QTreeWidgetItem(self.treeWidget1)  # 根节 库名/用户名
        Item_db.setText(0, '%s(%s)' % (self.db1.db_name, 0))
        icon_db = QtGui.QIcon()
        icon_db.addPixmap(QtGui.QPixmap("./icons/db.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Item_db.setIcon(0, icon_db)  # 设置图标
        Item_db.setExpanded(True)  # db结点展开
        user_sum = 0
        for user in self.table_22:  # 用户
            user_id = user.col_data2[0]
            if user_id >= 0 and user_id < 10000 and user.col_data2[2] == 1:
                user_sum += 1
                Item_user = QtWidgets.QTreeWidgetItem(Item_db)  # 父节 用户名
                Item_user.setText(0, '%s' % user.col_data2[1])
                icon_user = QtGui.QIcon()
                icon_user.addPixmap(QtGui.QPixmap("./icons/users.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                Item_user.setIcon(0, icon_user)  # 设置图标

                Item_tab = QtWidgets.QTreeWidgetItem(Item_user)  # 表目录
                icon_tab = QtGui.QIcon()
                icon_tab.addPixmap(QtGui.QPixmap("./icons/t1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                Item_tab.setIcon(0, icon_tab)  # 设置图标
                tab_sum = 0
                for table in data_1:  # 用户下的表
                    if table.owner == user_id:
                        Item1 = QtWidgets.QTreeWidgetItem(Item_tab)  # 表名
                        # icon11 = QtGui.QIcon()
                        # icon11.addPixmap(QtGui.QPixmap("./icons/t1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        # Item1.setIcon(0,icon11)         # 设置图标
                        tab_sum += 1;
                        col_sum = 0;
                        index_sum = 0
                        Item2 = QtWidgets.QTreeWidgetItem(Item1)  # 表的列
                        for col in table.col:  # 表的列
                            Item2_1 = QtWidgets.QTreeWidgetItem(Item2)  # 子节 列
                            try:
                                Item2_1.setText(0, '%s' % (col.col_name + ' (' + col.col_type_name + ')'))
                            except KeyError:
                                Item2_1.setText(0, '%s' % (col.col_name + ' (' + 'unkown' + ')'))
                            Item2.addChild(Item2_1)  # 添加子节点
                            col_sum += 1
                        Item2.setText(0, '%s(%s)' % ('columns', col_sum))  # 列名
                        Item3 = QtWidgets.QTreeWidgetItem(Item1)  # 表的索引
                        for index in table.indexes:  # 表的索引
                            Item3_1 = QtWidgets.QTreeWidgetItem(Item3)  # 子节 索引
                            Item3_1.setText(0, '%s' % (index.ind_name))
                            col_sum_1 = 0
                            for col_1 in index.col:
                                Item3_2 = QtWidgets.QTreeWidgetItem(Item3_1)  # 索引的列
                                Item3_2.setText(0, '%s' % (col_1.col_name + ' (' + col_1.col_type_name + ')'))
                                Item3_1.addChild(Item3_2)  # 添加子节点
                                col_sum_1 += 1
                            Item3_1.setText(0, '%s(%s)' % (index.ind_name, col_sum_1))
                            Item3.addChild(Item3_1)  # 添加子节点
                            index_sum += 1
                        Item3.setText(0, '%s(%s)' % ('indexes', index_sum))  # 索引名
                        Item1.setText(0, '%s(%s/%s)' % (table.tab_name, col_sum, 0))  # 表名
                Item_tab.setText(0, '%s(%d)' % ('tables', tab_sum))
        Item_db.setText(0, '%s(%s)' % (self.db1.db_name, user_sum))

    # tree 的鼠标左键
    def showSelected(self):
        item = self.treeWidget1.currentItem()
        if item == None:
            a = 0
        elif item.parent() == None:  # db 层 菜单
            a = 0
        elif item.parent().parent() == None:  # user 层  菜单
            a = 0
        elif item.parent().text(0)[0:6] == 'tables':
            self.tab_show()
        else:
            a = 0

    # table2 表数据显示
    def tab_show(self):
        data = []
        item = self.treeWidget1.currentItem()
        item1 = item.parent().parent()
        user_text1 = item1.text(0)  # 获取当前user_name
        tab_text1 = item.text(0)  # 获取当前table_name
        b = tab_text1.find('(', 0, -1)
        if b == -1:
            b = 0
        user_name1 = user_text1
        tab_name1 = tab_text1[0:b]
        self.tableWidget2.setAlternatingRowColors(True)  # 隔行变色
        for table in self.tables:
            if table.tab_name == tab_name1 and table.owner_name == user_name1:
                data1 = self.ora.unload_tab(self.file_infos, table, '')  # 解析表
                for data1_1 in data1:
                    for record in data1_1.record:
                        data.append(record.col_data2)
                print('table:%s, rec_sum:%d' % (tab_name1, len(data)))

                if len(data) == 0:
                    col_count = table.col_sum;
                    row_count = 0
                else:
                    col_count = len(data[0])  # 列数
                    row_count = len(data)  # 行数
                # 显示表数据
                item.setText(0, '%s(%s/%d)' % (table.tab_name, table.col_sum, row_count))  # 表名
                self.tableWidget2.setColumnCount(table.col_sum)
                self.tableWidget2.setRowCount(row_count)
                for i in range(table.col_sum):  # 表头列，设置表头
                    self.tableWidget2.setHorizontalHeaderItem(i, Qt.QTableWidgetItem("%s" % table.col[i].col_name))
                for i in range(row_count):  # 设置表数据
                    self.tableWidget2.setRowHeight(i, 20)  # 调整行高
                    for ii in range(table.col_sum):  # 列
                        try:
                            self.tableWidget2.setItem(i, ii, Qt.QTableWidgetItem("%s" % data[i][ii]))
                        except IndexError:
                            break
                break

    # tree的右键菜单
    def on_treeWidget1(self):  # on_treeWidget1_customContextMenuRequested
        menu_tab0 = QtWidgets.QMenu(self)  # db 层
        menu_tab0.addAction(self.expdbAction)
        menu_tab1 = QtWidgets.QMenu(self)  # user层
        menu_tab1.addAction(self.expuser_2_db_Action)
        menu_tab1.addAction(self.expinfo_Action)
        menu_tab2 = QtWidgets.QMenu(self)  # table层
        menu_tab2.addAction(self.exptab_2_db_Action)
        menu_tab2.addAction(self.exptab_2_sql_Action)

        item = self.treeWidget1.currentItem()
        if item != None:
            if item.parent() == None:
                menu_tab0.exec_(QtGui.QCursor.pos())
            elif item.parent().parent() == None:
                menu_tab1.exec_(QtGui.QCursor.pos())
            elif item.parent().text(0)[0:6] == 'tables':
                menu_tab2.exec_(QtGui.QCursor.pos())
            else:
                a = 0

    # table2 的右键菜单
    def on_tableWidget2(self, pos):
        menu_1 = QtWidgets.QMenu(self)
        menu_1.addAction(self.selectallAction)
        menu_1.addAction(self.notselectAction)
        item = self.tableWidget2.currentItem()
        if item != None:
            a = 0
        #  menu_1.exec_(QtGui.QCursor.pos())

    # 导出表到 Oracle
    def exptab_2_db(self):
        if self.reg == 0:
            self.register()
            return
        item = self.treeWidget1.currentItem()
        tab_text = item.text(0)  # 获取当前item的文本
        print('tab_name:%s,%s' % (self.table.tab_name, tab_text))
        self.db_link()

    # 导出用户到 Oracle
    def expuser_2_db(self):  # 导出所有的此类文件
        if self.reg == 0:
            self.register()
            return
        self.db_link()

    # 导出用户下的所有表结构
    def expuser_info(self):
        if self.reg == 0:
            self.register()
            return

    # 导出表数据到sql文件
    def exptab_2_sql(self):
        if self.reg == 0:
            self.register()
            return
        a = 0

    def db_link(self):
        # 弹出导出配置界面
        self.dblink_widget = QtWidgets.QWidget()
        self.dblink_widget.setGeometry(QtCore.QRect(385, 100, 550, 350))
        self.dblink_widget.setWindowTitle('配置连接到Oracle数据库')
        self.label_30 = QtWidgets.QLabel(self.dblink_widget)
        self.label_30.setGeometry(QtCore.QRect(10, 20, 80, 23))
        self.label_30.setText('连接名称')
        self.lineEdit_30 = QtWidgets.QLineEdit(self.dblink_widget)
        self.lineEdit_30.setGeometry(QtCore.QRect(100, 20, 400, 23))
        self.label_31 = QtWidgets.QLabel(self.dblink_widget)
        self.label_31.setGeometry(QtCore.QRect(10, 60, 80, 23))
        self.label_31.setText('主机名')
        self.lineEdit_31 = QtWidgets.QLineEdit(self.dblink_widget)
        self.lineEdit_31.setGeometry(QtCore.QRect(100, 60, 250, 23))
        self.label_35 = QtWidgets.QLabel(self.dblink_widget)
        self.label_35.setGeometry(QtCore.QRect(360, 60, 40, 23))
        self.label_35.setText('端口')
        self.lineEdit_35 = QtWidgets.QLineEdit(self.dblink_widget)
        self.lineEdit_35.setGeometry(QtCore.QRect(400, 60, 100, 23))
        self.lineEdit_35.setText('1521')
        self.label_32 = QtWidgets.QLabel(self.dblink_widget)
        self.label_32.setGeometry(QtCore.QRect(10, 100, 80, 23))
        self.label_32.setText('用户名')
        self.lineEdit_32 = QtWidgets.QLineEdit(self.dblink_widget)
        self.lineEdit_32.setGeometry(QtCore.QRect(100, 100, 400, 23))
        self.label_33 = QtWidgets.QLabel(self.dblink_widget)
        self.label_33.setGeometry(QtCore.QRect(10, 140, 80, 23))
        self.label_33.setText('密码')
        self.lineEdit_33 = QtWidgets.QLineEdit(self.dblink_widget)
        self.lineEdit_33.setGeometry(QtCore.QRect(100, 140, 400, 23))
        self.label_34 = QtWidgets.QLabel(self.dblink_widget)
        self.label_34.setGeometry(QtCore.QRect(10, 180, 80, 23))
        self.label_34.setText('SID')
        self.lineEdit_34 = QtWidgets.QLineEdit(self.dblink_widget)
        self.lineEdit_34.setGeometry(QtCore.QRect(100, 180, 400, 23))

        self.pushButton_22 = QtWidgets.QPushButton(self.dblink_widget)
        self.pushButton_22.setGeometry(QtCore.QRect(100, 260, 100, 23))
        self.pushButton_22.setText('测试')
        self.pushButton_23 = QtWidgets.QPushButton(self.dblink_widget)
        self.pushButton_23.setGeometry(QtCore.QRect(200, 260, 100, 23))
        self.pushButton_23.setText('取消')
        self.pushButton_25 = QtWidgets.QPushButton(self.dblink_widget)
        self.pushButton_25.setGeometry(QtCore.QRect(300, 260, 100, 23))
        self.pushButton_25.setText('导出用户')
        self.pushButton_24 = QtWidgets.QPushButton(self.dblink_widget)
        self.pushButton_24.setGeometry(QtCore.QRect(400, 260, 100, 23))
        self.pushButton_24.setText('导出表')

        self.dblink_widget.show()
        self.cc = 0  # 连接是否OK
        self.cc_user = 0
        self.pushButton_25.clicked.connect(self.data_out1)  # 点击导出用户
        self.pushButton_24.clicked.connect(self.data_out2)  # 点击导出表
        self.pushButton_22.clicked.connect(self.link_test)  # 点击测试
        self.pushButton_23.clicked.connect(self.link_close)  # 点击取消

    def data_out1(self):
        if self.reg == 1 and self.cc == 1:
            self.cc_user = 1
            item = self.treeWidget1.currentItem()
            user_text = item.text(0)  # 获取当前item的文本
            for table in self.tables:
                if table.user_name == user_text:
                    print('table:%s.%s,  %s' % (table.user_name, table.tab_name, user_text))
                    self.table = table
                    self.data1 = self.mdf.unload_tab(self.file_infos, table, '')  # 解析这个表
                    self.mdf.save_tab(self.data1, self.table, self.conn)
            print('用户：%s 导入完成...' % user_text)
        else:
            QtWidgets.QMessageBox.about(self.dblink_widget, "测试连接", "连接失败 ...  \t\t\n\n")

    def data_out2(self):
        if self.reg == 1 and self.cc == 1:
            self.mdf.save_tab(self.data1, self.table, self.conn)
        else:
            QtWidgets.QMessageBox.about(self.dblink_widget, "测试连接", "连接失败 ...  \t\t\n\n")

    # 连接Oracle测试
    def link_test(self):
        host = self.lineEdit_31.text()  # host
        port = self.lineEdit_35.text()  # port
        user = self.lineEdit_32.text()  # user
        password = self.lineEdit_33.text()  # password
        SID = self.lineEdit_34.text()  # db_naem
        db = 'host="%s:%s",user="%s",password="%s",SID="%s"' % (host, port, user, password, SID)
        print(db)
        if host == '' or user == '' or password == '' or SID == '':
            QtWidgets.QMessageBox.about(self.dblink_widget, "测试连接", "连接失败,信息不全 ...  \t\t\n")
            return
        try:
            self.oracle = cx_Oracle.connect(user, password, '%s:%s/%s' % (host, port, SID))  # 建立连接，3 个参数分开写
            self.cursor = self.oracle.cursor()
        except (cx_Oracle.InterfaceError, cx_Oracle.DatabaseError) as e:
            QtWidgets.QMessageBox.about(self.dblink_widget, "测试连接", "连接失败 ...  \t\t\n\n%s\t" % (e))
        else:
            QtWidgets.QMessageBox.about(self.dblink_widget, "测试连接", "连接成功 ...  \t\t\n")
            self.cc = 1

    def link_close(self):
        self.dblink_widget.close()

    def selectall(self):
        self.tableWidget2.selectAll()  # 全选

    def notselect(self):
        self.tableWidget2.clearSelection()  # 清除选择

    def progress(self, progress_val):
        self.progressBar.setValue(progress_val)

    def closeEvent(self, e):
        if self.file_infos == []:
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
        QtWidgets.QMessageBox.about(self, "About", "\tDBF unload  \t\n")


class myui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myui, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = myui()
    ui.show()
    sys.exit(app.exec_())
