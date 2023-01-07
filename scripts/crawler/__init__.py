from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
 
class SeleniumRequest:
    driver = None
    chrome_options = webdriver.ChromeOptions()
    
    def __init__(self):
        self.driver_path = Service(ChromeDriverManager().install())
        self.options = "--start-fullscreen"
        self.chrome_options.add_argument( self.options )
        
        self.driver = webdriver.Chrome(
            service = self.driver_path,
            options = self.chrome_options
        )

    def get( self, url, *args, callback=None):
        self.driver.get( url )
        return callback(*args, response=self.driver)
