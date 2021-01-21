# 模块导入
from os import system, name, popen
from os.path import exists, abspath
from sys import exit, argv

import chardet
import openpyxl
from wget import download

# 变量定义
first_file_open = True
coding = 'utf8'
index_c = -1
system_log = ''
echo_mode = False
file_path = []
l = []
l1 = []
l2 = []
index = -1
help_text = """
    欢迎使用新的winvi
    新的winvi打开二进制文件会直接退出
    使用帮助：
        :S 保存缓存修改
        :X 退出
        :O 切换编辑的文件(默认为第一个命令参数的文件)(保存文件)
        :OX 强制切换文件
        :G 将文件现有内容加载至缓存
        :G1 将目前的修改存放至缓存
        :G2 将读取的xls文件内容加载至缓存
        :R 清空缓存
        :D 清空文件
        :ECHO>>FILE 使用命令echo xxx >> file 保存文件(追加式)(请使用完成以后使用:G记录)
        :PL 输出文件列表
        :C 清除某一行的全部内容
        :M 将文件指针移到某行尾(-1为默认)
        :ADD_OTHERS_FILE 将文件缓存至文件列表
        :PATH 当前文件路径
        :U 执行系统命令
        :PU 显示日志
        :MC 将文件指针移至特定字符串下
        :PS 输出字符占字符串的位置
        :WT 将web上http&s协议的文件下载到本地编辑(以后可能会开发ftp,ssr等协议的在线编辑)
        :DIR 故名思意
        :EXIT_COMMAND,:EC 退出命令模式
        :XLSX (测试中)Excel表格读取，不能直接打开，需存放至filepath
        内容存放至g2,目前只能读取文件表的名称
        :H 输出本帮助（等效－h参数）
        :P 输出文件内容
        :PM 输出文件内容(前加序号)
        :CLEAR_WINDOW,:CW 清屏
    """

# 预处理开始

if argv[0] == "python":  # 删除开头的Python
    argv.pop(0)

if len(argv) == 1:  # 判断是否有要求打开的文件
    input_file_path = input("输入要打开的文件,:X退出:")
    if input_file_path == ":X":
        exit()
    else:
        file_path.append(input_file_path)
        argv.append(input_file_path)

if argv[1] == "-v":  # 判断是否为特殊选项
    print('\t\twinvi version:1.1\n\t\tnew winvi')
    exit()
elif argv[1] == '-h':
    print(help_text)
    exit()

# 删除开头的“winvi.py”
argv.pop(0)
# 如果删除后长度大于１，说明有多个文件
for file in argv:
    file_path.append(file)
# 预处理结束

file = file_path[0]  # 把文件名弄出来
if exists(file):
    r = open(file, 'rb')
    coding = chardet.detect(r.read()).get('encoding')
    if not coding:
        coding = 'utf8'
    r.close()
    r = open(file, 'r', encoding=coding)
    l = r.readlines()

w = open(file, 'w', encoding=coding)
r = open(file, 'r', encoding=coding)


def del_file():
    return open(file, 'w', encoding=coding)


def again_read_file():
    return open(file, 'r', encoding=coding)


while True:
    if first_file_open:
        w.writelines(l)
        first_file_open = False
    else:
        w.close()
        w = del_file()
        w.writelines(l)
    command = input()
    cmd = command
    if cmd == ':S':
        w.writelines(l)
        w.flush()
    elif cmd == ":X":
        exit()
    elif cmd == ':D':
        w = del_file()
    elif cmd == ':R':
        l = []
    elif cmd == ":O":
        print("选择一个")
        numbers = -1
        for back in file_path:
            numbers += 1
            print(numbers, "\t\t\t" + back)
        try:
            use_file = int(input())
        except ValueError:
            print("请输入数字")
            continue
        else:
            if use_file > numbers or use_file < 0:
                print("数字过界")
            file = file_path[use_file]
            w.writelines(l)
            w.flush()

            if exists(file):
                r = open(file, 'rb')
                coding = chardet.detect(r.read()).get('encoding')
                r.close()
                r = again_read_file()
                l = r.readlines()
            w = del_file()
            r = again_read_file()
            print("成功切换")
            continue
    elif cmd == ':OX':
        print("选择一个")
        numbers = -1
        for back in file_path:
            numbers += 1
            print(numbers, "\t\t\t" + back)
        use_file = int(input())
        file = file_path[use_file]
        if exists(file):
            r = open(file, 'rb')
            coding = chardet.detect(r.read()).get('encoding')
            r.close()
            r = again_read_file()
            l = r.readlines()
        w = del_file()
        r = again_read_file()
        print("成功切换")
        continue
    elif cmd == ":PATH":
        print("当前路径为：" + abspath(file) + "\\" + file)
    elif cmd == ':ECHO>>FILE':
        echo_mode = False if echo_mode else True
    elif cmd == ':C':
        index = -1
        print('为防止:M&:MC功能导致行数溢出，已经将index变量设为-1')
        try:
            clear_line = int(input("输入清除的行"))
        except ValueError:
            print('输入非数字')
            continue
        try:
            l.pop(clear_line)
        except IndexError:
            print("数字超出范围")
        else:
            print('清除完成')
    elif cmd == ':ADD_OTHERS_FILE':
        file_path.append(input("输入要添加的文件路径:"))
    elif cmd == ':M':
        try:
            index = int(input())
        except ValueError:
            print('输入非数字')
        else:
            try:
                l[index]
            except ValueError:
                index = -1
                print('索引越界')
            else:
                print('修改完成')
    elif cmd == ':G':
        l = r.readlines()
    elif cmd == ':G1':
        clone_back_input = input('B为还原,C为备份,其他键为取消')
        if clone_back_input == 'B':
            l = l1
        elif clone_back_input == 'C':
            l1 = l
        else:
            print('已取消')
            continue
    elif cmd == ':G2':
        clone_back_input = input('B为还原,其他键为取消')
        if clone_back_input == 'B':
            l = l2
        else:
            print('已取消')
            continue
    elif cmd == ':PL':
        print(l)
    elif cmd == ':U':
        sys_i = input('要使用的命令')
        system_log = popen(sys_i)
    elif cmd == ':PU':
        print(system_log.read())
    elif cmd == ':PS':
        s_b_i = -1
        s_b_i_i = -1
        for back_in in l:
            s_b_i += 1
            for s_back_in in back_in:
                print(s_back_in, end=' ')
            for s_back_in in back_in:
                s_b_i_i += 1
                print(s_b_i_i, end=' ')
            print('')
            s_b_i_i = -1
    elif cmd == ':MC':
        try:
            index_l = int(input("输入行数:"))
        except ValueError:
            print('输入非数字')
            continue
        try:
            str_chr_l = l[index_l]
        except IndexError:
            print('索引越界')
            continue
        index = index_l
        try:
            index_c = int(input("输入字符索引:"))
        except ValueError:
            print('输入非数字')
            index_c = -1
            continue
        try:
            char_chr_l = str_chr_l[index_c]
        except IndexError:
            print('索引越界')
            index_c = -1
            continue
    elif cmd == ':WT':
        web_text_url = input('请输入url:')
        out_web_text_pathname = input('请输入下载后的文件路径(附名称):')
        download(url=web_text_url, out=out_web_text_pathname)
        file_path.append(out_web_text_pathname)
        print('已经下载完毕,并且加入file_list，序号为' + str(file_path.index(out_web_text_pathname)))
    elif cmd == ':DIR':
        system('dir')
    elif command == ':CLEAR_WINDOW' or command == ':CW':
        if name == 'nt':
            system('cls')
        elif name == 'posix' or name == 'cygwin':
            system('clear')
        else:
            print('其他环境不支持清屏,请手动执行命令')
    elif command == ':H':
        print(help_text)
    elif command == ':P':
        for back_in in l:
            print(back_in)
    elif command == ':PM':
        index_l = -1
        for back_in in l:
            index_l += 1
            print(str(index_l) + "\t\t\t" + back_in)
    elif command == ':XLSX':
        print('请输入文件编号:', end='')
        try:
            n_xlsx = int(input(''))
            p_xlsx = file_path[n_xlsx]
        except IndexError:
            print('索引越界')
            continue
        except ValueError:
            print('非数字')
            continue
        else:
            if not exists(p_xlsx):
                del_file().close()
            else:
                xlsx_workbook = openpyxl.load_workbook(p_xlsx)
                workbook_sheets = xlsx_workbook.sheetnames
                for wb_sheet_names in workbook_sheets:
                    l2.append(wb_sheet_names)

    else:
        if echo_mode:
            system("echo " + file + " >> " + command)
        else:
            if index_c == -1:
                l.insert(index, command + "\n")
            else:
                l.pop(index)
                l.insert(index, l[index][0:index_c] + command + l[index][index_c:-1] + "\n")
