#Program to read the values of Temp and Hum from the dht22 sensor and send it over to AWS-IOT
#reference from: https://circuitdigest.com/microcontroller-projects/publish-sensor-data-to-amazon-aws-raspberry-pi-iot

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient #Import from AWS-IoT Library
import time#To create delay
from datetime import date, datetime #To get date and time
#import Adafruit_CharLCD as LCD #Import LCD library 
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

#lcd_rs        = 7  #RS of LCD is connected to GPIO 7 on PI
#lcd_en        = 8  #EN of LCD is connected to GPIO 8 on PI 
#lcd_d4        = 25 #D4 of LCD is connected to GPIO 25 on PI
#lcd_d5        = 24 #D5 of LCD is connected to GPIO 24 on PI
#lcd_d6        = 23 #D6 of LCD is connected to GPIO 23 on PI
#lcd_d7        = 18 #D7 of LCD is connected to GPIO 18 on PI
#lcd_backlight =  0  #LED is not connected so we assign to 0

#lcd_columns = 16 #for 16*2 LCD
#lcd_rows    = 2 #for 16*2 LCD

#lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
#                           lcd_columns, lcd_rows, lcd_backlight)   #Send all the pin details to library 

#lcd.message('AWS-IoT with Pi \n -CircuitDigest') #Give a intro message
time.sleep(2) #wait for 2 secs
#lcd.clear() #clear the LCD

connecting_time = time.time() + 10

if time.time() < connecting_time:  #try connecting to AWS for 10 seconds
    myMQTTClient.connect()
    myMQTTClient.publish("dht22/info", "connected", 0)
    print ("MQTT Client connection success!")
    #lcd.message('Connected to \n AWS thing') #if connected
else:
    print ("Error: Check your AWS details in the program")
    #lcd.message('Error: \nInvalid details') #if not connected

    
time.sleep(2) #wait for 2 secs

while 1: #Infinite Loop
    timenumeric=time.time() #numericdatetime
    #now = datetime.now() #get date and time 
    #current_time = now.strftime('%Y-%m-%dT%H:%M:%S') #get current time in string format 
    #current_time = datetime.now().isoformat()
    now = datetime.now() #get date and time 
    current_time = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] #get current time in string format  
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor_name, sensor_pin) #read from sensor and save respective values in temperature and humidity varibale  
    #lcd.clear() #Clear the LCD screen
    #lcd.message ('Temp = %.1f C' % temperature) # Display the value of temperature
    #lcd.message ('\nHum = %.1f %%' % humidity)  #Display the value of Humidity
    time.sleep(2) #Wait for 2 sec then update the values

    #prepare the payload in string format 
    payload = '{ "timestamp": ' + str(timenumeric) + ',"temperature": ' + str(temperature) + ',"humidity": '+ str(humidity) + ' ,"datetime":"'+ current_time + '"}'

    print (payload) #print payload for reference 
    myMQTTClient.publish("dht22/data", payload, 0) #publish the payload
    
    #lcd.clear() #Clear the LCD screen
    #lcd.message ('Published to \n  AWS-IOT') # Display the value of temperature

    time.sleep(30) #Wait for 30 sec then update the values