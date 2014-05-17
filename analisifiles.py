import serial, json, MySQLdb, datetime, time, sys
from urllib2 import urlopen
from json import load
from twython import Twython
from time import strftime

global countp  #
global statusl # Fix funzioni di check 
global statust #

#Setup Twitter
APP_KEY = 'YYSBOjOyGMv1PZjcaG31GSQKs'
APP_SECRET = 'OcuxPJIsPp8Jo1TUp4gWEvc3wqV9gpNnKIbQ39sysss8kXovgO'
ACCESS_KEY = '2500448047-2pkxZN4xyEGxtC6N58tZ5TWHsBGtiHGlvwAryoi'
ACCESS_SECRET = 'N0xfygXAeVM6XAa449vDzABvQEuwTuwhztHG9sreJIPCy'
CONSUMER_KEY = 'jBVWluOauKWgwvkR9anra0Xkj'
CONSUMER_SECRET = '9Kv0hoZSjpRE27RFdRBlKqppDE6HY1iXKQesOviahjC2vOuKxy'
twyapi = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

#Connessione MySQL

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="hackaton")
cursor = db.cursor()

#Info sull'aula

giornilist = ['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica']
giorno = giornilist[datetime.date.today().weekday()]

if giorno == 'sabato' or giorno == 'domenica':
    print "E' il weekend, non ci sono lezioni!"
    sys.exit()


cursor.execute("SELECT * FROM %s WHERE aula = 'G2C'" % (giorno)) 
corsi = cursor.fetchall()

print "Lezioni giornaliere: \n", corsi


#Lettura temperatura esterna tramite OpenWeatherMap API

meteor = urlopen('http://api.openweathermap.org/data/2.5/weather?id=4219762')
meteo = load(meteor)
temp = int((meteo['main']['temp_max'] + meteo['main']['temp_min'])/2 - 273.15) #Media max e min + conversione in C + float to int
umidita = meteo['main']['humidity']

ser = serial.Serial('COM4', 9600) #Apro connessione Arduino
data = ser.readline() #Leggo il serial fino al primo /n

#Check temperatura

statust = "Ok"

def checktemp():

    if int(data[1:3]) in range(21,26):
        #Temperatura ok, non invio nulla
        statust = "Ok"

    elif int(data[1:3]) < 20:
        #Alert freddo
        twyapi.update_status(status="Nell'aula G2C la temperatura e' scesa")
        statust = "Freddo"

    elif int(data[1:3]) > 26:
        #Alert caldo
        twyapi.update_status(status="Nell'aula G2C la temperatura e' troppo alta")
        statust = "Caldo"

#Check luce

statusl = "Ok"

def checkluce():

    if int(data[4:7]) in range(400, 700):
        #Luce ok, non invio nulla
        statusl = "Ok"
    elif int(data[4:7]) < 400:
        #Alert bassa luce
        twyapi.update_status(status="Nell'aula G2C c'e' poca luce")
        statusl = "Meno del normale"
    elif int(data[4:7]) > 700:
        #Sensore in prossimita' di una luce
        twyapi.update_status(status="Nell'aula G2C il sensore e' mal posizionato")
        statusl = "Sensore mal posizionato"

countp = 0

def checkpass(): #Vedo quanti 
    if int(data[0]) == 1:
        countp += 1
    

start = time.time()
if time.time() < start + 300:
    checkpass()
else:
    if 2 * countp > 60:
        twyapi.update_status(status="L'aula G2C si sta riempiendo")

print "Informazioni Aula G2C \n Stato temperatura: %s \n Illuminazione: %s \n" % (statust, statusl)


#Setto un intervallo di 10 minuti tra ogni call

while True:
    checkluce()
    checktemp()
    time.sleep(600)

db.close()