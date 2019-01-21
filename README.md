# Table of Contents
1. [Introduction](#introduction)
2. [Simulateur de données en temps réel](#simulateur)
3. [Connector spark-kafka-cassandra db](#spark)
4. [Connector kafka-cassandra webapp](#spark)
5. [Webapp](#webapp)

## 1. Introduction

Nous allons decrire dans les prochaine sections les fichiers et la facon de construire les images qu'on a utilisé pour le projet.

## 2. Simulateur de envoie des données en temps réel

Pour l'envoie de données nous avons utilisé un script python qui envoie certain quantité de données chaque 60 seconde au lien du broker kafka service.

Pour construire et executer l'image il faut faire
```
docker build -t <nom-utilisateur-dockerhub>/simulateur .
docker run <nom-utilisateur-dockerhub>/simulateur
```
Cette image elle a pas besoin d'etre dans le cluster. Elle peux se communiquer avec kafka dehors le cluster. Par contre il faut modifier l'address a la main dans le script simulateur/src/sim.py.

## 3. Connector spark-kafka-cassandra db

L'image docker et sources fournis sont que pour montrer le travail fait. Car le source code il est deja dans une image docker disponible dans dockerhub car elle est necessaire pour le deployment automatique du cluster.

L'image que on a dans kafka_spark_cassandra elle fait le spark submit job qui crée automatiquement les noeuds spark dans kubernetes.


## 4. Connector kafka-cassandra webapp

On utilise un programme python pour repondre au requets du webapp.

docker build -t <nom-utilisateur-dockerhub>/webapp-responder .

L'image est utilisé par un fichier de configuration kubernetes qui la prends de dockerhub. Il y a pas besoin de faire docker run.

## 5. Webapp

### Build jar

To build image follow the [tuto](https://docs.aws.amazon.com/lambda/latest/dg/java-create-jar-pkg-maven-and-eclipse.html)
without the step 5

### Kafka address and topics

To modify the kafka address and topics go to the file located in resources/application.properties

### Local execution

After build

```
java -jar <jar_name>
```

### Docker

To build the docker image after build the jar copy the jar inside the docker folder and execute the command

```
docker build --build-arg JAR_FILE=<jar_name> -t kastellanos/webapp:1.0 .
docker run ...
```
