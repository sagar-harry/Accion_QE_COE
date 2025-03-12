
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from compare_sentences import compare_sentences

def test_successful_login():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        wait = WebDriverWait(driver, 10)

        # Open the SauceDemo login page
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()
        time.sleep(3)  # wait for page load

        # Find username input, enter the username
        username_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='user-name']")))
        username_input.send_keys("standard_user")
        time.sleep(3)

        # Find password input, enter the password
        password_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys("secret_sauce")
        time.sleep(3)

        # Find Login button and click it
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']")))
        login_button.click()
        time.sleep(3)

        # Wait until URL changes to /inventory.html
        wait.until(EC.url_to_be("https://www.saucedemo.com/inventory.html"))

        # Verify the correct page is loaded
        current_url = driver.current_url
        if not current_url.endswith("/inventory.html"):
            print("URL mismatch: Expected URL should end with '/inventory.html'")
            sys.exit(1)

        # Verify the Products title is visible
        products_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='title' and text()='Products']")))
        expected_title = "Products"
        actual_title = products_title.text
        if not compare_sentences(actual_title, expected_title):
            print(f"Title mismatch: Expected title '{expected_title}', but found '{actual_title}'")
            sys.exit(1)

        print("Test Passed!")
        sys.exit(0)

    except Exception as e:
        print(f"Test Failed: {e}")
        sys.exit(1)

    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    test_successful_login()
