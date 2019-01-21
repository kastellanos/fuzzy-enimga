from cassandra.cluster import Cluster
from kafka import KafkaProducer, KafkaConsumer
import csv
import json
import time

def translate(s):
    if s["category"] == "wspd":
        s["category"] = "Wind Speed"
        s["value"] = str( float(s["value"])*0.514444 )
    if s["category"] == "temp":
        s["category"] = "Temperature"
        s["value"] = str( (float(s["value"])-32)*(5/9) )
    if s["category"] == "snow":
        s["category"] = "Total snow "
        s["value"] = str( float(s["value"])*25.4 )
    if s["category"] == "qpf":
        s["category"] = "Total precipitation"
        s["value"] = str( float(s["value"])*25.4 )
    return s
cluster = Cluster(['cassandra'])

session = cluster.connect('sdtd')

consumer = KafkaConsumer('topicA',
                         bootstrap_servers=['kafka-service:9092'],value_deserializer=lambda m: json.loads(m.decode('ascii')))

producer = KafkaProducer(bootstrap_servers='kafka-service:9092')


for message in consumer:
    print(message.value)
    if "ville" in message.value:

        rows = session.execute("SELECT reference_month,reference_day,reference_hour,element,value from sdtd.weather where ville='{}' allow filtering".format(message.value["ville"]))
        i = 0
        roww = []
        for row in rows:

            x = {"day":row[1], "hour":row[2], "category":row[3],"value":row[4]}
            roww.append(x)
        print(roww)
        roww = sorted(roww, key=lambda i: (int(i["day"]),int(i["hour"])))
        for row in roww:
            time.sleep(1)
            print(row)

            producer.send('livetemperature', json.dumps([translate(row)]).encode('utf-8'))
            if i==10:
                break
            i +=1
        producer.flush()
    else:
        # {'month': '6', 'year': '2017', 'maximum': '25', 'type': 'temp', 'minimum': '12', 'day': '21'}
        k = message.value
        rows = session.execute("SELECT ville,element, value,reference_year,reference_day,reference_month,reference_hour from sdtd.weather where reference_year='{}' and reference_month='{}' and reference_day='{}' and element = '{}' allow filtering".format(k["year"],k["month"],k["day"],k["type"]))
        i = 0
        roww = []
        t = {}
        for row in rows:
            if row[0] not in t:
                t[row[0]] = {"ville":row[0], "category":row[1], "value":float(row[2]),"hour":row[6],"count_hours":1}
            else:
                t[row[0]]["value"] += float(row[2])
                t[row[0]]["count_hours"] += 1


        oo = []
        for h in t.keys():
            t[h]["value"]= str(t[h]["value"]/ t[h]["count_hours"])
            oo.append(t[h])
        #print(oo)
        roww = sorted(oo, key=lambda i: (i["ville"],int(i["hour"]),float(i["value"])))
        for row in roww:
            row = translate(row)

            if float(row["value"]) >= float(k["minimum"]) and float(row["value"]) <= float(k["maximum"]):
                print(row)
                time.sleep(1)
                producer.send('livetemperature', json.dumps([row]).encode('utf-8'))

        producer.flush()
