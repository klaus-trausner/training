from umqtt.simple import MQTTClient
import secret
import machine
import ubinascii

mqttServer = secret.mqttAddress


clientID = ubinascii.hexlify(machine.unique_id())

mqttc = MQTTClient(clientID, mqttServer, port = secret.mqttPort, user = secret.user, password= secret.mqttPassword,keepalive=60)

