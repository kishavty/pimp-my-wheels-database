import random
import numpy as np
import mysql.connector
import pandas as pd


##imiona meskie
dane = pd.read_csv('imiona_meskie.csv')
imiona_m = dane["IMIĘ PIERWSZE"]
imiona_m_liczba = dane["LICZBA WYSTĄPIEŃ"]
liczba_suma = sum(imiona_m_liczba)
imiona_m_prawdo = [i/liczba_suma for i in imiona_m_liczba]

##nazwiska meskie
dane = pd.read_csv('nazwiska_meskie.csv')
nazwiska_m = dane["Nazwisko aktualne"]
nazwiska_m_liczba = dane["Liczba"]
liczba_suma = sum(nazwiska_m_liczba)
nazwiska_m_prawdo = [i/liczba_suma for i in nazwiska_m_liczba]


#imiona damksie
dane = pd.read_csv('imiona_zenskie.csv')
imiona_z = dane["IMIĘ_PIERWSZE"]
imiona_z_liczba = dane["LICZBA_WYSTĄPIEŃ"]
liczba_suma = sum(imiona_z_liczba)
imiona_z_prawdo = [i/liczba_suma for i in imiona_z_liczba]

#nazwiska damskie
dane = pd.read_csv('nazwiska_zenskie.csv')
nazwiska_z = dane["Nawisko aktualne"]
nazwiska_z_liczba = dane["Liczba"]
liczba_suma = sum(nazwiska_z_liczba)
nazwiska_z_prawdo = [i/liczba_suma for i in nazwiska_z_liczba]



def generate_name(sex, names_m=[], names_f=[], probabilities_m=[], probabilities_f=[]):
    if sex == "m": #male
        name = np.random.choice(names_m, p = probabilities_m)
    elif sex == "f": #female
        name = np.random.choice(names_f, p = probabilities_f)
    return name, sex


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
    return


