# -*- coding: utf-8 -*-
#  ASM 解析
import struct, time, sqlite3  # ,sys
import threading, logging

s = struct.unpack  # B H I


# 结构体
class kfbh():  # 块头结构,32B
    def __init__(self):
        self.endian = 1  # 平台软件的字节顺序(大小端),1:小端,0:大端
        self.hard = 130  # 用于标识的magic数,4k:0x82,8k:0xa2,16k:0xc2
        self.type = 1  # 元数据类型，主要包括1种磁盘头,4种文件目录,6种磁盘目录,11种别名和12种间接扩展
        self.datfmt = 1  # 元数据的数据块的数据格式
        self.block_blk = 1  # 当前块所属的ASM文件内的块号(4k/块)
        self.block_obj = 1  # 当前块所属的文件号(ASM中的文件号,不是数据库文件的文件号)
        self.check = 1  # 用于块一致性检查的校验和


class kfdhdb():  # 磁盘头结构
    def __init__(self):
        self.file = 0  # 文件,句柄
        self.frm = ''  # 大小端
        self.driver_provstr = ''  # 驱动程序保留信息
        self.compat = ''  # 打开本磁盘组所需的ASM最小版本
        self.dsknum = 0  # 磁盘号
        self.dskname = ''  # 磁盘名
        self.grpname = ''  # 磁盘组名
        self.hdrsts = ''  # 磁盘状态.
        self.grptyp = ''  # 磁盘组的冗余类型
        self.crestmp = 0  # 磁盘创建时间戳
        self.mntstmp = 0  # mount时间戳
        self.secsize = 0  # 磁盘扇区大小(B)(=512B)
        self.blksize = 0  # 元数据块大小(B)(=4096B)
        self.ausize = 0  # 分配单元大小(B)(=1M)
        self.mfact = 0  # 0x0c0: 0x0001bc80
        self.dsksize = 0  # 磁盘大小，以分配单元为单位,取值时已转为G
        self.pmcnt = 0  # 物理元数据所占用的分配单元数
        self.fstlocn = 0  # 空闲空间表的第一个块号
        self.altlocn = 0  # 分配表的第一个块号
        self.f1b1locn = 0  # 文件目录指针,文件目录是一个特殊的虚拟元数据文件,它包含了所有ASM文件的I-NODE
        self.dbcompat = 0  # 打开磁盘组所需的数据库实例最小版本
        self.grpstmp = 0  # 磁盘组创建时间戳


class kfffdb():  # ASM file directory 文件目录 结构
    def __init__(self):
        self.name = ''  # 文件名
        self.file_no = 0  # 文件号
        self.grpname = ''  # 文件所在的磁盘组名
        self.incarn = 0  # 块的分配信息。 作为名字的一个 版本号
        self.hibytes = 0  # 文件字节数高位
        self.lobytes = 0  # 文件字节数低位
        self.xtntcnt = 0  # 给文件分配的扩展数
        self.xtnteof = 0  # 文件EOF之前的扩展数,总的扩展数
        self.blkSize = 0  # 每个块的字节数，不同的文件类型块大小可能不同，比如，元数据为4096b,数据库日志文件为512b，而数据文件一般是8k
        self.flags = 0  # 文件标志
        self.fileType = 0  # 文件类型. 15:元数据文件; 13:参数文件; 2:数据文件;6:临时文件;3:日志文件;1:控制文件
        self.dXrs = 0  # 直接扩展冗余模式,如果采用了正常冗余,每个扩展还会增加一个镜像,而如果采用高度冗余,每个扩展会增加2个镜像
        self.iXrs = 0  # 间接扩展冗余模式
        self.dXsiz_0 = 0  # 每种扩展大小包含的直接扩展数,扩展大小分为1个分配单元,4个分配单元,16个分配单元三种
        self.dXsiz_1 = 0  # 0x028: 0x00000000
        self.dXsiz_2 = 0  # 0x02c: 0x00000000
        self.iXsiz_0 = 0  # 每种扩展大小包含的间接扩展数
        self.iXsiz_1 = 0  # 0x034: 0x00000000
        self.iXsiz_2 = 0  # 0x038: 0x00000000
        self.xtntblk = 0  # 本块 包含的直接和间接指针总数量,如：10,61,63
        self.break1 = 0  # 直接和间接扩展指针的边界插槽，一般是60，表示前60个是直接扩展指针
        self.priZn = 0  # 主扩展所处磁盘区
        self.secZn = 0  # 镜像扩展所处磁盘区
        self.ub2spare = 0  # 0x042: 0x0000
        self.alias_0 = 0  # 文件指针别名
        self.alias_1 = 0  # 0x048: 0xffffffff      #  file.xtnteof//file.strpwdth
        self.strpwdth = 0  # 条带宽度，即条带跨越几个扩展，可以简单理解为在几个AU/磁盘 间做条带。
        self.strpsz = 0  # 条带大小(2^N)比如20表示1m的条带。条带宽度和条带大小决定了条带划分模式
        self.usmsz = 0  # 文件附加的用户元数据大小
        self.crets_hi = ''  # 文件创建时间
        self.modts_hi = ''  # 文件修改时间
        self.xptr = []  # 文件指针 数组
        self.map = []


class xptr():  # 文件数据指针 结构 (8B)
    def __init__(self):
        self.au = 0  # 0x4a0:    4B
        self.disk = 0  # 0x4a4:    2B
        # self.flags = 0		# 0x4a6:    1B
        # self.chk = 0		# 0x4a7:    1B


class kfddde():  # ASM DISK DIRECTORY  磁盘目录 结构
    def __init__(self):
        self.dsknum = 0  # diskgroup中，该disk的disk编号，从0开始排序，该值为0，说明该disk是这个磁盘组中的第一个disk
        self.state = 0  # disk状态。其中2表示normal。在asm中，该值对应v$asm_disk.state，主要有如下几种值：
        self.dskname = 0  # 磁盘名称，这是asm中定义的diskname.
        self.fgname = 0  # 这表示failgroup diskname，由于我这里是external冗余，所以failgroup就是本身。
        self.crestmp = ''  # 这里表示该disk的创建时间戳
        # self.failstmp = 0    # 这里表示disk 失败的时间戳
        # self.timer = 0
        self.size = 0  # disk大小,由于au默认是1m,所以这里是1024m。


class kffdnd():  # ASM ALIAS DIRECTORY  的块头目录结构信息
    def __init__(self):
        self.bnode_incarn = 0  # 分配信息，包括block的分支号和指向next freelist block的指针
        self.parent_number = 0  # 表示指向上一层的block
        self.overfl_incarn = 0  # overfl,表示指向同层级的下一个block
        self.fstblk_number = 0  # 第一个block。


class kfade():  # ASM ALIAS DIRECTORY(别名目录) 的 结构
    def __init__(self):
        self.level = 0
        self.current_number = 0  # 表示当前block号
        self.parent_number = 0  # 表示指向上一层的block
        self.overfl_number = 0  # overfl,表示指向同层级的下一个block
        self.fstblk_number = 0  # 第一个block。
        self.refer_number = 0  # 指向下一层的block号
        self.name = ''
        self.fnum = 0
        self.finc = 0
        self.flags = 0


class xptr_1():  # 文件数据指针 结构2 (8B)
    def __init__(self):
        self.disk = 0  # 0x4a4:    2B
        self.strip_no = 0  # 0x4a0:    4B


# 多线程,导出文件
class OUT_FILE(threading.Thread):  # 类OUT_FILE继承自 threading
    def __init__(self, disk, file_info, out_path, db):  # 解析函数
        super(OUT_FILE, self).__init__()
        self.disk = disk
        self.file_info = file_info
        self.out_path = out_path
        self.db = db

    def run_1(self):  # 解文件map到内存
        print('开始导出到内存...')
        logging.info('开始导出到内存...')
        kfdhdb1 = self.disk[0];
        err_files = 0
        for i in range(len(self.file_info)):  # 每一个文件
            file = self.file_info[i];
            err_is = 0;
            yichu = 0;
            map = []
            strip = 2 ** file.strpsz  # 条带大小
            #    f_size1 = file.lobytes+file.hibytes*4294967296; f_size2 = 0
            print('file#%d: 指针数:%s,指针数:%s,条带宽度:%s,条带大小:%sK,解出指针数:%s' % (
            file.file_no, file.xtntcnt, file.xtnteof, file.strpwdth, strip / 1024, len(file.xptr)))
            logging.info('file#%d: 指针数:%s,指针数:%s,条带宽度:%s,条带大小:%sK,解出指针数:%s' % (
            file.file_no, file.xtntcnt, file.xtnteof, file.strpwdth, strip / 1024, len(file.xptr)))
            loop_1 = file.xtnteof // file.strpwdth  # 总的 指针数(AU数)/一层的AU数
            loop_2 = file.xtnteof % file.strpwdth  # 总的 指针数(AU数)%一层的AU数

            for i1 in range(loop_1 + 1):  # 总的 指针数(AU数)/一层的AU数   *********************
                if i1 < loop_1:
                    aa1 = 0;
                    aa2 = 0;  # aa1是au号 ,aa2 是当前层号.
                    ausize = kfdhdb1.ausize
                    if kfdhdb1.compat == '11.2.0.0.0' or kfdhdb1.compat == '12.1.0.0.0':
                        if file.strpwdth * i1 < 20000:
                            ausize = kfdhdb1.ausize  # AU 大小
                        elif file.strpwdth * i1 >= 20000 and file.strpwdth * i1 < 40000:
                            ausize = kfdhdb1.ausize * 4  # 4M 的AU 大小
                        elif file.strpwdth * i1 >= 40000:
                            ausize = kfdhdb1.ausize * 16
                    bb1 = int(ausize / strip)  # AU 大小/条带大小 ， 层数
                    loop = file.strpwdth * bb1  # loop_1是 一层的AU数* 层数
                    for i2 in range(loop):
                        id = i1 * file.strpwdth + aa1
                        try:
                            disk_no = file.xptr[id].disk  # 磁盘号
                        except IndexError:  #
                            err_is = 1;
                            yichu += 1
                            if yichu == 1:  # 第一层
                                #    print('file#%d：xptr[id]溢出,文件有间接指针没找全'%(file.file_no))    # 有溢出的说明 其间接指针 没找全
                                logging.warning('file#%d：xptr[id]溢出，文件有间接指针没找全' % (file.file_no))
                            break  # continue
                        au_no = file.xptr[id].au
                        f1 = 0
                        for disk_1 in self.disk:
                            if disk_1.dsknum == disk_no:
                                f1 = disk_1.file
                                break  # 此盘找到了，不用在循环找了
                        if f1 == 0:  # 此盘没有找到
                            if aa2 == 0:  # 第一层
                                #  print('file#%d：此磁盘没找到：disk_no:%d'%(file.file_no,disk_no))
                                logging.warning('file#%d：此磁盘没找到：disk_no:%d' % (file.file_no, disk_no))
                            err_is = 1
                        #   continue
                        map1 = xptr_1()
                        map1.disk = disk_no
                        map1.strip_no = au_no * int(kfdhdb1.ausize / strip) + aa2
                        map.append(map1)
                        aa1 += 1
                        if aa1 == file.strpwdth:  #
                            aa1 = 0;
                            aa2 += 1  # aa1是au号 ,aa2 是当前层号
                elif i1 == loop_1:
                    aa1 = 0;
                    aa2 = 0;  # aa1是au号 ,aa2 是当前层号.
                    ausize = kfdhdb1.ausize
                    if kfdhdb1.compat == '11.2.0.0.0' or kfdhdb1.compat == '12.1.0.0.0':
                        if file.strpwdth * i1 < 20000:
                            ausize = kfdhdb1.ausize  # AU 大小
                        elif file.strpwdth * i1 >= 20000 and file.strpwdth * i1 < 40000:
                            ausize = kfdhdb1.ausize * 4  # 4M 的AU 大小
                        elif file.strpwdth * i1 >= 40000:
                            ausize = kfdhdb1.ausize * 16
                    bb1 = int(ausize / strip)  # AU 大小/条带大小 ， 层数
                    loop = loop_2 * bb1  # loop_1是 一层的AU数* 层数
                    for i2 in range(loop):
                        id = i1 * file.strpwdth + aa1
                        try:
                            disk_no = file.xptr[id].disk  # 磁盘号
                        except IndexError:  #
                            err_is = 1;
                            yichu += 1
                            if yichu == 1:  # 第一层
                                #    print('file#%d：xptr[id]溢出,文件有间接指针没找全'%(file.file_no))    # 有溢出的说明 其间接指针 没找全
                                logging.warning('file#%d：xptr[id]溢出，文件有间接指针没找全' % (file.file_no))
                            break  # continue
                        au_no = file.xptr[id].au
                        f1 = 0
                        for disk_1 in self.disk:
                            if disk_1.dsknum == disk_no:
                                f1 = disk_1.file
                                break  # 此盘找到了，不用在循环找了
                        if f1 == 0:  # 此盘没有找到
                            if aa2 == 0:  # 第一层
                                #  print('file#%d：此磁盘没找到：disk_no:%d'%(file.file_no,disk_no))
                                logging.warning('file#%d：此磁盘没找到：disk_no:%d' % (file.file_no, disk_no))
                            err_is = 1
                        #    continue
                        map1 = xptr_1()
                        map1.disk = disk_no
                        map1.strip_no = au_no * int(kfdhdb1.ausize / strip) + aa2
                        map.append(map1)
                        aa1 += 1
                        if aa1 == file.strpwdth:  #
                            aa1 = 0;
                            aa2 += 1  # aa1是au号 ,aa2 是当前层号

            if err_is == 1:
                err_files += 1
            self.file_info[i].map = map
            print('file#%d：%s 完成... err_is:%d' % (file.file_no, file.name, err_is))
            logging.info('file#%d：%s 完成... err_is:%d' % (file.file_no, file.name, err_is))
        print('导出到内存：完成... 损坏文件数:%d' % (err_files))
        logging.info('导出到内存：完成... 损坏文件数:%d' % (err_files))

    def run_2(self, db):  # 解文件map到数据库
        f = open(db, 'wb')
        f.close()
        conn = sqlite3.connect(db)  # 打开数据库
        cursor = conn.cursor()
        cursor.execute("create table t_all(file_no,blk_start,blk_end,disk_no,au_no);")
        print('开始导出到sqlite...')
        logging.info('开始导出到sqlite...')
        for i in range(len(self.file_info)):  # 每一个文件
            file = self.file_info[i]
            strip = 2 ** file.strpsz  # 条带大小
            blk_size = file.blkSize  # 文件的块大小
            aa = strip / blk_size
            try:
                cursor.execute("create table t_%s(id,file_no,blk_start,blk_end,disk_no,au_no);" % (file.file_no))
            except sqlite3.OperationalError:
                cursor.execute("drop table t_%s;" % (file.file_no))
                cursor.execute("create table t_%s(id,file_no,blk_start,blk_end,disk_no,au_no)" % (file.file_no))
            for ii in range(len(file.map)):
                cursor.execute("insert into t_%s values(%d,%d,%d,%d,%d,%d);" % (
                file.file_no, ii, file.file_no, int(ii * aa), int((ii + 1) * aa - 1), file.map[ii].disk,
                file.map[ii].strip_no))
                cursor.execute("insert into t_all values(%d,%d,%d,%d,%d);" % (
                file.file_no, int(ii * aa), int((ii + 1) * aa - 1), file.map[ii].disk, file.map[ii].strip_no))
                if ii % 100000 == 0:  # 97G的指针 提交一次
                    conn.commit()
            conn.commit()
        cursor.close()
        print('导出到sqlite 完成 ...')

    def run_3(self):  # 导出文件
        print('开始导出文件...')
        logging.info('开始导出文件...')
        err_files = 0
        for i in range(len(self.file_info)):  # 每一个文件
            file = self.file_info[i];
            err_is = 0
            f = open(self.out_path + '/' + file.name, 'w+b')
            f_size1 = file.lobytes + file.hibytes * 4294967296;
            f_size2 = 0
            strip = 2 ** file.strpsz  # 条带大小
            blk_size = file.blkSize  # 文件的块大小
            for ii in range(len(file.map)):
                f1 = 0
                for disk_1 in self.disk:
                    if disk_1.dsknum == file.map[ii].disk:
                        f1 = disk_1.file
                        break
                if f1 == 0:
                    #     #  print('导出file#%d：此磁盘没找到：disk_no:%d'%(file.file_no,file.map[ii].disk))
                    #     logging.warning('导出file#%d：此磁盘没找到：disk_no:%d'%(file.file_no,file.map[ii].disk))
                    err_is = 1
                    continue
                f1.seek(file.map[ii].strip_no * strip)
                data = f1.read(strip)  # 一般是 读取 1M

                f_size2 = ii * strip  # 文件现在的大小
                aa = f_size1 - f_size2  # 处理文件尾部
                #   print('i1:%d,i2:%d,disk_no:%d,au_no:%d,f_size1:%d,f_size2:%d'%(i1,i2,disk_no,au_no,f_size1,f_size2))
                if aa <= strip:
                    if aa <= 0:
                        aa = 0
                    f1.seek(file.map[ii].strip_no * strip)
                    data = f1.read(aa)

                f.seek(ii * strip)  #
                try:
                    f.write(data)
                except OSError as e:
                    print('OSError: %s: %s\n' % (e.errno, e.strerror))
                    err_is == 1
                    break

            if err_is == 1:
                err_files += 1
            f.close()
            print('导出file#%d：%s 完成... err_is:%d' % (file.file_no, file.name, err_is))
            logging.info('导出file#%d：%s 完成... err_is:%d' % (file.file_no, file.name, err_is))
        print('导出：完成... 损坏文件数:%d' % (err_files))
        logging.info('导出：完成... 损坏文件数:%d' % (err_files))

    # 单独开的线程
    def run(self):
        self.run_1()  # 解文件map到内存
        if self.db != '':
            self.run_2(self.db)  # 解文件map到数据库
        elif self.db == '':
            self.run_3()  # 导出文件


class ASM():
    def __init__(self):
        self.disks = []

    def datetime(self, data, frm):
        data_1 = s(frm + '2I', data[0:8])
        hour = data_1[0] & 31  # 5bit
        day = (data_1[0] >> 5) & 31  # 5bit
        month = (data_1[0] >> 10) & 15  # 4bit
        year = (data_1[0] >> 14) & 65535  # 18bit
        suec = data_1[1] & 1023  # 微妙 10bit
        msec = (data_1[1] >> 10) & 1023  # 毫秒 10bit
        secs = (data_1[1] >> 20) & 63  # 秒 6bit
        mins = (data_1[1] >> 26) & 63  # 分钟 6bit
        datetime1 = '%d-%d-%d %d:%d:%d' % (year, month, day, hour, mins, secs)
        return datetime1

    def version(self, data, frm):
        ver_1 = s("4B", data[0:4])
        if frm == '<':
            version1 = str(ver_1[3]) + '.' + str(ver_1[2] // 16) + '.' + str(ver_1[2] % 16) + '.' + str(
                ver_1[1]) + '.' + str(ver_1[0])
        else:
            version1 = str(ver_1[0]) + '.' + str(ver_1[1] // 16) + '.' + str(ver_1[1] % 16) + '.' + str(
                ver_1[2]) + '.' + str(ver_1[3])
        return version1

    # 初始化磁盘信息，磁盘头信息
    def disk_init(self, fn):  # 初始化磁盘信息
        self.disks = []
        for i in range(len(fn)):  # 磁盘头
            f = open(fn[i], 'rb')
            data_1 = f.read(8192)
            endian = s('B', data_1[0:1])
            if endian[0] == 1:
                frm = '<'
            elif endian[0] == 0:
                frm = '>'
            #    else: return
            #   kfbh_1 = s(frm+'4BII',data_1[0:12])     # 块头信息
            kfdhdb1 = kfdhdb()  # 磁盘头
            kfdhdb1.file = f;
            kfdhdb1.frm = frm
            kfdhdb1.driver_provstr = str(data_1[32:64], encoding="gbk").rstrip(str(b'\x00', encoding="gbk"))  # 驱动程序保留信息
            version1 = self.version(data_1[64:68], frm)
            kfdhdb1.compat = version1
            kfdhdb_1 = s(frm + 'H2B', data_1[68:72])
            hdrsts = {3: '正常', 1: '不可读', 2: '可被添加', 4: '移除', 5: '冲突', 6: '不兼容', 7: '可被添加', 0: '未知'}
            grptyp = {1: '无冗余', 2: '正常冗余', 3: '高冗余', 0: '未知'}
            kfdhdb1.dsknum = kfdhdb_1[0]
            kfdhdb1.grptyp = grptyp[kfdhdb_1[1]]
            try:
                kfdhdb1.hdrsts = hdrsts[kfdhdb_1[2]]
            except KeyError as e:
                kfdhdb1.hdrsts = ''
            kfdhdb1.dskname = str(data_1[72:104], encoding="gbk").rstrip(str(b'\x00', encoding="gbk"))  # 磁盘名
            kfdhdb1.grpname = str(data_1[104:136], encoding="gbk").rstrip(str(b'\x00', encoding="gbk"))  # 磁盘组名
            kfdhdb_2 = s(frm + 'HH7I', data_1[216:248])
            kfdhdb1.secsize = kfdhdb_2[0]  # 磁盘扇区大小(B)(=512B)
            kfdhdb1.blksize = kfdhdb_2[1]  # 元数据块大小
            kfdhdb1.ausize = kfdhdb_2[2]  # au 大小
            kfdhdb1.mfact = kfdhdb_2[3]  # 113792  ?
            kfdhdb1.dsksize = kfdhdb_2[4] / 1024  # 磁盘大小 GB
            kfdhdb1.pmcnt = kfdhdb_2[5]
            kfdhdb1.fstlocn = kfdhdb_2[6]
            kfdhdb1.altlocn = kfdhdb_2[7]
            kfdhdb1.f1b1locn = kfdhdb_2[8]
            kfdhdb1.crestmp = self.datetime(data_1[200:208], frm)
            kfdhdb1.mntstmp = self.datetime(data_1[208:216], frm)
            self.disks.append(kfdhdb1)
        return self.disks  # 没有按磁盘号排序的

    def disk_file_list(self, disks, files):
        f = open(r'.\list.db', 'wb')
        f.close()
        conn = sqlite3.connect(r'.\list.db')  # 打开数据库
        cursor = conn.cursor()
        cursor.execute("create table disk_group(disk_no,disk_name,disk_size_G)")
        cursor.execute("create table file_name(file_no,file_name,size_B,size_G,xt_no)")
        for disk_1 in disks:
            cursor.execute("insert into disk_group(disk_no,disk_name,disk_size_G) values(%d,'%s',%s);" % (
            disk_1.dsknum, disk_1.file.name, disk_1.dsksize))
        for file in files:
            cursor.execute(
                "insert into file_name(file_no,file_name,size_B,size_G,xt_no) values(%d,'%s',%d,%7.3f,%d);" % (
                file.file_no, file.name, int(file.lobytes + file.hibytes * 4294967296),
                (file.lobytes + file.hibytes * 4294967296) / 1024.0 / 1024 / 1024.0, file.xtntcnt))
        conn.commit()

    # 解析asm磁盘上的元文件
    def asm(self, disks):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s]  %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='asm_%s.log' % (time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))),
                            filemode='w')
        file_data = []  # 解析文件目录,文件1
        disk_data = []  # 解析磁盘目录,文件2
        alias_data = []  # 解析别名目录,文件6
        kfdhdb1 = disks[0]
        frm = kfdhdb1.frm
        au_off = kfdhdb1.f1b1locn
        print('ASM 解析开始 ... \n')
        logging.info('ASM 解析开始 ... \n')
        if kfdhdb1.dsknum == 0:  # 初始化 file#1 的文件目录，获取到file#1的信息
            f = kfdhdb1.file
            f.seek(au_off * kfdhdb1.ausize + 1 * kfdhdb1.blksize)
            data_2 = f.read(4096)
            if len(data_2) != 4096:
                print(' 初始化 file#1的指针, 此块没有数据：disk_no:%d,au_no:%d' % (0, au_off))
                logging.warning('初始化file#1的指针, 的此块没有数据：disk_no:%d,au_no:%d' % (0, au_off))
                return [], []
            kfffdb0 = kfffdb()  # file#1的文件目录
            file_no1 = s(frm + 'I', data_2[4:8])
            kfffdb0.file_no = file_no1[0]
            kfffdb_3 = s(frm + '2H', data_2[92:96])
            kfffdb0.xtntblk = kfffdb_3[0]
            kfffdb0.break1 = kfffdb_3[1]
            for i0 in range(kfffdb0.xtntblk):  # file1 数据指针
                off = 1216 + i0 * 8
                kfffdb_2 = s(frm + 'IHBB', data_2[off:off + 8])
                xptr1 = xptr()
                xptr1.au = kfffdb_2[0]
                xptr1.disk = kfffdb_2[1]
                kfffdb0.xptr.append(xptr1)

            for i1 in range(kfffdb0.xtntblk):  # 遍历文件1的所有块，完全解析file#1
                au_no = kfffdb0.xptr[i1].au
                disk_no = kfffdb0.xptr[i1].disk
                f = 0
                for disk_1 in disks:
                    if disk_1.dsknum == disk_no:
                        f = disk_1.file
                        break
                if f == 0:
                    print('file#1的此磁盘没找到：disk_no:%d' % (disk_no))
                    logging.warning('file#1的此磁盘没找到：disk_no:%d' % (disk_no))
                    continue
                loop1 = int(kfdhdb1.ausize / kfdhdb1.blksize)
                for i in range(loop1):  # 解析文件目录,文件1. 获得所有文件的信息(位图)
                    f.seek(au_no * kfdhdb1.ausize + (i) * kfdhdb1.blksize)
                    data_2 = f.read(4096);
                    err_is = 0
                    if len(data_2) != 4096:
                        if i == 0:
                            print('file#1的此块没有数据：disk_no:%d,au_no:%d' % (disk_no, au_no))
                            logging.warning('file#1的此块没有数据：disk_no:%d,au_no:%d' % (disk_no, au_no))
                            break
                        continue
                    kfffdb1 = kfffdb()  # 文件目录 , 文件属性
                    file_no1 = s(frm + 'I', data_2[4:8])
                    kfffdb1.file_no = file_no1[0]
                    kfffdb_0 = s(frm + 'I', data_2[32:36])
                    kfffdb1.incarn = kfffdb_0[0]  #
                    kfffdb_1 = s(frm + '5I2B', data_2[44:66])
                    kfffdb1.hibytes = kfffdb_1[0]
                    kfffdb1.lobytes = kfffdb_1[1]
                    kfffdb1.xtntcnt = kfffdb_1[2]
                    kfffdb1.xtnteof = kfffdb_1[3]
                    kfffdb1.blkSize = kfffdb_1[4]
                    kfffdb1.flags = kfffdb_1[5]
                    kfffdb1.fileType = kfffdb_1[6]
                    kfffdb_3 = s(frm + '2H', data_2[92:96])
                    kfffdb1.xtntblk = kfffdb_3[0]  # 本块 包含的直接和间接指针总数量
                    kfffdb1.break1 = kfffdb_3[1]
                    kfffdb_4 = s(frm + '2B', data_2[108:110])
                    kfffdb1.strpwdth = kfffdb_4[0]  # 条带宽度
                    kfffdb1.strpsz = kfffdb_4[1]  # 条带大小(2^N)比如20表示1m的条带
                    kfffdb1.crets_hi = self.datetime(data_2[112:120], frm)  # 文件创建时间
                    kfffdb1.modts_hi = self.datetime(data_2[120:128], frm)  # 文件修改时间
                    if kfffdb1.break1 == 0 or kfffdb1.xtntblk == 0:  # 屏蔽掉 file#0
                        continue
                    if kfffdb1.file_no == 2938:  # 调试
                        print('file#%d -----------' % kfffdb1.file_no)
                    for ii in range(kfffdb1.xtntblk):  # 解析此文件的 数据指针
                        off = 1216 + ii * 8
                        kfffdb_2 = s(frm + 'IHBB', data_2[off:off + 8])
                        xptr1 = xptr()
                        xptr1.au = kfffdb_2[0]
                        xptr1.disk = kfffdb_2[1]
                        # xptr1.flags = kfffdb_2[2]
                        # xptr1.chk = kfffdb_2[3]
                        if ii < kfffdb1.break1:
                            kfffdb1.xptr.append(xptr1)
                        elif ii >= kfffdb1.break1:  # 解析此文件的 间接数据指针
                            au_no1 = xptr1.au
                            disk_no1 = xptr1.disk
                            f1 = 0
                            for disk_1 in disks:  #
                                if disk_1.dsknum == disk_no1:
                                    f1 = disk_1.file
                                    break
                            if f1 == 0:
                                err_is = 1
                                print('解析file#%d 的间接指针,此磁盘没找到：disk_no:%d' % (kfffdb1.file_no, disk_no1))
                                logging.warning('解析file#%d 的间接指针,此磁盘没找到：disk_no:%d' % (kfffdb1.file_no, disk_no1))
                                continue
                            for i2 in range(loop1):  # 解析文件目录,文件1
                                f1.seek(au_no1 * kfdhdb1.ausize + (i2) * kfdhdb1.blksize)
                                data_3 = f1.read(kfdhdb1.blksize)  # 4096B
                                if len(data_3) != kfdhdb1.blksize:
                                    if i2 == 0:
                                        err_is = 1
                                        print('解析file#%d 的间接指针,所在的块没有数据：disk_no:%d,au_no:%d' % (
                                        kfffdb1.file_no, disk_no1, au_no1))
                                        logging.warning('解析file#%d 的间接指针,所在的块没有数据：disk_no:%d,au_no:%d' % (
                                        kfffdb1.file_no, disk_no1, au_no1))
                                        break
                                    continue
                                file_no2 = s(frm + 'IH', data_3[32:38])
                                xptr2_sum = file_no2[1]
                                for i3 in range(xptr2_sum):  # 解析此文件的 间接数据指针
                                    off = 44 + i3 * 8
                                    try:
                                        kfffdb_2 = s(frm + 'IHBB', data_3[off:off + 8])
                                    except struct.error:
                                        err_is = 1
                                        continue
                                    xptr2 = xptr()
                                    xptr2.au = kfffdb_2[0]
                                    xptr2.disk = kfffdb_2[1]
                                    # xptr2.flags = kfffdb_2[2]
                                    # xptr2.chk = kfffdb_2[3]
                                    kfffdb1.xptr.append(xptr2)
                    if kfffdb1.file_no < 10:
                        kfffdb1.strpwdth = 1
                        kfffdb1.strpsz = 20  # 1M的条带大小
                    file_data.append(kfffdb1)
                    strip = 2 ** kfffdb1.strpsz  # 条带大小
                    print('目录->file#: %d 解析完成... err_is:%d (指针数:%s,条带宽度:%s,条带大小:%sK,解出指针数:%s)' % (
                    kfffdb1.file_no, err_is, kfffdb1.xtntcnt, kfffdb1.strpwdth, strip / 1024, len(kfffdb1.xptr)))
                    logging.info('目录->file#: %d 解析完成... err_is:%d (指针数:%s,条带宽度:%s,条带大小:%sK,解出指针数:%s)' % (
                    kfffdb1.file_no, err_is, kfffdb1.xtntcnt, kfffdb1.strpwdth, strip / 1024, len(kfffdb1.xptr)))
                    del kfffdb1
        elif kfdhdb1.dsknum != 0:
            #  print('没有找到磁盘0 ...')
            logging.warning('没有找到磁盘0 ...')
            return [], []

        for i1 in range(file_data[1].xtntblk):  # 获取文件2的指针. 磁盘目录
            au_no = file_data[1].xptr[i1].au
            disk_no = file_data[1].xptr[i1].disk
            f = 0
            for disk_1 in disks:
                if disk_1.dsknum == disk_no:
                    f = disk_1.file
                    break
            if f == 0:
                #  print('file#2,此磁盘没找到：disk_no:%d'%(disk_no))
                #      logging.warning('file#2,此磁盘没找到：disk_no:%d'%(disk_no))
                continue
            for i in range(20):  # 解析磁盘目录,文件2.
                f.seek(au_no * kfdhdb1.ausize + (i) * kfdhdb1.blksize)
                data_3 = f.read(4096)
                if len(data_3) == 0:
                    #  print('file#2,此块没有数据：disk_no:%d,au_no:%d'%(disk_no,au_no))
                    logging.warning('file#2,此块没有数据：disk_no:%d,au_no:%d' % (disk_no, au_no))
                    continue
                for ii in range(8):  # 条目， 简单取法
                    off = 68 + ii * 448
                    kfddde_2 = s(frm + 'HB', data_3[off + 16:off + 19])
                    kfddde1 = kfddde()
                    kfddde1.dsknum = kfddde_2[0]
                    kfddde1.state = kfddde_2[1]
                    kfddde1.dskname = str(data_3[off + 20:off + 52], encoding="gbk").rstrip(
                        str(b'\x00', encoding="gbk"))  # ascii,gbk,gb2312,utf-16
                    kfddde1.fgname = str(data_3[off + 52:off + 84], encoding="gbk").rstrip(
                        str(b'\x00', encoding="gbk"))  # ascii,gbk,gb2312,utf-16
                    kfddde_3 = s(frm + 'I', data_3[off + 104:off + 108])
                    kfddde1.size = kfddde_3[0]
                    kfddde1.crestmp = self.datetime(data_3[off + 84:off + 92], frm)
                    if kfddde1.dskname == '':
                        continue
                    disk_data.append(kfddde1)

        for i1 in range(file_data[5].xtntblk):  # 获取文件6的指针，别名目录
            au_no = file_data[5].xptr[i1].au
            disk_no = file_data[5].xptr[i1].disk
            f = 0
            for disk_1 in disks:
                if disk_1.dsknum == disk_no:
                    f = disk_1.file
                    break
            if f == 0:
                #   print('file#6,此磁盘没找到：disk_no:%d'%(disk_no))
                #   logging.warning('file#6,此磁盘没找到：disk_no:%d'%(disk_no))
                continue
            for i in range(256):  # 解析别名目录,文件6.  每个AU
                f.seek(au_no * kfdhdb1.ausize + (i) * kfdhdb1.blksize)
                data_3 = f.read(4096)
                if len(data_3) == 0:
                    #  print('file#6,此块没有数据：disk_no:%d,au_no:%d'%(disk_no,au_no))
                    #    logging.warning('file#6,此块没有数据：disk_no:%d,au_no:%d'%(disk_no,au_no))
                    continue
                block_hdr = s(frm + 'I', data_3[4:8])
                kfade_1 = s(frm + '3I', data_3[44:56])  # kffdnd信息
                for i1 in range(53):  # 块(4096B)中条目
                    kfade1 = kfade()
                    off = 68 + 76 * i1
                    kfade_2 = s(frm + 'I', data_3[off + 12:off + 16])  # 下一级的块指针
                    kfade_3 = data_3[off + 16:off + 64]  # 文件名
                    kfade_4 = s(frm + '2IB', data_3[off + 64:off + 73])
                    kfade1.refer_number = kfade_2[0]  # 下一级的块指针
                    kfade1.name = str(kfade_3, encoding="gbk").rstrip(
                        str(b'\x00', encoding="gbk")).lower()  # alias 名称，转换为小写
                    kfade1.fnum = kfade_4[0]
                    kfade1.finc = kfade_4[1]
                    kfade1.flags = kfade_4[2]
                    kfade1.overfl_number = kfade_1[0]  # 指向同层级的下一个block
                    kfade1.parent_number = kfade_1[2]  # 上一级的块指针
                    kfade1.current_number = block_hdr[0]  # 当前的块号
                    if kfade1.fnum == 0:
                        continue
                    if kfade1.name == '':
                        break  # continue #
                    if kfade1.current_number == 0:
                        kfade1.level = 1
                    elif kfade1.parent_number == 0 and kfade1.fnum == 0xffffffff:
                        kfade1.level = 2
                    elif kfade1.parent_number == 1 or kfade1.refer_number == 0xffffffff or kfade1.refer_number == 0:
                        kfade1.level = 3
                    alias_data.append(kfade1)
        kfade2 = kfade()
        kfade2.level = 2
        kfade2.name = 'metafile'
        alias_data.append(kfade2)

        for i in range(len(file_data)):
            if file_data[i].file_no == 1:
                file_data[i].name = 'file directory'
            elif file_data[i].file_no == 2:
                file_data[i].name = 'disk directory'
            elif file_data[i].file_no == 6:
                file_data[i].name = 'alias directory'
            elif file_data[i].file_no in (3, 4, 5, 7, 8, 9, 12):
                file_data[i].name = 'file_%d' % file_data[i].file_no

            for ii in range(len(alias_data)):  # *************************
                if file_data[i].file_no == alias_data[ii].fnum:  # and file_data[i].flags == alias_data[ii].flags
                    file_data[i].name = alias_data[ii].name + '.' + str(file_data[i].file_no) + '.' + str(
                        file_data[i].incarn)  # 文件名，为小写
                    if alias_data[ii].flags == 17:
                        file_data[i].name = alias_data[ii].name
                        break  # *****************
        print("ASM 解析完成...\n")
        logging.info("ASM 解析完成...\n")
        logging.info('磁盘组名称:%s ,数据库名称：%s\n' % (kfdhdb1.grpname, alias_data[0].name))
        return file_data, alias_data, disk_data
