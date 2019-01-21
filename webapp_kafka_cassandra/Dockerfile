FROM python:3.6.7

RUN pip install cassandra-driver kafka

COPY src/kafca.py /
COPY src/run.sh /
RUN chmod +x /run.sh

ENTRYPOINT ["./run.sh"]
