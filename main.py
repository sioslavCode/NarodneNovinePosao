import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import smtplib

# Ovo je direktni url na stranicu OGLASNI DIO - Natjecaji za javna mjesta...da se izbjegnu ta dva klika..kategorija = 3 je Oglasnio dio a ogvrsta=26 je Natječaji za radna mjesta
# Ovaj broj=131 je tjedan ili tako nekakva objava i po tomo se zapravo može iterirat. A ovo rpp je broj redaka pa da nemoramo pagination staviomo 200
from selenium.webdriver.common.by import By

url = "https://narodne-novine.nn.hr/search.aspx?sortiraj=4&kategorija=3&ogvrsta=26&godina=2021&broj=131&rpp=200&qtype=1&pretraga=da"
service = Service("C:/Users/Komp/PycharmProjects/NarodneNovinePosao/chromedriver.exe")
chrome_options = Options()

driver = webdriver.Chrome(
    service=service,
    options=chrome_options
)

driver.get(url)
print("Otvorio stranicu")
time.sleep(3)

# Natječaji su nam već ispisani sada treba kliknuti na svaki. Možemo prvo naslove i linkove staviti u listu ili dict

# Lista evih div elementa koji su sebi sadrze naslov i link

try:
    div_element_list = driver.find_elements(By.CLASS_NAME, "resultTitle")
except NoSuchElementException:
    poruka = "Nema elemenata. Moguce da su promjenili classu!"

for element in div_element_list:
    naslov = element.text
    link = element.find_element(By.TAG_NAME, "a").get_attribute("href")
    print(naslov)
    print(link)

# Odi na svaki od linkova u listi i otvori ga

# NE ZABORAVI STAVITI RANDOM SLEEP IZMEDU SVAKOG UPITA OTVARANJE LINKA DA NEBI BIO ROBOT

url_oglasa = "https://narodne-novine.nn.hr/clanci/oglasi/o8327312.html"
driver.get(url_oglasa)

sadrzaj = driver.find_element(By.ID, "html-content-frame")
print("Sadržaj objave:" + "\n")
print(sadrzaj.text)

# Provjeri sadrži li sadržaj ključne rijeci


# Ako ima dodaj ga u poruku


# Zamjeni dio porkue sa <mark> da se vide kljucne rijeci žutom bojom


# Pošalji email poruku

driver.close()
