#!/usr/bin/python
#coding:utf-8


'''
zoom : sub_1017117c4断下后 frp即可出来temp_8的结果

'''

import lldb
import commands
import optparse
import shlex
import re


# 获取ASLR偏移地址
def get_ASLR():
    # 获取'image list -o'命令的返回结果
    interpreter = lldb.debugger.GetCommandInterpreter()
    returnObject = lldb.SBCommandReturnObject()
    interpreter.HandleCommand('image list -o', returnObject)
    output = returnObject.GetOutput()
    # 正则匹配出第一个0x开头的16进制地址
    match = re.match(r'.+(0x[0-9a-fA-F]+)', output)
    if match:
        #print('ALSR',match.group(1))
        return match.group(1)
    else:
        return None

# 计算str变成数值相减
def cal_minus(a,b):
    return hex(int(a,16) - int(b,16))


# 计算bt的ida偏移地址
def get_offset_bt():
    # 获取'bt'命令的返回结果
    interpreter = lldb.debugger.GetCommandInterpreter()
    returnObject = lldb.SBCommandReturnObject()
    interpreter.HandleCommand('bt', returnObject)
    output = returnObject.GetOutput()
    
    
    # print(f"Find all: {_} Output: [{output}] Type: {type(output)}")
    # 基址
    base_address = get_ASLR()
    
    #技术符号，区分是否当前线程
    count = 0;
    # 正则匹配出以 【16进制地址开头】，以【`】结尾的str
    for i in re.findall('0x[0-9a-fA-F]{16}.*?(?:`)', output):
        # 以表示符分离正则匹配结果
        match = re.split(r'\x1b\[0m \x1b\[36m', i, 1)
        # 以表示符分离正则匹配结果
        match = [match[0], re.split(r'\x1b\[39m', match[1], 1)[0]]
        if match:
            if count == 0:
                print('\033[0;31m *\033[0m',f'  frame #{count}:\t',cal_minus(match[0],base_address), '\033[0;36m '+ str(match[1])+ '\033[0m')
            else:
                print(f'     frame #{count}:\t',cal_minus(match[0],base_address), '\033[0;36m '+ str(match[1])+ '\033[0m')
            # 自增1
            count += 1;
        else:
            print('error: no finding match...:')


# main函数
def find_frame_offset(debugger, command, result, internal_dict):
    # get_ASLR()
    get_offset_bt()

#计算指定command_address在ida中的偏移地址
def find_offset(debugger, command, result, internal_dict):
    # 获取基址
    base_address_0 = get_ASLR()
    
    #用户是否输入了地址参数
    if not command:
        print(result, 'Please input the address!')
        return
    # 计算偏移地址
    offset_address = cal_minus(command,base_address_0)
    # 判断偏移地址是否存在
    if int(offset_address,16) > 0:
        #如果找到了command偏移，就打印输出
        print('\033[0;31m' +  str(offset_address)+'\033[0m')
    else:
        print('The address entered is incorrect!')
    

#显示所有寄存器值
def read_re(debugger, command, result, internal_dict):
    # 执行're r'命令
    debugger.HandleCommand('re r')


#一旦Python模块被加载到LLDB中时它就会被调用s
def __lldb_init_module(debugger, internal_dict):
#    # 'command script add sbr' : 给lldb增加一个'sbr'命令
#    # '-f lldb_about.sbr' : 该命令调用了lldb_about文件的sbr函数
#    # -f参数表明你想要绑定一个Python函数命令.
#    # 也可以写成 command script add -f lldb_about.sbr sbr

    debugger.HandleCommand('process connect connect://127.0.0.1:8888')
    print('process connect connect://127.0.0.1:8888')

    debugger.HandleCommand('command script add gbt -f offset_bt.find_frame_offset')
    print('The "gbt" python command has been installed and is ready for use.')
    
    debugger.HandleCommand('command script add fo -f offset_bt.find_offset')
    print('The "fo" python command has been installed and is ready for use.')
    
    debugger.HandleCommand('command script add rr -f offset_bt.read_re')
    print('The "rr" python command has been installed and is ready for use.')
    

