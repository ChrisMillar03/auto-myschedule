import os, time, keras_ocr
from dotenv import load_dotenv
from binascii import a2b_base64
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fix_captcha(text):
	new_text = ""

	for c in text:
		if c in ["o", "O"]:
			new_text += "0"
		elif c in ["i", "I", "j", "J", "l", "L"]:
			new_text += "1"
		elif c in ["s", "S", "z", "Z"]:
			new_text += "5"
		elif c in ["g", "G"]:
			new_text += "9"
		else:
			new_text += c

	return new_text

def fetch_schedule(mcd_user, mcd_pass, weeks=2, timeout=4):
	pipeline = keras_ocr.pipeline.Pipeline()
	options = webdriver.ChromeOptions()
	options.add_argument("--headless")

	driver = webdriver.Chrome(options=options)
	driver.set_window_size(1600, 900)
	driver.get("https://mcduk.reflexisinc.co.uk/kernel/views/authenticate/W/MCDUK.view")

	username = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("xpath", "//input[@placeholder='Enter username']")))
	password = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("xpath", "//input[@placeholder='Enter password']")))
	captcha = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("xpath", "//input[@placeholder='Type the text']")))
	image = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("id", "captchaImage")))
	submit = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("id", "loginButton")))

	captcha_data = image.get_attribute("src")

	with open("captcha.png", "wb") as fd:
		fd.write(a2b_base64(captcha_data.split(",")[-1]))

	images = [keras_ocr.tools.read("captcha.png")]
	prediction_groups = pipeline.recognize(images)
	captcha_text = ""

	for k, v in enumerate(prediction_groups):
		captcha_text += v[0][0]

	captcha_text = fix_captcha(captcha_text)

	username.send_keys(mcd_user)
	password.send_keys(mcd_pass)
	captcha.send_keys(captcha_text)
	submit.click()

	try:
		menu = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("id", "menu-ESS")))
		menu.click()
	except TimeoutException:
		print("Unable to find navigation menu, captcha solver likely failed.")
		driver.quit()
		return

	schedule = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("xpath", "//div[@class='ps-content']/mat-accordion[1]")))
	schedule.click()

	frame = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(("id", "ESS_ESS^ESS")))
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
	load_dotenv()
	fetch_schedule(os.getenv("MCD_USERNAME"), os.getenv("MCD_PASSWORD"))
	time.sleep(5)
