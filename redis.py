#!/usr/bin/python3

import os
import sys
import json
import paramiko
import subprocess
import time
import logging
from configparser import ConfigParser
from utils import utilParamikoShell
from utils import utilParamikoSftp
from utils import utilLog

class redisOperation(object):
    def __init__(self):
        configFileAbsPath = os.path.join(sys.path[0], "redis_config.ini")
        if not os.path.exists(configFileAbsPath):
            logging.error("配置文件丢失:{}".format(configFileAbsPath))
            sys.exit(1)
        else:
            cp = ConfigParser()
            cp.read(configFileAbsPath, encoding='UTF-8')

        self.redisinfo = {
            "deployPath" : cp.get('redis', 'deployPath'),
            "filePath": cp.get('redis', 'filePath'),
            "IP": cp.get('redis', 'IP'),
            "sshdport": cp.get('redis', 'sshdport'),
            "username": cp.get('redis', 'username'),
            "password": cp.get('redis', 'password'),
            "redisport": cp.get('redis', 'redisport'),
            "logpath": cp.get('redis', 'logpath'),
            "redisVersion": cp.get('redis', 'redisVersion'),
            "redisCluster": cp.get('cluster', 'redisCluster'),
            "redisCliPath": cp.get('cluster', 'redisCliPath'),
            "redisCliIP": cp.get('cluster', 'redisCliIP'),
            "redisCliPort": cp.get('cluster', 'redisCliPort'),
            "requirePass": cp.get('cluster', 'requirePass'),

        }
        print(self.redisinfo)
        try:
            self.shell = utilParamikoShell(self.redisinfo["IP"], self.redisinfo["sshdport"],
                                self.redisinfo["username"], self.redisinfo["password"])
        except Exception as e:
            print("创建与目标服务器的SSH连接失败,详情如下:" + str(e))
            sys.exit(1)

        try:
            self.sftp, self.trans = utilParamikoSftp(self.redisinfo["IP"], int(self.redisinfo["sshdport"]),
                                self.redisinfo["username"], self.redisinfo["password"])
        except Exception as e:
            print("创建与目标服务器的Sftp连接失败,详情如下:" + str(e))
            sys.exit(1)

        self.logger = utilLog()

    def closeShell(self):
        #关闭shell链接
        self.shell.close()

    def closeSftp(self):
        #关闭SFTP连接
        self.trans.close()

    def setenv(self):
        #设置机器环境
        #关闭THP

        #修改系统允许的进程能打开的最大的文件数
        self.shell.exec_command('echo -e "*    soft    nofile    65536\n*    hard    nofile    65536" >> /etc/security/limits.conf')
        #重启等待连接
        return

    def deploygcc(self):
        #安装GUN组件用作后续编译部署用
        self.shell.exec_command('apt install -y build-essential')
        return

    def deployredis(self):
        self.setenv()
        self.deploygcc()
        #解压redis
        #编译
        #检查
        #配置渲染
        #导出结果
        return

    def addintocluster(self):
        #检测当前的redis是否已经运行，否则运行redis
        #操作加入集群
        print

    def deletefromcluster(self):
        #操作从集群中剔除
        print

    # def startredis():)
    #     #启动redis
    #     return
    #
    # def stopredis():
    #     #关闭redis
    #     return
    #
    # def restartRedis

if __name__ == '__main__':
    print
