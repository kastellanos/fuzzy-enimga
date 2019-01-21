from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from cassandra.cluster import Cluster


def lambdatrait(rdd):

    rdd.foreach(lambda record: sendCassandra(record))

def sendCassandra(record):
    cs_cluster = Cluster(['cassandra'])
    cs_session = cs_cluster.connect('sdtd')
    cs_session.execute("INSERT INTO MYDATA (id, level , projected_hour  , x  ,y  ,value ,category  ,area  ,  element ,reference_year ,reference_month ,reference_day ,reference_hour ,reference_minute,ville) VALUES(%s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ) ",[record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9],record[10],record[11],record[12],record[13],record[14]])


sc = SparkContext(appName="PythonSparkStreamingKafka")
sc.setLogLevel("WARN")

ssc = StreamingContext(sc,20)

kafkaStream = KafkaUtils.createStream(ssc, 'zoo1:2181', 'spark-streaming', {'topic':1})

lines = kafkaStream.map(lambda x: x[1].split(",")).foreachRDD(lambdatrait)

ssc.start()
ssc.awaitTermination()
