#!/usr/bin/python3.6

import paramiko
import subprocess
import logging
import os
import sys
import socket
import hashlib

def utilLog():
    logger = logging.getLogger('updateNotice')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.formatter = formatter
    logger.addHandler(console_handler)
    logFileAbsPath = os.path.join(sys.path[0], "redisOperation.log")
    file_handler = logging.FileHandler(logFileAbsPath)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def utilFilepath(file):
    path = os.path.join(sys.path[0], file)
    return path

def utilgetAllFile(dir):
    filelist = []
    for home, dirs, files in os.walk(dir):
        # for dir in dirs:
        #     print(dir)
        for file in files:
            if file.endswith(('yml', 'yaml')):
                fullname = os.path.join(home, file)
                filelist.append(fullname)
    return filelist

def utilgetIPhostname():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return hostname, ip

def utilHashmd5(filepath):
    if not os.path.isfile(filepath):
        return
    myHash = hashlib.md5()
    f = open(filepath, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myHash.update(b)
    f.close()
    return myHash.hexdigest()

def utilSubprocess(ip):
    p = subprocess.Popen(['ping', '-c', '3'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, strerr = p.communicate(input=ip)
    if p.returncode is 0:
        print("pong!")
    else:
        print("pang!")
    # while True:
    #     testSubprocess(input("test ping host ip:"))

    #Popen执行成功是返回执行结果，执行失败无任何返回
    #call基于Popen,成功时返回0，失败时返回1
    #check_call基于call,成功时返回0，失败的时候返回一个traceback
    #check_output基于run，run基于Popen,成功时返回执行结果，失败时返回traceback
    print(subprocess.Popen(["cat", "hosts"], cwd="/etc"))
    hostname = subprocess.check_output("hostname")
    print(hostname)
    print(subprocess.check_output("netstat -ntlp| grep ssh", shell=True))
    retcode = subprocess.call("ping -c 1 www.baidu.com", shell=True)
    print(retcode)
    print(subprocess.check_call(["ping", "www.baidu.com", "-c", "3"]))

def utilParamikoShell(hostIP, port, username, password):
    #定义一个shell连接
    shell = paramiko.SSHClient()
    shell.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    shell.connect(hostname=hostIP, port=port, username=username, password=password,
                    look_for_keys=False, allow_agent=False)
    return shell

def utilParamikoSftp(hostIP, port, username, password):
    # 定义一个sftp连接
    trans = paramiko.Transport((hostIP, port))
    trans.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(trans)
    return sftp, trans

if __name__ == '__main__':
    print("演示样例")
    # shell = utilParamikoShell("192.168.110.128", 22, "root", "111111")
    # stdin, stdout, stderr = shell.exec_command("hostname")
    # print(stdout.read().decode('utf-8'))
    # shell.close()

    # sftp, trans = utilParamikoSftp("192.168.110.128", 22, "root", "111111")
    # path = os.path.join(sys.path[0], 'utils.py')
    # sftp.put(path, '/usr/local/utils.py')
    
    
