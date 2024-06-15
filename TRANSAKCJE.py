import re
import mysql.connector
import pandas as pd
import numpy as np
import math
import datetime

ranking = pd.read_excel("ranking_polska.xlsx", sheet_name="Data", skiprows = [0,1,2,3], usecols=[1,2,3,4])
marki = ranking["marka"]

cars = pd.read_csv("CarsData.csv", delimiter= ",")
cars = cars[cars["Make"].isin(marki)]

motocykle = pd.read_csv("BikeData.csv", delimiter= ",")


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

# POBIERANIE TABEL
mycursor = con.cursor()
mycursor.execute("SELECT * FROM pojazdy")
myresult = mycursor.fetchall()
pojazdy =pd.DataFrame(myresult)

mycursor.execute("SELECT id_części, cena FROM części")
myresult = mycursor.fetchall()
czesci =pd.DataFrame(myresult)

mycursor.execute("SELECT id_klienta, nip FROM klienci")
myresult = mycursor.fetchall()
klienci =pd.DataFrame(myresult)

mycursor.execute("SELECT * FROM uslugi")
myresult = mycursor.fetchall()
uslugi =pd.DataFrame(myresult)

id_klienta_naprawy = list(klienci[0])
powtorki = 68
indeksy_powtorek = np.random.randint(1, len(id_klienta_naprawy), size = powtorki)
for i in range(len(indeksy_powtorek)):
    powtorzony_klient = np.random.choice(id_klienta_naprawy[:indeksy_powtorek[i]])
    id_klienta_naprawy.insert(indeksy_powtorek[i], powtorzony_klient)

id_pojazdy_naprawy = id_klienta_naprawy #na razie potem trzeba będzie pozmieniać np. po sprzedaży 

ile_sprzedazy = 30

rng = np.random.default_rng()
id_pojazdu_sprzedaży = rng.choice(np.arange(1, len(klienci)), size = ile_sprzedazy, replace=False)
id_pojazdu_sprzedaży = sorted(id_pojazdu_sprzedaży)
data_zakupu = []
typ_transakcji_naprawy = ["naprawa"] * len(id_klienta_naprawy)

# TERAZ DATY ale tak jakby dla napraw, bo data zakupu to też data przyjęcia renowacji 
start = datetime.date(2022, 5, 1)
end = datetime.date(2024, 6, 5)

print((end - start).days)
step = int((end - start).days/ len(id_klienta_naprawy))
print(step)
dates = [start + datetime.timedelta(days = i*step + np.random.randint(-3, 3)) for i in range(len(id_klienta_naprawy))]

dates_zap = [dates[i]+ datetime.timedelta(days =  np.random.randint(1, 15)) for i in range(len(id_klienta_naprawy))]
id_kli_kupno = []
data_sprzedazy = []
for el in id_pojazdu_sprzedaży:
    indeksy = []
    for i in range(len(id_pojazdy_naprawy)):
        if el == id_pojazdy_naprawy[i]:
            indeksy.append(i)
    typ_transakcji_naprawy[indeksy[len(indeksy)-1]] = "renowacja"
    data_zakupu.append(dates[indeksy[len(indeksy)-1]])
    data_sprzedazy.append(dates_zap[indeksy[len(indeksy)-1]] + datetime.timedelta(days = np.random.randint(3, 15)))
print(id_klienta_naprawy)
print(typ_transakcji_naprawy)

id_pojazdy_naprawy = id_klienta_naprawy.copy()

for i in range(len(typ_transakcji_naprawy)):
    if(typ_transakcji_naprawy[i] == "renowacja"):
        id_kli_kupno.append(id_klienta_naprawy[i])
        id_klienta_naprawy[i] = None
#data_zakupu = sorted(data_zakupu)

#for el in data_zakupu:
    #data_sprzedazy.append(el + datetime.timedelta(days = np.random.randint(7, 60)))

for i in range(len(dates_zap)):
    if dates_zap[i]>datetime.date.today():
        dates_zap[i] = datetime.date.today() + datetime.timedelta(days = np.random.randint(-50, -20))


for i in range(len(data_sprzedazy)):
    if data_sprzedazy[i]>datetime.date.today():
        data_sprzedazy[i] = datetime.date.today() + datetime.timedelta(days = np.random.randint(-20, 0))
    

id_kli_sprz = []
for el in id_kli_kupno:
    kli = np.random.choice(klienci[0])
    while kli == el:
        kli = np.random.choice(klienci[0])
    id_kli_sprz.append(kli)

cena_zakupu = []
for i in range(len(id_pojazdu_sprzedaży)):
    index = id_pojazdu_sprzedaży[i]
    model = pojazdy.iloc[index - 1, 3]
    rok_produkcji = pojazdy.iloc[index -1 , 2]
    typ_pojazdu = pojazdy.iloc[index -1, 6]
    cena = 0
    try:
        if typ_pojazdu == "samochód":
            cena = []
            #for j in range(len(cars)):
                #if cars["Model"][j] == model:
                    #cena = cars.iloc[j]["MSRP"]
            # Pobranie ceny MSRP dla samochodu
            cena = cars[cars["Model"] == model]["MSRP"]
            if not cena.empty:
                cena = cena.iloc[0]
            else:
                continue
        else:
            for j in range(len(motocykle)):
                if motocykle["model"][j] == model:
                    cena = motocykle.iloc[j]["price"]
            
        if cena == 0:
            cena = np.random.randint(30000, 80000)
        # Usunięcie niepotrzebnych znaków z ceny
        cena = re.sub(r'[^\w]', '', str(cena))
        
        # Konwersja ceny na int
        cena = int(cena)
        
        # Aktualizacja ceny w zależności od wieku pojazdu
        aktualny_rok = 2024
        cena = 4* cena * 0.5 ** ((aktualny_rok - rok_produkcji)/5)
        
        if cena>300000:
            cena=int(np.random.randint(30000, 80000))
        # Dodanie ceny do listy
        cena_zakupu.append(int(cena))
        
    except (ValueError, IndexError) as e:
        print(f"Error processing vehicle at index {index}: {e}")
        cena_zakupu.append(int(np.random.randint(30000, 80000)))
"""
data_zwrotu_naprawy = []
for i in range(len(data_zakupu)):
    if data_sprzedazy[i] ==None:
        data_zwrotu_naprawy.append(data_zakupu[i] + datetime.timedelta(days = np.random.randint(1, (datetime.date.today - data_zakupu[i]).days)))
    else:
        data_zwrotu_naprawy.append(data_zakupu[i] + datetime.timedelta(days = np.random.randint(1, (data_sprzedazy[i] - data_zakupu[i]).days)))

"""
#NAPRAWY

naprawy = list(zip(id_klienta_naprawy, id_pojazdy_naprawy, dates, dates_zap, typ_transakcji_naprawy))

cena_naprawy = []
uzyte_czesci = []
for i in range(len(id_pojazdu_sprzedaży)):
    n = len(czesci)
    c = np.random.randint(1, n, size = np.random.randint(1, 7))
    uzyte_czesci.append(c)
    cena = 0
    for el in c:
        cena += czesci.iloc[el - 1][1]
    cena_naprawy.append(cena)

cena_naprawy2 = [] #do napraw bo wcześniejsze do sprzedaży XD
uzyte_czesci2 = []
for i in range(len(naprawy)):
    n = len(czesci)
    c = np.random.randint(1, n, size = np.random.randint(1, 7))
    uzyte_czesci2.append(c)
    cena = 0
    for el in c:
        cena += czesci.iloc[el - 1][1]
    if naprawy[i][4] == "naprawa":
        cena_naprawy2.append(float(cena)*np.random.uniform(1.3, 1.7))
    else:
        cena_naprawy2.append(cena)

cena_sprzedaży = [int(int((cena_zakupu[i] + cena_naprawy[i]))*np.random.uniform(1.1, 1.4)) for i in range(len(data_sprzedazy))]

sprzedaz = list(zip(id_pojazdu_sprzedaży, id_kli_sprz, data_zakupu, data_sprzedazy, cena_zakupu, cena_naprawy, cena_sprzedaży))

#TRANSAKCJE

kupno = list(zip(id_pojazdu_sprzedaży, id_kli_kupno, data_zakupu, [(-1)* el for el in cena_zakupu], ["kupno"] * len(id_pojazdu_sprzedaży)))
sprzed = list(zip(id_pojazdu_sprzedaży, id_kli_sprz, data_sprzedazy, [cena_sprzedaży[i] - cena_zakupu[i] for i in range(len(cena_sprzedaży))], ["sprzedaż"] * len(id_pojazdu_sprzedaży)))
nap = []
ren = []


for i in range(len(naprawy)):
    if naprawy[i][4] == 'naprawa':
        nap.append((naprawy[i][1], naprawy[i][0],naprawy[i][3], cena_naprawy2[i],'naprawa'))
    else:
        ren.append((naprawy[i][1], naprawy[i][0],naprawy[i][3],(-1)* cena_naprawy2[i],'renowacja'))

tra =  sprzed + nap + ren

for i in range(len(tra)):
    tra[i] = list(tra[i])

for i in range(len(tra)):
    if tra[i][1] != None:
        if int(klienci.iloc[tra[i][1] -1][1]) == 0:
            tra[i].extend(['paragon', tra[i][2], np.random.choice(['karta', 'gotówka', 'przelew'])])
        else:
            tra[i].extend(['faktura', tra[i][2] + datetime.timedelta(days = 30), np.random.choice(['karta', 'gotówka', 'przelew'])])

    else:
        tra[i].extend(['faktura', tra[i][2] + datetime.timedelta(days = 30), 'przelew'])

tra.sort(key=lambda x: x[2])
mycursor = con.cursor()


mycursor.execute("DROP TABLE IF EXISTS transakcje")

sql ='''CREATE TABLE transakcje(
   id_transakcji INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
   typ_transakcji ENUM('naprawa', 'renowacja', 'sprzedaż', 'kupno') NOT NULL,
   termin_zapłaty DATE,
   paragon_czy_faktura VARCHAR(10) NOT NULL,
   data_wystawienia DATE,
   sposób_zapłaty VARCHAR(40) NOT NULL,
   data_zapłaty DATE,
   kwota_całkowita DOUBLE
);'''
mycursor.execute(sql)

tra2 = []
for i in range(len(tra)):
    insert = (
        "INSERT INTO transakcje(typ_transakcji, termin_zapłaty, paragon_czy_faktura, data_wystawienia, sposób_zapłaty, data_zapłaty, kwota_całkowita)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )
    try:
        dni = (tra[i][6]-tra[i][2]).days
        do_dzis = np.abs((tra[i][6]-datetime.date(2024,6,15)).days)
        if dni ==0:
            data_zapla = tra[i][2]
        else:
            if dni<do_dzis:
                data_zapla = tra[i][2] + datetime.timedelta(days = np.random.randint(1, dni))
            else:
                if do_dzis!=0:
                    data_zapla = tra[i][2] + datetime.timedelta(days = np.random.randint(0, do_dzis))
                else: data_zapla = tra[i][2]  
        ins = (tra[i][4], tra[i][6], tra[i][5], tra[i][2], str(tra[i][7]), data_zapla, round(float(tra[i][3]), 2))
        tra2.append([i, tra[i][4], tra[i][6], tra[i][5], tra[i][2], str(tra[i][7]), data_zapla, float(tra[i][3]), tra[i][0], tra[i][1]])
        mycursor.execute(insert, ins)
        con.commit()
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
        con.rollback()

mycursor.execute("DROP TABLE IF EXISTS sprzedaż")

sql = '''CREATE TABLE sprzedaż(
id_sprzedaży_kupna INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
id_pojazdu INT NOT NULL,
id_transakcji INT NOT NULL,
id_klienta INT NOT NULL,
data_zakupu DATE,
data_sprzedaży DATE,
cena_zakupu INT NOT NULL,
cena_naprawy DOUBLE NOT NULL,
cena_sprzedaży INT NOT NULL
);
'''
mycursor.execute(sql)

for i in range(len(sprzedaz)):
    insert = (
        "INSERT INTO sprzedaż(id_pojazdu, id_transakcji, id_klienta, data_zakupu, data_sprzedaży, cena_zakupu, cena_naprawy, cena_sprzedaży)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    )
    id_tr =0
    for j in range(len(tra2)):
        if tra2[j][8] == sprzedaz[i][0]:
            id_tr = tra2[j][0]
    if id_tr ==0:
        print("Błąd w indeksie")
    ins = (int(sprzedaz[i][0]), id_tr, int(sprzedaz[i][1]), sprzedaz[i][2], sprzedaz[i][3], sprzedaz[i][4], float(sprzedaz[i][5]), sprzedaz[i][6])
    try:
        mycursor.execute(insert, ins)
        con.commit()
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
        con.rollback()

mycursor.execute("DROP TABLE IF EXISTS naprawy")

sql = '''CREATE TABLE naprawy(
id_naprawy_renowacji INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
id_klienta INT,
id_pojazdu INT NOT NULL,
id_transakcji INT NOT NULL,
data_przyjęcia DATE,
data_zwrotu DATE
);
'''

mycursor.execute(sql)

for i in range(len(naprawy)):
    insert = (
        "INSERT INTO naprawy(id_klienta, id_pojazdu, id_transakcji, data_przyjęcia, data_zwrotu)"
        "VALUES (%s, %s, %s, %s, %s)"
    )
    id_tr =0
    for j in range(len(tra2)):
        if tra2[j][8] == naprawy[i][1]:
            id_tr = tra2[j][0]
    if id_tr ==0:
        print("Błąd w indeksie")
    ins = (naprawy[i][0],int(naprawy[i][1]),int(id_tr),naprawy[i][2],naprawy[i][3])
    try:
        mycursor.execute(insert, ins)
        con.commit()
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
        con.rollback()
mycursor.close()
con.close()