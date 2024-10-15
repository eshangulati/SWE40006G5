from selenium import webdriver
import unittest

class MyAppTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',  # Connect to the Selenium container
            desired_capabilities={'browserName': 'chrome'}
        )

    def test_home_page(self):
        driver = self.driver
        driver.get("http://app:80")  # 'app' refers to the application container
        self.assertIn("Welcome to my website", driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
