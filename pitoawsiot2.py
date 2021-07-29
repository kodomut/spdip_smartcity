#Program to read the values of Temp and Hum from the dht22 sensor and send it over to AWS-IOT
#reference from: https://circuitdigest.com/microcontroller-projects/publish-sensor-data-to-amazon-aws-raspberry-pi-iot

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient #Import from AWS-IoT Library
import time#To create delay
from datetime import date, datetime #To get date and time
import Adafruit_DHT #Import DHT Library for sensor

myMQTTClient = AWSIoTMQTTClient("new_Client")
myMQTTClient.configureEndpoint("a3jfoxtam7xsv1-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/cert2/CA.pem", "/home/pi/cert2/private.pem.key", "/home/pi/cert2/certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

sensor_name = Adafruit_DHT.DHT22 #we are using the dht22 sensor
sensor_pin = 4 #The sensor is connected to GPIO17 on Pi


connecting_time = time.time() + 10

if time.time() < connecting_time:  #try connecting to AWS for 10 seconds
    myMQTTClient.connect()
    myMQTTClient.publish("dht22/info", "connected", 0)
    print ("MQTT Client connection success!")
else:
    print ("Error: Check your AWS details in the program")

    
time.sleep(2) #wait for 2 secs

while 1: #Infinite Loop
    timenumeric=time.time() #numericdatetime
    now = datetime.now() #get date and time 
    current_time = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] #get current time in string format  
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor_name, sensor_pin) #read from sensor and save respective values in temperature and humidity varibale  
    time.sleep(2) #Wait for 2 sec then update the values

    #prepare the payload in string format 
    payload = '{ "timestamp": ' + str(timenumeric) + ',"temperature": ' + str(temperature) + ',"humidity": '+ str(humidity) + ' ,"datetime":"'+ current_time + '"}'

    print (payload) #print payload for reference 
    myMQTTClient.publish("dht22/data", payload, 0) #publish the payload

    time.sleep(30) #Wait for 30 sec then update the values