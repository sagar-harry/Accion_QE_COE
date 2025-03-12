
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from compare_sentences import compare_sentences

def test_validate_cart_count():
    # Setup Chrome options for incognito and disabling notifications
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-notifications")

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Wait instance
    wait = WebDriverWait(driver, 10)

    try:
        # Open the SauceDemo login page
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()

        # Wait for 3 seconds
        time.sleep(3)
        
        # Enter username
        username_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='user-name']")))
        username_field.send_keys("standard_user")
        time.sleep(3)

        # Enter password
        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='password']")))
        password_field.send_keys("secret_sauce")
        time.sleep(3)

        # Click on login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']")))
        login_button.click()
        time.sleep(3)

        # Validate redirection to the Product Listing Page
        expected_title = 'Products'
        actual_title = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='title']"))).text
        assert compare_sentences(expected_title, actual_title), "Redirection to Product Listing Page Failed"

        # Click the 'Add to cart' button on 'Sauce Labs Backpack'
        add_to_cart_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']")))
        add_to_cart_button.click()
        time.sleep(3)

        # Validate cart badge displays '1'
        cart_badge = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='shopping_cart_badge']")))
        assert compare_sentences(cart_badge.text, '1'), "Cart badge count is not correct"

        # Validate the cart icon is visible with 'data-test' attribute as 'shopping-cart-link'
        cart_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-test='shopping-cart-link']")))
        assert cart_icon.is_displayed(), "Cart icon is not visible"

        # Exit with code 0 if the test case passed
        sys.exit(0)

    except Exception as e:
        print(f"Test failed: {e}")
        # Exit with code 1 if the test case failed
        sys.exit(1)

    finally:
        driver.quit()

test_validate_cart_count()
