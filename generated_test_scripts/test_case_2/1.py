
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import sys
from compare_sentences import compare_sentences

def test_validate_cart_count():
    # Setup WebDriver options
    options = Options()
    options.add_argument("--incognito")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })

    # Initialize WebDriver
    driver = webdriver.Chrome(options=options)
    try:
        # Navigate to the homepage
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()

        # Wait for the page to load
        sleep(3)

        # Locate the username input field and enter username
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-test='username']"))
        )
        username_input.send_keys("standard_user")
        sleep(3)

        # Locate the password input field and enter password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-test='password']"))
        )
        password_input.send_keys("secret_sauce")
        sleep(3)

        # Locate and click the login button
        login_button = driver.find_element(By.XPATH, "//input[@data-test='login-button']")
        login_button.click()
        sleep(3)

        # Verify redirection to the product listing page
        expected_title = "Swag Labs - Product Listing"
        actual_title = driver.title
        if not compare_sentences(expected_title, actual_title):
            sys.exit(1)

        # Locate and click the 'Add to Cart' button for 'Sauce Labs Backpack'
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-test='add-to-cart-sauce-labs-backpack']")))
        add_to_cart_button.click() 
        sleep(3)

        # Verify that the cart icon displays a badge with a count of '1'
        cart_badge = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@data-test='shopping-cart-badge']"))
        )
        if not compare_sentences(cart_badge.text, "1"):
            sys.exit(1)

        # If everything passed successfully
        sys.exit(0)

    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    test_validate_cart_count()
