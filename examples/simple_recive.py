import pika

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
credentials = pika.PlainCredentials('public_user', 'CH3COONA')
parameters = pika.ConnectionParameters('rabbitmq.selfmade.ninja',
                                        5672,
                                       'eswaraprasath_hello_world',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='My_first_queue')

channel.basic_consume(queue='My_first_queue',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
print("he")

