from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class SeleniumHelper:
    def __init__(self, driverType='Chrome', implicitWait=10):
        # initialize appropriate driver, remember to download driver and add it to you PATH environment variable
        if driverType == 'Firefox':
            self.driver = webdriver.Firefox()
        elif driverType == 'Chrome':
            option = webdriver.ChromeOptions()
            chrome_prefs = {}
            option.experimental_options["prefs"] = chrome_prefs
            chrome_prefs["profile.default_content_settings"] = {"images": 2}
            chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
            self.driver = webdriver.Chrome(chrome_options=option)
        elif driverType == 'IE':
            self.driver = webdriver.Ie()
        else:
            raise Exception('Unknown webdriver type')
        # for every action do a retry with a 10 seconds timeout by default or user specified
        self.driver.implicitly_wait(implicitWait)

    def navigateToUrl(self, url):
        try:
            self.driver.get(url)
        except:
            # signal something was wrong, or handle the exception appropriately here according to your needs
            raise

    def closeBrowser(self):
        try:
            self.driver.close()
        except:
            # signal something was wrong, or handle the exception appropriately here according to your needs
            raise

    def search(self, searchString):
        try:
            # find search field in webpage using XPATH
            input = self.driver.find_elements_by_xpath('//input[@type="text" and @name="q"]')[0]
            # check if input is accessible to the user
            if not input.is_displayed():
                raise Exception("Search field not found.")
            # clear contents of search field
            input.clear()
            # type in query followed by the ENTER key to trigger the search
            input.send_keys(searchString + Keys.RETURN)
        except:
            # signal something was wrong, or handle the exception appropriately here according to your needs
            raise

    def waitForPageTitle(self, expectedTitle, timeout=30):
        while timeout > 0:
            timeout = timeout - 1
            time.sleep(1)
            if expectedTitle in self.driver.title:
                break
        if timeout <= 0 and (expectedTitle not in self.driver.title):
            return False
        return True

    def getContent(self):
        return self.driver.page_source
