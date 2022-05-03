from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os

user = input('Login: ')
passwd = input('Haslo: ')
print()

path = input('Jaka lokalizacja zapisu?\n')
print()

while (0==0):
    numer = input('Numer budynku: ')
    print()
    opcja = input("[w] wszystkie\n[z] zamontowane\n[p] puste\n[l] bez legalizacji\nWybierz: ")
    opts = Options()
    opts.add_argument(" --headless")
    opts.add_argument("--log-level=3")
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])

    #opts.binary_location="C:\Program Files\Google\Chrome\Application\chrome.exe"

    chrome_driver = os.getcwd() +"\\chromedriver.exe"

    driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

    driver.get("https://webbill.brunata.dk/login/weblogin.logincontrol.showlogin?p_kalder=http://webbill.brunata.dk/webbill/webbill.home.start_frames")

    driver.maximize_window()

    username = '/html/body/form/div/div/div/div[1]/input'
    password = '/html/body/form/div/div/div/div[2]/input'
    logIn = '/html/body/form/div/div/div/div[3]/input'
    nrBudynku = '//*[@id="p_anlnr"]'
    WebMon = '/html/body/ul/li[10]/a'
    odczyty = '//*[@id="menu10_5"]'

    driver.find_element_by_xpath(username).send_keys(user)
    driver.find_element_by_xpath(password).send_keys(passwd)
    driver.find_element_by_xpath(logIn).click()

    driver.switch_to.frame('venstre_del')

    driver.find_element_by_xpath(nrBudynku).send_keys(numer)
    driver.find_element_by_xpath(nrBudynku).send_keys(Keys.ENTER)
    driver.find_element_by_xpath(WebMon).click()
    driver.find_element_by_xpath(odczyty).click()
    driver.switch_to.parent_frame()
    driver.switch_to.frame('hoejre_del')

    f = open(path + '\\' + numer + opcja + ".txt",'w',encoding="utf-8")
    print('KOLUMNA;KOLUMNA;KOLUMNA;KOLUMNA;KOLUMNA;KOLUMNA;KOLUMNA;KOLUMNA;ADRES;NAZWISKO;LICZBA', file = f)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")
    results = soup.find_all("table", class_ = "tablgitter")

    while (0==0):

        if opcja == "w":
        
            for table in results:
                table = table.find_all("td", class_="tekst")
                for mieszkanie in table:
                    print(mieszkanie.get_text().strip(), end=";", file = f)
                print("\n", end="", file = f)
            for linia in results:
                linia = linia.find_all("td", class_="mlrtabel")
                print(int(len(linia)/9), file = f)
            break

        elif opcja == "z":

            for table in results:
                if table.find("td", class_="mlrtabel"):
                    table = table.find_all("td", class_="tekst")
                    for mieszkanie in table:
                        print(mieszkanie.get_text().strip(), end=";", file = f)
                    print("\n", end="", file = f)
            break

        elif opcja == "p":
        
            for table in results:
                if not table.find("td", class_="mlrtabel"):
                    table = table.find_all("td", class_="tekst")
                    for mieszkanie in table:
                        print(mieszkanie.get_text().strip(), end=";", file = f)
                    print("0\n", end="", file = f)
            break

        elif opcja == "l":

            for table in results:
                table = table.find_all("td", class_="tekst")
                for mieszkanie in table:
                    print(mieszkanie.get_text().strip(), end=";", file = f)
                print("\n", end="", file = f)
            for linia in results:
                linia = linia.find_all("td", class_="mlrtabel")
                print(int(len(linia)/9), file = f)
            print("", file = f)
            for legal in results:
                legal = legal.find_all("a")
                print(int(len(legal)), file = f)
            break

        else:
            print("Error")


    driver.quit()
    print()
    answer = input('Dalej?\n[t] tak\n[n] nie\nWybierz: ')
    if answer == 'n':
        break
    print()