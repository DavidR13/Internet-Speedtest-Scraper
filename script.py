from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementNotInteractableException
import smtplib
import time

EMAIL = ''
PASSWORD = ''
SMTP_HOST = ''
SPEEDTEST_SITE = 'https://www.speedtest.net/'
MINIMUM_DOWNLOAD_SPEED = 100
MINIMUM_UPLOAD_SPEED = 10


class InternetSpeedTestBot:
    def __init__(self, driver):
        self.driver = webdriver.Chrome(service=driver)
        self.upload = 0
        self.download = 0

    # private method for getting internet speed information
    def __get_internet_speed(self):
        self.driver.get(SPEEDTEST_SITE)
        time.sleep(5)

        start_test = self.driver.find_element(by='class name', value='start-text')
        start_test.click()
        time.sleep(45)

        try:
            dismiss_notification = self.driver.find_element(by='xpath', value='/html/body/div[3]/div/div[3]/div/div/div'
                                                                              '/div[2]/div[3]/div[3]/div/div[8]/div/a')
            dismiss_notification.click()
            time.sleep(2)
        except ElementNotInteractableException:
            print('There is no notification popup.')
        finally:
            self.download = float(self.driver.find_element(by='xpath', value='/html/body/div[3]/div/div[3]/div/div'
                                                                                     '/div/div[2]/div[3]/div[3]/div/div[3]/div'
                                                                                     '/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
            self.upload = float(self.driver.find_element(by='xpath', value='/html/body/div[3]/div/div[3]/div/div/div'
                                                                                   '/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]'
                                                                                   '/div[1]/div[3]/div/div[2]/span').text)

    # private method for sending the email with SMTP
    def __send(self):
        if self.upload < MINIMUM_UPLOAD_SPEED or self.download < MINIMUM_DOWNLOAD_SPEED:
            with smtplib.SMTP(SMTP_HOST, port=587) as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=EMAIL,
                    msg=f"""SUBJECT: Internet Is Being Slow ;(\n\n
                    Woah! Looks like there's an issue with my internet speed again...
                    Download Speed: {self.download}
                    Upload Speed: {self.upload}
                    
                    This is below my comfort level of a {MINIMUM_DOWNLOAD_SPEED} download and a {MINIMUM_UPLOAD_SPEED} upload speed.
                    
                    I should probably check my internet or check with my provider...
                    """
                )

    # used to call the private methods on the class level
    def send_email(self):
        self.__get_internet_speed()
        self.__send()


if __name__ == '__main__':
    chrome_driver = Service('')
    my_bot = InternetSpeedTestBot(chrome_driver)
    my_bot.send_email()
