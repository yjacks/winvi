# 一个命令行文本处理软件
# coding:utf8
import sys  # 需要用到两个函数
from os import makedirs
from os.path import exists, abspath

command = sys.argv  # 获取命令行
m = command[1]
"""
通过报出错误的方式进行隐式判断
"""
try:
    command[1]
except IndexError:
    print("没有文件可供打开")
    sys.exit()

# 没有多说的必要
try:
    r = open(m, mode='r', encoding='utf8')
except FileNotFoundError:
    w = open(m, mode='w', encoding='utf8')
    r = open(m, mode='r', encoding='utf8')
    w.close()

l = r.readlines()
w = open(m, mode='w', encoding='utf8')
h = '''
    欢迎使用WinVi
    ⚠警告！请不要用该工具打开二进制文件，否则后果自负！
    ⚠警告！已知Bug:再多次按:S时，会多次将内容复制,然后写入到文件，不会刷新缓存。
    按:S以保存进度,按:X以退出,
    按:N以跳行修改文件,按:D以清空文件
    按:R以清除缓存,按:P输出当前内容
    按:PA输出索引与内容,按:G手动缓存文件内容至缓存
    按:O以另存为,按:C以清除行,按:PH查看当前路径
'''
s = -1
fl = False

print(h)

while True:
    if not fl:
        w.writelines(l)
        fl = True
    i = input()

    if i == ':PA':
        if l:
            l = l
            s = -1
            for bv in l:
                s += 1
                print(str(s) + "    " + bv)
        else:
            s = None
            print("无内容")

    elif i == ':P':
        print(l)

    elif i == ':X':
        sys.exit()

    elif i == ':D':
        w = open(command[1], 'w', encoding='utf8')

    elif i == ':R':
        l = []

    elif i == ':S':
        w.writelines(l)
        w.flush()

    elif i == ':N':
        print("输入行数")
        try:
            n = int(input())
        except TypeError:
            print("输入非数字")
            continue

        try:
            k = l[n]
        except IndexError:
            print("超出行数")
            continue
        else:
            print(k)
            p = input("输入修改后的内容")
            l.pop(n)
            l.insert(n - 1 if l != [] or len(l) == 1 else 0, p + "\n")

    elif i == ':G':
        l = r.readlines()

    elif i == ':O':
        print("请输入文件路径(取消输入N)")
        m = input()
        if m == 'N':
            continue

        if not exists(m):
            print("文件不存在，是否创建？")
            no = input('Y为创建,其他为取消:')
            if no == 'y':
                try:
                    open(m, mode='w', encoding='utf8').close()
                    w = open(m, mode='w', encoding='utf8')
                    r = open(m, mode='r', encoding='utf8')
                except:
                    hj = abspath(m)
                    makedirs(hj)
                    open(m, mode='w', encoding='utf8').close()
                    w.close()
                    r.close()
                    w = open(m, mode='w', encoding='utf8')
                    r = open(m, mode='r', encoding='utf8')
            else:
                print("操作取消")
        else:
            w = open(m, mode='w', encoding='utf8')
            r = open(m, mode='r', encoding='utf8')
            print("操作成功")

    elif i == ':C':
        print("删除第几行？")
        try:
            vbd = int(input())
        except TypeError:
            print("输入非数字")
            continue
        try:
            l[vbd]
        except IndexError:
            print("行数错误")
        else:
            print("这是内容:" + l[vbd] + "是否删除？(Y)")
            pod = input()
            if pod == 'Y':
                l.pop(vbd)
                w = open(m, 'w', encoding='utf8')
                w.writelines(l)
                w.flush()
            else:
                print("操作取消")

    elif i==":PH":
        print(m)

    else:
        l.append(i + "\n")
