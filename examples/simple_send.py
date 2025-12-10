import pika

credentials = pika.PlainCredentials('public_user', 'CH3COONA')
parameters = pika.ConnectionParameters('rabbitmq.selfmade.ninja',
                                        5672,
                                       'eswaraprasath_hello_world',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='My_first_queue')
channel.basic_publish(exchange='',
                      routing_key='My_first_queue',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

