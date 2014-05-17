import MySQLdb
import datetime
import sys 
# Connessione al database e setup cursor

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="hackaton")
cursor = db.cursor()

#Raccolgo inof

giornilist = ['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica']
giorno = giornilist[datetime.date.today().weekday()]
ora = datetime.datetime.now().strftime("%H:%M:%S")
if giorno == 'sabato' or giorno == 'domenica':
    print "E' il weekend, non ci sono lezioni!"
    sys.exit()

macroarea = raw_input('Che corso di laurea stai seguendo? ')

#Define query SQL & fetch

sql = "SELECT * FROM %s WHERE macroarea = '%s'" % (giorno, macroarea)
cursor.execute(sql)
risultato = cursor.fetchall()

def corsiora(): #Lista delle lezioni in corso in questo momento

    for i in risultato: 
        corso = i[0]
        macro = i[1]
        orario = i[2]
        aula = i[3]
        durata = i[4]
        fine = orario + durata
        if orario < ora < orario + durata:
            print "In aula %s c'e' un corso di %s fino alle %s" % (aula, corso, fine)

def aulelibere(): #Lista delle aule libere
    print "Le aule libere sono: \n"
    for i in risultato:    
        corso = i[0]
        macro = i[1]
        orario = i[2]
        aula = i[3]
        fine = i[4]
        if not orario < ora < orario + durata:
            print aula, "\n"
    

ask = raw_input("Cosa vuoi sapere? (Inserisci il numero e premi invio) \n 1. Quali lezioni sono in corso \n 2. Le aule libere\n")
if ask == "1":
    print corsiora()
elif ask == "2":
    print aulelibere()

db.close()