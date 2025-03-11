
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from compare_sentences import compare_sentences

def test_successful_login():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--incognito")

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # Step 1: Navigate to the login page
        driver.get("https://www.saucedemo.com/")
        time.sleep(3)  # Wait for the page to load
        
        # Step 2: Enter the username
        username_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@data-test='username']"))
        )
        username_input.send_keys("standard_user")
        time.sleep(3)
        
        # Step 3: Enter the password
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@data-test='password']"))
        )
        password_input.send_keys("secret_sauce")
        time.sleep(3)
        
        # Step 4: Click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@data-test='login-button']"))
        )
        login_button.click()
        time.sleep(3)
        
        # Step 5: Assert redirection to product listing page
        WebDriverWait(driver, 10).until(
            EC.url_contains('/inventory.html')
        )
        assert '/inventory.html' in driver.current_url
        
        # Step 6: Assert the Products header text
        product_listing_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@data-test='title' and contains(text(), 'Products')]"))
        )
        header_text = product_listing_header.text
        expected_header = "Products"
        assert compare_sentences(header_text, expected_header)
        
        print("Test Passed")
        sys.exit(0)
    
    except Exception as e:
        print("Test Failed: ", e)
        sys.exit(1)
    
    finally:
        # Close the driver
        driver.quit()

# Execute the test
test_successful_login()
