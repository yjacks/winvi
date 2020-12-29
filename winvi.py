from os import system, name
from os.path import exists, abspath
from sys import exit, argv

system_log=''
echo_mode = False
file_path = []
l = []
l1 = []
index = -1
help_text="""
    欢迎使用新的winvi
    新的winvi打开二进制文件会直接退出
    使用帮助：
    输入:COMMAND进入命令编辑模式：
        命令用法：
            :S 保存缓存修改
            :X 退出
            :O 切换编辑的文件(默认为第一个命令参数的文件)(保存文件)
            :OX 强制切换文件
            :G 将文件现有内容加载至缓存
            :G1 将目前的修改存放至缓存
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
            :EXIT_COMMAND,:EC 退出命令模式

    独立指令:
    :H 输出本帮助（等效－h参数）
    :P 输出文件内容
    :PM 输出文件内容(前加序号)
    :CLEAR_WINDOW,:CW 清屏
    """

if argv[0] == "python":
    argv.pop(0)

if len(argv) == 1:
    input_file_path = input("输入要打开的文件,:X退出:")
    if input_file_path == ":X":
        exit()
    else:
        file_path.append(input_file_path)
        argv.append(input_file_path)

if argv[1] == "-v":
    print('\t\twinvi version:1.1\n\t\tnew winvi')
    exit()
elif argv[1] == '-h':
    print(help_text)

argv.pop(0)
if len(argv) > 1:
    for file in argv:
        file_path.append(file)
else:
    file_path.append(argv[0])

file = file_path[0]
if exists(file):
    r = open(file, 'r')
    l = r.readlines()

w = open(file, 'w')
r = open(file, 'r')

while True:
    command = input()
    if command == ":COMMAND":
        print('成功进入COMMAND模式')
        while True:
            cmd = input()
            if cmd == ':S':
                w.writelines(l)
                w.flush()
            elif cmd == ":X":
                exit()
            elif cmd == ':D':
                w = open(file, 'w')
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
                    if exists(file):
                        r = open(file, 'r')
                        l = r.readlines()
                    w = open(file, 'w')
                    r = open(file, 'r')
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
                    r = open(file, 'r')
                    l = r.readlines()
                w = open(file, 'w')
                r = open(file, 'r')
                print("成功切换")
                continue
            elif cmd == ':EXIT_COMMAND' or cmd == ':EC':
                print('退出COMMAND模式')
                break
            elif cmd == ":PATH":
                print("当前路径为：" + abspath(file) + "\\" + file)
            elif cmd == ':ECHO>>FILE':
                echo_mode = False if echo_mode else True
            elif cmd == ':C':
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
                clone_back_input = input('B为还原,C为备份')
                if clone_back_input == 'B':
                    l = l1
                elif clone_back_input == 'C':
                    l1 = l
            elif cmd == ':PL':
                print(l)
            elif cmd == ':U':
                system_log=system(input('输入指令'))
            elif cmd == ':PU':
                print(system_log)
            else:
                print('输入非指令')

    # 退出COMMAND范畴
    elif command == ':CLEAR_WINDOW' or command == ':CW':
        if name == 'nt':
            system('cls')
        elif name == 'posix':
            system('clear')
        else:
            print('Java虚拟机(Jython)暂不支持清屏')
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
    else:
        if echo_mode:
            system("echo " + file + " >> " + command)
        else:
            l.insert(index, command + "\n")
