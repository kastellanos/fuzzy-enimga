from kafka import KafkaProducer
import csv
import time
producer = KafkaProducer(bootstrap_servers='kafka-service:9092')

with open('mydata.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    i = 0
    for row in spamreader:

        x = ', '.join(row)
        print x
        producer.send('topic', x)
        i +=1
        if i== 100:
            time.sleep(60)

    producer.flush()
