import random
import numpy as np
import mysql.connector
import pandas as pd


##imiona meskie
dane = pd.read_csv('data/imiona_meskie.csv')
imiona_m = dane["IMIĘ_PIERWSZE"]
imiona_m_liczba = dane["LICZBA_WYSTĄPIEŃ"]
liczba_suma = sum(imiona_m_liczba)
imiona_m_prawdo = [i/liczba_suma for i in imiona_m_liczba]

##nazwiska meskie
dane = pd.read_csv('data/nazwiska_meskie.csv')
nazwiska_m = dane["Nazwisko aktualne"]
nazwiska_m_liczba = dane["Liczba"]
liczba_suma = sum(nazwiska_m_liczba)
nazwiska_m_prawdo = [i/liczba_suma for i in nazwiska_m_liczba]


#imiona damksie
dane = pd.read_csv('data/imiona_zenskie.csv')
imiona_z = dane["IMIĘ_PIERWSZE"]
imiona_z_liczba = dane["LICZBA_WYSTĄPIEŃ"]
liczba_suma = sum(imiona_z_liczba)
imiona_z_prawdo = [i/liczba_suma for i in imiona_z_liczba]

#nazwiska damskie
dane = pd.read_csv('data/nazwiska_zenskie.csv')
nazwiska_z = dane["Nazwisko aktualne"]
nazwiska_z_liczba = dane["Liczba"]
liczba_suma = sum(nazwiska_z_liczba)
nazwiska_z_prawdo = [i/liczba_suma for i in nazwiska_z_liczba]



def generate_name(names_m=[], lastnames_m = [], names_f=[], lastnames_f=[], prob_l_m=[], prob_l_f=[], prob_m=[], prob_f=[]):
    i = np.random.choice([0,1])
    if i == 0: #male
        name = np.random.choice(names_m, p = prob_m)
        lastname = np.random.choice(lastnames_m, p = prob_l_m)
    else: #female
        name = np.random.choice(names_f, p = prob_f)
        lastname = np.random.choice(lastnames_f, p = prob_l_f)
    return name, lastname


def generate_nip():
    """ 
    https://pl.wikipedia.org/wiki/Numer_identyfikacji_podatkowej """

    nip = str(random.choice(range(100000000, 900000000)))

    #wielkie wyliczanie ostatniej cyfry kontrolnej nip:
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    total = sum(int(nip[i]) * weights[i] for i in range(9))
    control_digit = str(total % 11)

    nip += control_digit

    return nip


def generate_phone_number():
    """
    Generates a random phone number. https://pl.wikipedia.org/wiki/Numery_telefoniczne_w_Polsce
    """
    number =  str("+48 ") + str(np.random.choice([45, 50, 51, 53, 57, 60, 66, 69, 72, 73, 78, 79, 88])) + str(random.choice(range(1000000, 9000000)))
    return number


def generate_email(first_name, last_name):
    """
    Generates a random email for the customer.
    """
    email_end = ["@gmail.com", "@o2.pl", "@wp.pl", "@interia.pl", "@onet.pl", "@yahoo.com"]
    weights_email = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]

    if " " in first_name:
        first_name = first_name.split(" ")[0]

    email = (first_name[0: random.randint(2, len(first_name) - 1)] +
             random.choices(['', '.', '-'], weights=[0.7, 0.2, 0.1])[0] +
             last_name[0: random.randint(2, len(last_name) - 1)])
    
    email = email.lower()
    
    email += str(random.choices(['', str(random.randint(0, 100))], weights=[0.4, 0.6])[0])
    email += random.choices(email_end, weights=weights_email)[0]
    
    return email


def create_customer():

    imie, nazwisko = generate_name(names_m=imiona_m, lastnames_m = nazwiska_m, 
                                    names_f=imiona_z, lastnames_f=nazwiska_z, 
                                    prob_l_m=nazwiska_m_prawdo, prob_l_f=nazwiska_z_prawdo, 
                                    prob_m=imiona_m_prawdo, prob_f=imiona_z_prawdo)
    nip = np.random.choice([0, generate_nip()], p = [0.8, 0.2])
    nr_telefonu = generate_phone_number()
    email = generate_email(imie, nazwisko)

    return (str(imie), str(nazwisko), str(nip), str(nr_telefonu), str(email))

############################

klienci = []


for i in range(100):
    klienci.append(create_customer())


############################

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


mycursor.execute("DROP TABLE IF EXISTS klienci")

sql ='''CREATE TABLE klienci(
   id_klienta INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
   imie VARCHAR(40) NOT NULL,
   nazwisko VARCHAR(40) NOT NULL,
   nip VARCHAR(40) NOT NULL,
   nr_telefonu VARCHAR(40) NOT NULL,
   email VARCHAR(40) NOT NULL
);'''
mycursor.execute(sql)

for klient in klienci:   
    insert = (
        "INSERT INTO klienci(imie, nazwisko, nip, nr_telefonu, email)"
        "VALUES (%s, %s, %s, %s, %s)"
    )
    try:
        print(klient)
        mycursor.execute(insert, klient)
        con.commit()
    except mysql.connector.Error as err:
        print(f"Błąd: {err}")
        con.rollback()


mycursor.close()
con.close()

