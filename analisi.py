import serial, json, MySQLdb, datetime, time, sys, os
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

#Infos

giornilist = ['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica']
giorno = giornilist[datetime.date.today().weekday()]

if giorno == 'sabato' or giorno == 'domenica':
    print "E' il weekend, non ci sono lezioni!"
    sys.exit()

#Chiamo tutti gli eventi legati all'aula dal database
    
cursor.execute("SELECT * FROM %s WHERE aula = 'G2C'" % (giorno)) 
corsi = cursor.fetchall()

print "Informazioni Aula G2C \nLezioni giornaliere: \n"

for i in corsi:    
    corso = i[0]
    macro = i[1]
    orario = i[2]
    aula = i[3]
    fine = i[4]
    print corso, "(", orario, "-", fine, ")"

print  "\n ===================== \n"

'''
#Lettura temperatura esterna tramite OpenWeatherMap API

meteor = urlopen('http://api.openweathermap.org/data/2.5/weather?id=4219762')
meteo = load(meteor)
temp = int((meteo['main']['temp_max'] + meteo['main']['temp_min'])/2 - 273.15) #Media max e min + conversione in C + float to int
umidita = meteo['main']['humidity']

if temp > 25:
    #Spengi termosifoni
elif temp < 15:
    #Accendi termosifoni
else:
    pass
'''

ser = serial.Serial('COM4', 9600) #Apro connessione Arduino
data = ser.readline() #Leggo il serial fino al primo /n

#Check temperatura


def checktemp():
    statust = "Ok"

    if int(data[0:2]) in range(21,26):
        #Temperatura ok, non invio nulla
        statust = "Ok"

    elif int(data[0:2]) < 20:
        #Alert freddo

        statust = "Freddo"

    elif int(data[0:2]) > 26:
        #Alert caldo

        statust = "Caldo"
    return statust

statust = checktemp()

#Check luce


def checkluce():
    statusl = "Ok"
    if int(data[2:6]) in range(400, 600):
        #Luce ok, non invio nulla
        statusl = "Ok"
    elif int(data[2:6]) < 400:
        #Alert bassa luce
        statusl = "Meno del normale"
        #Alza serrande
    elif int(data[2:6]) > 600:
        #Sensore in prossimita' di una luce
        statusl = "Sensore mal posizionato"
    return statusl

statusl = checkluce()

tweet = "Lezione: Hackaton | Temperatura: %s C | Illuminazione: %s | " % (data[0:2], statusl) + ts
twyapi.update_status(status=tweet)

#Setto un intervallo di n minuti tra ogni call
#Le informazioni in questo modo sono aggiornate di continuo

while True:
    print "Informazioni Aula G2C \n\nLezioni giornaliere: \n"

    for i in corsi:    
        corso = i[0]
        macro = i[1]
        orario = i[2]
        aula = i[3]
        fine = i[4]
        print corso, "(", orario, "-", fine, ")"

    print  "\n ===================== \n"
    checkluce()
    checktemp()
    print "Stato temperatura: %s" % (statust), "(",data[0:2],"C)", "\nIlluminazione: %s \n" % (statusl)
    print "Ultimo update", datetime.datetime.now().strftime("%H:%M:%S")
    time.sleep(600) #Misuro ogni 10 minuti
    os.system('cls')

db.close()
