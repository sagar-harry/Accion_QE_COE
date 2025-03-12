
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from compare_sentences import compare_sentences

def test_successful_login():
    # Configure ChromeOptions
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")

    # Instantiate the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to the home page (login page)
        driver.get("https://www.saucedemo.com/")
        
        # Wait for elements and actions
        wait = WebDriverWait(driver, 10)

        # Wait before action
        time.sleep(3)
        
        # Enter username
        username_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-test='username']")))
        username_field.send_keys("standard_user")

        # Wait before action
        time.sleep(3)
        
        # Enter password
        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-test='password']")))
        password_field.send_keys("secret_sauce")

        # Wait before action
        time.sleep(3)
        
        # Click the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@data-test='login-button']")))
        login_button.click()

        # Wait for navigation
        time.sleep(3)
        
        # Check if redirected to the product listing page
        wait.until(EC.url_contains("/inventory.html"))
        current_url = driver.current_url
        if compare_sentences(current_url.split("/")[-1], "inventory.html") != 100.0:
            raise Exception("URL does not match expected path")

        # Wait to ensure title is present
        time.sleep(3)

        # Assert the product listing page title
        product_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@data-test='title' and text()='Products']")))
        expected_title = "Products"
        if compare_sentences(product_title.text, expected_title) != 100.0:
            raise Exception("Page title does not match expected title")

        # Exit with success
        sys.exit(0)

    except Exception as e:
        print(str(e))
        sys.exit(1)

    finally:
        # Close the driver
        driver.quit()

# Running the test function
test_successful_login()
