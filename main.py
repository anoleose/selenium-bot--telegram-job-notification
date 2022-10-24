
import time
import os
from random import randrange
from database import connection, create_task, get_all_task, get_task, update_task
from send import telegram_bot_sendtext, time_run_notification
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
load_dotenv()



def notification(url, key_word):
	url = url
	key_word = key_word
	options = Options()
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option('useAutomationExtension', False)
	options.add_argument('--disable-blink-features=AutomationControlled')

	options.add_argument("--headless")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--no-sandbox")
	browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
	browser.get(url)
	time.sleep(randrange(3, 6))

	search = browser.find_element(By.ID, "q")
	for letter in key_word:
		time.sleep(0.5)
		search.send_keys(letter, Keys.ENTER)

	time.sleep(1.5)
	tasks_list = browser.find_element(By.ID, "tasks_list")
	task_list  = tasks_list.find_elements(By.CLASS_NAME, "content-list__item")

	for count, task in enumerate(task_list[:5], 1):
		time.sleep(2)
		title  = task.find_element(By.CLASS_NAME, "task__title").text
		link   = task.find_element(By.TAG_NAME, "a").get_attribute('href')
		price  = task.find_element(By.CLASS_NAME, "task__price").text
		try:
			bid    = task.find_element(By.CLASS_NAME, "params__responses").text
		except NoSuchElementException:
			bid  = "0 отклик"
		view   = task.find_element(By.CLASS_NAME, "params__views").text
		posted = task.find_element(By.CLASS_NAME, "params__published-at").text
		create_data = (count, title, link, price, bid, view, posted)
		update_data = (title, link, price, bid, view, posted, count)
		if get_task(connection, count) is None:
			create_task(connection, create_data)
			print("create new record")
		elif count != get_task(connection, count)[0] and title != get_task(connection, count)[1]:
			create_task(connection, create_data)
			print("create new record")
		elif title != get_task(connection, count)[1] and count == get_task(connection, count)[0]:
			link = f"<a color='green' href='{link}'><b>Откликнуться</b></a>"
			notification = f"<strong>{title}</strong>\nPrice: {price}\nFeedback: {bid}\nView: {view}\nPublished: {posted}\n{link} "
			telegram_bot_sendtext(notification)
			update_task(connection, update_data)
		else:
			print("exist")


if __name__ =='__main__':
	minute_run = time_run_notification(5)
	if minute_run<300:
		print("minutes must be 5 or plus")
	else:
		while True:
			notification("https://freelance.habr.com/tasks", "Django")
			print("searching...")
			time.sleep(minute_run)









