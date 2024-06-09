import mysql.connector
import pandas as pd
import numpy as np
import math


ranking = pd.read_excel("ranking_polska.xlsx", sheet_name="Data", skiprows = [0,1,2,3], usecols=[1,2,3,4])
marki = ranking["marka"]
#marki = list(marki)
for i in range(len(ranking["2020"])):
    if ranking["2020"][i] == 0:
        ranking["2020"][i] = np.mean([ranking["2022"][i], ranking["2023"][i]])
suma = sum(ranking["2020"]) + sum(ranking["2022"]) + sum(ranking["2023"])
p = [] 
for i in range(len(marki)):
    p.append(sum([ranking["2020"][i], ranking["2022"][i], ranking["2023"][i]])/suma)

def infer_fuel_type(row):
    if float(row["EngineSize"]) <= 2.0 and float(row["Cylinders"]) <= 4:
        return "Benzyna"
    elif float(row["EngineSize"]) > 3.0 and float(row["Cylinders"]) >= 6:
        return "Diesel"
    elif float(row["MPG_City"]) > 40:  # Przyjmując, że bardzo niskie MPG wskazuje na hybrydy/elektryczne
        return "Hybrydowy/elektryczny"
    else:
        return "Benzyna"

cars = pd.read_csv("CarsData.csv", delimiter= ",")
cars = cars[cars["Make"].isin(marki)]
ile_aut = 40
ile_motocykli = 10
auta = []
motoc = []
i=0
while i < ile_aut:
    mar = np.random.choice(marki, size = 1, p = p)[0]
    z_marki = cars[cars["Make"]==mar]
    if(z_marki.empty):
        continue
    else:
        #model = np.random.choice(list(z_marki["Model"]), size = 1)
        model = np.random.choice(list(z_marki["Model"]), size=1).item()
        wiersz = z_marki[z_marki["Model"]==model]
        if len(wiersz)>1:
            wiersz = wiersz.iloc[np.random.randint(len(wiersz))]
        index_wiersza = wiersz.index[0]
        rok = np.random.randint(2000, 2024)
        przebieg = int(sum(np.random.randint(12500, 22500, size = 2025 - rok)))
        paliwo = infer_fuel_type(wiersz)
        auta.append((str(mar), rok,model, przebieg, paliwo, "samochód"))
        i+=1

print(auta)
paliwa = ['Petrol', 'Diesel', 'Electric']
#motocykle
motocykle = pd.read_csv("BikeData.csv", delimiter= ",")


for i in range(ile_motocykli):
    ind = np.random.randint(len(motocykle) - 1)
    wiersz = motocykle.iloc[ind]
    while type(wiersz["model"]) != str or type(wiersz["company_name"]) != str or type(wiersz["Fuel Type"]) != str or wiersz["Fuel Type"] not in paliwa:
        ind = np.random.randint(len(motocykle) - 1)
        wiersz = motocykle.iloc[ind]
    rok = np.random.randint(2000, 2024)
    przebieg = int(sum(np.random.randint(12500, 22500, size = 2025 - rok)))
    paliwo = wiersz["Fuel Type"]
    if paliwo == 'Petrol':
        paliwo = 'Benzyna'
    elif paliwo == 'Electric':
        paliwo = 'Elektryczne'
    motoc.append((wiersz["company_name"], rok, wiersz["model"], przebieg, paliwo, "motocykl"))

    print(motoc)

id_motocyki = np.random.randint(ile_motocykli + ile_aut, size = ile_motocykli)
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

#mycursor.execute("SELECT length FROM film")
#con.commit()
mycursor.execute("DROP TABLE IF EXISTS pojazdy")

sql ='''CREATE TABLE pojazdy(
   id_pojazdu INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
   marka VARCHAR(40) NOT NULL,
   data_produkcji INT UNSIGNED,
   model VARCHAR(40) NOT NULL,
   przebieg INT UNSIGNED,
   rodzaj_paliwa VARCHAR(40) NOT NULL,
   typ_pojazdu ENUM('samochód', 'motocykl') NOT NULL
);'''
mycursor.execute(sql)
a = 0
m = 0
for i in range(ile_aut + ile_motocykli):   
    insert = (
        "INSERT INTO pojazdy(marka, data_produkcji, model, przebieg, rodzaj_paliwa, typ_pojazdu)"
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    try:
        if i in id_motocyki:
            if m<len(motoc):
                mycursor.execute(insert, motoc[m])
                m+=1
                con.commit()
        else:
            if a<len(auta):
                mycursor.execute(insert, auta[a])
                a+=1
                con.commit()
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
        con.rollback()


mycursor.close()
con.close()
