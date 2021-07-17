import os
import time
import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
import config


def click_modal_ok_button():
    try:
        modal_ok_button = driver.find_element_by_id('modal-releaseAnnoucements-btn-accept')
        if modal_ok_button.is_displayed():
            modal_ok_button.send_keys(Keys.ENTER)

        time.sleep(2)
        return True
    except common.exceptions.NoSuchElementException:
        print('Retrying OK..')

        time.sleep(5)
        click_modal_ok_button()


def search_address_main(address, city):
    try:
        address_input = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div[1]/div[1]/section[2]/div/div[1]/div[1]/input')
        city_input = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div[1]/div[1]/section[2]/div/div[1]/div[2]/input[1]')
        search_button = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div[1]/div[1]/section[2]/div/div[1]/div[5]/button')

        address_input.send_keys(address)
        city_input.send_keys(city)
        search_button.send_keys(Keys.ENTER)

        return True
    except common.exceptions.NoSuchElementException:
        print('Retrying search..')

        time.sleep(5)
        search_address_main(address, city)


def search_address_repeat(address, city):
    try:
        address_input = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div[1]/section[2]/div/div[1]/div[1]/input')
        city_input = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div[1]/section[2]/div/div[1]/div[2]/input[1]')
        search_button = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div[1]/section[2]/div/div[1]/div[5]/button')

        address_input.clear()
        address_input.send_keys(address)
        city_input.clear()
        city_input.send_keys(city)
        search_button.send_keys(Keys.ENTER)

        return True
    except common.exceptions.NoSuchElementException:
        print('Retrying search..')

        time.sleep(5)
        search_address_repeat(address, city)

    except common.exceptions.ElementNotInteractableException:
        print('Retrying search..')

        try:
            cancel_button = driver.find_element_by_xpath('/html/body/div[1]/div/div[11]/div/div/div[2]/div[3]/button[2]')
            cancel_button.send_keys(Keys.ENTER)
        except common.exceptions.NoSuchElementException:
            print('Retrying search..')

        time.sleep(5)
        search_address_repeat(address, city)


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

"""
    Connect to the MySQL instance 
"""
conn = mysql.connector.connect(
    user=config.dbUsername, password=config.dbPassword, host=config.dbHost,
    database=config.dbName, auth_plugin='mysql_native_password'
)

# Create table if not exist
createTable: str = """CREATE TABLE IF NOT EXISTS location_info (
  `id` INT NOT NULL AUTO_INCREMENT,
  `location` VARCHAR(255) NULL,
  `l_address` VARCHAR(255) NULL,
  `l_city` VARCHAR(255) NULL,
  `address` VARCHAR(255) NULL,
  `owner` VARCHAR(255) NULL,
  `vesting` VARCHAR(100) NULL,
  `recording_date` VARCHAR(16) NULL,
  `document_type` VARCHAR(100) NULL,
  `document_description` VARCHAR(128) NULL,
  `amount` VARCHAR(32) NULL,
  `buyer` VARCHAR(255) NULL,
  `seller` VARCHAR(255) NULL,
  PRIMARY KEY (`id`)
)"""

db = conn.cursor()

db.execute(createTable)
conn.commit()

url = "http://ortconline.com/"

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_PATH = os.path.join(PROJECT_ROOT, config.chromeDriver)

driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.maximize_window()
driver.get(url)

time.sleep(2)

emailInput = driver.find_element_by_id('_ctl0_PageContent_EmailTextbox')
passwordInput = driver.find_element_by_id('_ctl0_PageContent_PasswordTextbox')
loginButton = driver.find_element_by_id('_ctl0_PageContent_LoginClient')

emailInput.send_keys('stelladai@gmail.com')
passwordInput.send_keys('Stella123!')
loginButton.send_keys(Keys.ENTER)

time.sleep(5)

titlePro247Link = driver.find_element_by_xpath('/html/body/form/div/div/div[2]/div[1]/div[2]/ul/li[7]/ul/li[1]/span/a')
titlePro247Link.send_keys(Keys.ENTER)

time.sleep(5)

driver.switch_to.window(driver.window_handles[-1])

try:
    clickedModalOkButton = click_modal_ok_button()
    print(clickedModalOkButton)
except common.exceptions.ElementNotInteractableException:
    time.sleep(5)

    clickedModalOkButton = click_modal_ok_button()
    print(clickedModalOkButton)

time.sleep(5)

locationsList = [
    {'address': '58 Discovery', 'city': 'Irvine, CA 92618'},
    {'address': '58 Discovery', 'city': 'Irvine, CA 92618'}
]
i = 0
for location in locationsList:
    print(location['address'], location['city'])

    if i == 0:
        search_address_main(location['address'], location['city'])
    else:
        search_address_repeat(location['address'], location['city'])

    time.sleep(10)

    getNowButton = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[1]/div[2]/div[4]/div[9]/div/div[1]/div[3]/div[2]/div/button[1]')
    getNowButton.send_keys(Keys.ENTER)

    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])

    try:
        transactionSummaryTitle = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[13]/tbody/tr[1]/td')
        print('Title Found:', transactionSummaryTitle.text)
    except common.exceptions.NoSuchElementException:
        viewOrderButton = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[11]/div/div/div[2]/div[1]/table/tbody/tr/td[5]/span')
        viewOrderButton.click()

        driver.switch_to.window(driver.window_handles[-1])

    transactionSummaryTitle = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[13]/tbody/tr[1]/td')
    print('Title Found:', transactionSummaryTitle.text)

    # dom = BeautifulSoup(driver.page_source, 'html.parser')
    # tables = BeautifulSoup(str(dom), 'html.parser').find_all('table')
    #
    # spl_found = False
    # for table in tables:
    #     trs = BeautifulSoup(str(table), 'html.parser').find_all('tr')
    #     for tr in trs:
    #         tds = BeautifulSoup(str(tr), 'html.parser').find_all('td')
    #         for td in tds:
    #             if td.text.strip() == 'Subject Property Location':
    #                 spl_found = True
    #                 continue
    #

    owner = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[4]/tbody/tr[2]/td[2]').text
    vesting = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[4]/tbody/tr[5]/td[2]').text
    mailing_address = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[12]/tbody/tr[5]/td[2]').text
    recording_date = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[13]/tbody/tr[3]/td[2]').text
    document_type = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[13]/tbody/tr[3]/td[3]').text
    document_desc = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[13]/tbody/tr[3]/td[4]').text
    amount = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[13]/tbody/tr[3]/td[5]').text
    buyer = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[13]/tbody/tr[3]/td[7]').text
    seller = driver.find_element_by_xpath('/html/body/div[1]/div[2]/table[13]/tbody/tr[3]/td[8]').text

    query = "INSERT INTO location_info (location, l_address, l_city, address, owner, vesting, recording_date," \
            "document_type, document_description, amount, buyer, seller) VALUES ('', '" + location['address'] + "', '"\
            + location['city'] + "', '" + mailing_address + "', '" + owner + "', '" + vesting + "', '"\
            + recording_date + "', '" + document_type + "', '" + document_desc + "', '" + amount + "', '"\
            + buyer + "', '" + seller + "')"
    print(query)

    try:
        db.execute(query)
        conn.commit()
    except (mysql.connector.errors.InterfaceError, mysql.connector.errors.DataError):
        print('Error')

    driver.close()
    print(len(driver.window_handles))
    driver.switch_to.window(driver.window_handles[1])

    i += 1

time.sleep(5)

driver.quit()
