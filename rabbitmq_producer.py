#!/usr/bin/python3

import pika
import os
import sys
import time
from configparser import ConfigParser

def getRabbitmqInfo():
    #获取配置信息写入rabbitmqInfo字典并返回
    configFileAbsPath = os.path.join(sys.path[0], "rabbitmq_config.ini")
    if not os.path.exists(configFileAbsPath):
        print("配置文件丢失:{}".format(configFileAbsPath))
        sys.exit(1)
    else:
        cp = ConfigParser()
        cp.read(configFileAbsPath, encoding='UTF-8')

    rabbitmqInfo = {
        "IP": cp.get('rabbitmq', 'IP'),
        "port": cp.get('rabbitmq', 'port'),
        "username": cp.get('rabbitmq', 'username'),
        "password": cp.get('rabbitmq', 'password'),

    }
    # print(rabbitmqInfo)
    # print(type(rabbitmqInfo["IP"]))
    return rabbitmqInfo

def createChannel():
    #连接rabbitmq，创建信道并返回信道
    rabbitmqInfo = getRabbitmqInfo()
    credentials = pika.PlainCredentials(username=rabbitmqInfo["username"],
                                        password=rabbitmqInfo["password"])
    conn_params = pika.ConnectionParameters(host=rabbitmqInfo["IP"],
                                            credentials=credentials)
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()

    #将消费确认传递给信道
    # def confirm_handler(frame):
    #     # 创建一个消费确认方法
    #     if type(frame.method) == spec.Confirm.SelectOk:
    #         logging.info("信道目前处于消费确认的模式")
    #     elif type(frame.method) == spec.Basic.Nack:
    #         if frame.method.delivery_tag in msg_ids:
    #             logging.error("消息丢失!")
    #     elif type(frame.method) == spec.Basic.Ack:
    #         if frame.method.delivery_tag in msg_ids:
    #             logging.info("消费者确认已经收到了消息")
    #             msg_ids.remove(frame.method.delivery_tag)

    channel.confirm_delivery()
    return channel

if __name__ == '__main__':
    #生产者开始投递消息
    # msg = sys.argv[1]
    msg = "现在的时间是:" + str(time.time())
    msg_props = pika.BasicProperties(delivery_mode=2)
    msg_props.content_type = "text/plain"
    channel = createChannel()
    while True:
        channel.basic_publish(body=msg, exchange="hello-exchange",
                              properties=msg_props, routing_key="hello")
    channel.close