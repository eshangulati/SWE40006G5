from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest

class MyAppTests(unittest.TestCase):

    def setUp(self):
        # Set up remote connection to Selenium container
        chrome_options = webdriver.ChromeOptions()
        
        # Add headless mode to reduce load
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")  # Optional: further reduce load
        
        self.driver = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            options=chrome_options
        )
    
    def tearDown(self):
        # Close the browser after test
        self.driver.quit()
    
    def test_home_page(self):
        # Visit the application URL
        self.driver.get('http://app:80')  # Assuming the app is running on port 80 in the container
        # Verify the title of the homepage
        self.assertIn("Welcome", self.driver.title)
    
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
