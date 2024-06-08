import random
import numpy as np
import mysql.connector
import pandas as pd



dane_moto = pd.read_csv('data/uslugi_motocyklowe.csv')
uslugi_moto = dane_moto['Usluga']
cena_moto = dane_moto['Cena']


dane_auto = pd.read_csv('data/uslugi_samochodowe.csv')
uslugi_auto = dane_auto['Usluga']
cena_auto = dane_auto['Cena']


#####################################

uslugi = []

for i in range(len(dane_moto)):
    typ = str("motocykl")
    nazwa = uslugi_moto[i]
    koszt = int(cena_moto[i])
    uslugi.append((typ, nazwa, koszt))

for i in range(len(dane_auto)):
    typ = str("samochod")
    nazwa = uslugi_auto[i]
    koszt = int(cena_auto[i])
    uslugi.append((typ, nazwa, koszt))

####################################

con = mysql.connector.connect(
    host = "giniewicz.it",
    user = "team11",
    password = "te@m24ii",
    database = "team11"
)

if(con):
    print("Połączenie udane")
else:
    print("Połączenie nieudane")

mycursor = con.cursor()


mycursor.execute("DROP TABLE IF EXISTS uslugi")

sql ='''CREATE TABLE uslugi(
   id_uslugi INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
   typ_uslugi VARCHAR(40) NOT NULL,
   nazwa_uslugi VARCHAR(80) NOT NULL,
   koszt_uslugi INT UNSIGNED
);'''
mycursor.execute(sql)

for usluga in uslugi:   
    insert = (
        "INSERT INTO uslugi(typ_uslugi, nazwa_uslugi, koszt_uslugi)"
        "VALUES (%s, %s, %s)"
    )
    try:
        print(usluga)
        mycursor.execute(insert, usluga)
        con.commit()
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
        con.rollback()


mycursor.close()
con.close()