import json
from kafka import KafkaProducer
import time
producer = KafkaProducer(bootstrap_servers = ['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
producer.send('testtopic', {'aaa':'bbb'})

time.sleep(10)