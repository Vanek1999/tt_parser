#_____Разраб: ento_Vanek_____
#_____Подключение библиотек_____
import os
import telebot
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC



#_____Настройки_____   
bot = telebot.TeleBot ('1848165503:AAF5N91q9k_ZiIJPy8O4gOw35YrE0pasQ0A')
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

tt_link = []
data_url = []

def get_all_video():
	url = "https://www.tiktok.com/@batek.official"
	driver.get(url)
	sleep(1)

	#_____Спускаемся вниз_____
	element = driver.find_element(By.XPATH, """/html/body/tiktok-cookie-banner""")
	actions = ActionChains(driver)
	actions.move_to_element(element).perform()
	sleep(1)
	html = driver.page_source
	while True:
		sleep(3)
		element = driver.find_element(By.XPATH, """/html/body/tiktok-cookie-banner""")
		actions = ActionChains(driver)
		actions.move_to_element(element).perform()
		sleep(1)
		html2 = driver.page_source
		if html == html2:
			break
		else:
			html = html2

	#_____Забираем ссылки с вёрстки и ретёрнаем_____
	data = []
	for link in BeautifulSoup(html, features="html.parser").find_all("a"):
		data.append(link.get("href"))
	for tt in data:
		if "https://www.tiktok.com/@" in tt:
			tt_link.append(tt)
		else:
			pass

	return tt_link

def save_video(tt):
	#_____Настройки_____
	options = webdriver.ChromeOptions()
	options.add_argument("--disable-blink-features=AutomationControlled")
	options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option('useAutomationExtension', False)
	driver = webdriver.Chrome(options=options)

	#_____Сохраняем видео без водяного знака_____
	url = "https://savetik.app/ru/"
	driver.get(url)
	sleep(1)
	driver.find_element(By.XPATH, """//*[@id="url"]""").send_keys(tt)
	sleep(1)
	driver.find_element(By.XPATH, """//*[@id="download"]""").click()
	sleep(3)
	driver.find_element(By.XPATH, """//*[@id="downloadnow"]""").click()
	sleep(3)

def upload_video():
	try:
		#_____Загружаем видео в тг канал_____
		for filename in os.listdir("C:/Users/User/Downloads"):
			if "Savetik_" in filename:
				video = open("C:/Users/User/Downloads/" + filename, 'rb')
				bot.send_video("@ento_test", video)
	except:
		sleep(20)
		upload_video()

if __name__ == '__main__':
	#_____Запуск_____
	get_all_video()

	#_____Потоки_____
	with ThreadPoolExecutor(max_workers=5) as executor:
		for tt in tt_link:
			executor.submit(save_video, tt)

	upload_video()
