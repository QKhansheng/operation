#!/usr/bin/python3

from rabbitmq_producer import createChannel

def msg_consumer(channel, method, properties, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == "quit":
        channel.basic_cancle(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        print(body)
    return

if __name__ == '__main__':
    #获取连接信道
    channel = createChannel()
    #声明持久化交换器hello-exchange
    channel.exchange_declare(exchange="hello-exchange", exchange_type="topic", passive=False,
                             durable=True, auto_delete=False)
    #声明持久化队列hello-queue,并将镜像模式的参数传递给该队列
    queue_args = {"x-ha-policy" : "all"}
    channel.queue_declare(queue="hello-queue", arguments=queue_args)
    #声明队列和交换器的绑定
    channel.queue_bind(queue="hello-queue", exchange="hello-exchange", routing_key="hello")
    #订阅消费者
    channel.basic_consume(queue="hello-queue",on_message_callback=msg_consumer,
                          consumer_tag="hello-consumer")
    #开始消费
    channel.start_consuming()
