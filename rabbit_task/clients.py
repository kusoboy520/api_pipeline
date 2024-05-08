import pika
import redis
import logging

logging.basicConfig(filename='./log/rabbit.log', encoding='utf-8', level=logging.DEBUG)

class PikaClient:
    '''
    Connect to RabbitMQ server
    hint: you should check conn_check==True first
    '''
    def __init__(self, username='rabbitmq', password='rabbitmq', durable=True):
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
        try:
            self.connection = pika.BlockingConnection(parameters=parameters)
            self.conn_check = self.connection.is_open
            self.channel = self.connection.channel()
            self.durable = durable
            logging.info('rabbit server connect success')
        except Exception as _:
            print('Connection failed')
            self.conn_check=False

    def MessageSender(self, queue_name, body, exchange='', routing_key=''):
        self.channel.queue_declare(queue=queue_name, durable=self.durable)
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body
        )
        self.channel.close()
        self.connection.close()

    def MessageConsume(self, queue_name, exchange='', routing_key='' ):
        self.channel.queue_declare(queue=queue_name, durable=self.durable)
        queue = self.channel.queue_declare(queue=queue_name, durable=self.durable)
        n = queue.method.message_count
        all_messages = []
        if n>0:
            for i in range(n):
                method, property, body = self.channel.basic_get(queue=queue_name, auto_ack=True)
                all_messages.append(body)
            self.channel.close()
            self.connection.close()
        return all_messages
    
def redisClient(host='localhost', port=6379, db=0):
    '''connect to redis db'''
    redis_pool = redis.ConnectionPool(
        host=host, 
        port=port, 
        db=db,
        decode_responses=True
    )
    r = redis.StrictRedis(connection_pool=redis_pool)
    return r
    




