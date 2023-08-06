import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

def fetchSchedule(weeks=2, timeout=4):
	options = webdriver.ChromeOptions()
	options.add_argument("--headless")

	driver = webdriver.Chrome(options=options)
	driver.set_window_size(1600, 900)
	driver.get("https://mcduk.reflexisinc.co.uk/kernel/views/authenticate/W/MCDUK.view")

	username = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("xpath", "//input[@placeholder='Enter username']")))
	password = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("xpath", "//input[@placeholder='Enter password']")))
	submit = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("id", "loginButton")))

	username.send_keys(os.getenv("MCD_USERNAME"))
	password.send_keys(os.getenv("MCD_PASSWORD"))
	submit.click()

	try:
		schedule = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("xpath", "//*[@id='systemLink']/div[2]/div")))
		schedule.click()
	except TimeoutException:
		print("Unable to find schedule redirect, are the login details correct?")
		driver.quit()
		return

	frame = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("class name", "how-do-div-iframe")))
	driver.switch_to.frame(frame)

	for i in range(weeks):
		try:
			rows = WebDriverWait(driver, timeout).until(EC.visibility_of_all_elements_located(("class name", "empShiftRowTable")))
			driver.save_screenshot(f"week{i}.png")
		except TimeoutException:
			print("No more weeks left to fetch")
			break

		nextWeek = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("class name", "calNextButton")))
		nextWeek.click()

	driver.quit()

if __name__ == "__main__":
	fetchSchedule()
