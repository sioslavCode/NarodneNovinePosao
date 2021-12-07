import os
import time
from email.message import EmailMessage
from random import randint
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import smtplib

# Ovo je direktni url na stranicu OGLASNI DIO - Natjecaji za javna mjesta...da se izbjegnu ta dva klika..kategorija = 3 je Oglasnio dio a ogvrsta=26 je Natječaji za radna mjesta
# Ovaj broj=131 je tjedan ili tako nekakva objava i po tomo se zapravo može iterirat. A ovo rpp je broj redaka pa da nemoramo pagination staviomo 200
from selenium.webdriver.common.by import By

url = "https://narodne-novine.nn.hr/search.aspx?sortiraj=4&kategorija=3&ogvrsta=26&godina=2023&broj=131&rpp=200&qtype=1&pretraga=da"
service = Service("C:/Users/Komp/PycharmProjects/NarodneNovinePosao/chromedriver.exe")
chrome_options = Options()

driver = webdriver.Chrome(
    service=service,
    options=chrome_options
)
lista_objava = []
objave_s_kljucnim_rijecima = []
poruka = ""


class objava:
    def __init__(self, naslov, link):
        self.naslov = naslov
        self.link = link


# Prvo odi na stranicu pa joj uzmi zadnji NN broj i onda taj broj stavi u URL kako bi se nize izlistale stvari
driver.get(url)
print("Otvorio stranicu")
time.sleep(3)

listaNN = []
tablicaObjava = driver.find_element(By.ID, "space-table-placeholder")
zadnji_redak = tablicaObjava.find_elements(By.TAG_NAME, "tr")[-1]
nnBroj = zadnji_redak.find_elements(By.TAG_NAME, "td")[0].text
poruka = zadnji_redak.find_elements(By.TAG_NAME, "td")[1].text
print(poruka)

godina = date.today().year

print(godina)
print(nnBroj)

# Natječaji su nam već ispisani sada treba kliknuti na svaki. Možemo prvo naslove i linkove staviti u listu ili dict

# Lista evih div elementa koji su sebi sadrze naslov i link

url = "https://narodne-novine.nn.hr/search.aspx?sortiraj=4&kategorija=3&ogvrsta=26&godina=" + str(
    godina) + "&broj=" + str(nnBroj) + "&rpp=200&qtype=1&pretraga=da"
driver.get(url)
time.sleep(5)

try:
    div_element_list = driver.find_elements(By.CLASS_NAME, "resultTitle")
except NoSuchElementException:
    poruka = "Nema elemenata. Moguce da su promjenili classu!"

for element in div_element_list:
    naslov = element.text
    link = element.find_element(By.TAG_NAME, "a").get_attribute("href")

    lista_objava.append(objava(naslov, link))
    print(naslov)
    print(link)

# Odi na svaki od linkova u listi i otvori ga

for jedna_objava in lista_objava:
    # if lista_objava.index(jedna_objava) == 8: break #Ovo sluzi smao za tesitanje tj da prestane radit nakon 5 puta
    time.sleep(randint(7, 12))
    driver.get(jedna_objava.link)
    print(f"Otvaram: {jedna_objava.link}")
    # preuzmi sadzraj tog div elemnta
    sadrzaj = driver.find_element(By.ID, "html-content-frame")

    # Provjeri sadrži li sadržaj ključne rijeci

    kljucna_rijec = "pravn"

    if kljucna_rijec in sadrzaj.text:
        objave_s_kljucnim_rijecima.append(jedna_objava)

# Ako ima dodaj ga u poruku

for objava_kljucna in objave_s_kljucnim_rijecima:
    print(
        f"U teksu naslova: {objava_kljucna.naslov}, link: {objava_kljucna.link} nalazi se ključna riječ: {kljucna_rijec}")
    poruka = poruka + "Naslov: " + objava_kljucna.naslov + "<br>" + objava_kljucna.link + "<br>"

# Zamjeni dio porkue sa <mark> da se vide kljucne rijeci žutom bojom


# Pošalji email poruku


EMAIL_ADRESS = os.environ.get("python_user")
EMAIL_PASSWORD = os.environ.get("python_password")

msg = EmailMessage()
msg["Subject"] = "Narodne Novine posao objava"
msg["From"] = EMAIL_ADRESS
msg["To"] = EMAIL_ADRESS
msg.set_content(poruka)

msg.add_alternative(
    "<html><body><h3>Narodne Novine posao objava</h3>" + "Broj NN: " + nnBroj + "<br>" + poruka +
    "</body>"
    "</html>",
    subtype="html")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

    smtp.send_message(msg)

driver.close()
