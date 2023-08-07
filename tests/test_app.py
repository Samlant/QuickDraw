import time

from selenium import webdriver
from selenium.webdriver.edge.options import Options


class WebClient:
    def __init__(self) -> None:
        self.options = Options()
        self.options.page_load_strategy = "normal"

    def engage_browser(self, uri: str):
        driver = webdriver.Edge(options=options)
        driver.get(uri)
        print(driver.title)
        while driver.title == "Google":
            print("Still waiting for a new page")
            time.sleep(2)
        print(driver.current_url)
        uri = driver.current_url
        driver.quit()
        return uri
