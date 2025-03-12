
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from compare_sentences import compare_sentences
import sys

def run_checkout_test():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--start-maximized")

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Define xpaths
        locators = {
            "username": "//input[@id='user-name']",
            "password": "//input[@id='password']",
            "login_btn": "//input[@id='login-button']",
            "add_to_cart_btn": "//button[@id='add-to-cart-sauce-labs-backpack']",
            "shopping_cart_icon": "//div[@id='shopping_cart_container']//a",
            "checkout_btn": "//button[@id='checkout']",
            "first_name": "//input[@id='first-name']",
            "last_name": "//input[@id='last-name']",
            "postal_code": "//input[@id='postal-code']",
            "continue_btn": "//input[@id='continue']",
            "finish_btn": "//button[@id='finish']",
            "order_confirmation_msg": "//h2[@class='complete-header' and contains(text(), 'Thank you for your order!')]"
        }

        base_url = "https://www.saucedemo.com/"
        wait_time = 3

        # Start test
        driver.get(base_url)

        # Login
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, locators["username"])))
        driver.find_element(By.XPATH, locators["username"]).send_keys("standard_user")
        sleep(wait_time)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, locators["password"])))
        driver.find_element(By.XPATH, locators["password"]).send_keys("secret_sauce")
        sleep(wait_time)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, locators["login_btn"])))
        driver.find_element(By.XPATH, locators["login_btn"]).click()
        sleep(wait_time)

        # Assert on Product Listing Page
        current_url = driver.current_url
        if not current_url.endswith("/inventory.html"):
            sys.exit(1)

        # Add product to cart
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, locators["add_to_cart_btn"])))
        driver.find_element(By.XPATH, locators["add_to_cart_btn"]).click()
        sleep(wait_time)

        # Navigate to cart
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, locators["shopping_cart_icon"])))
        driver.find_element(By.XPATH, locators["shopping_cart_icon"]).click()
        sleep(wait_time)

        # Assert on Shopping Cart Page
        current_url = driver.current_url
        if not current_url.endswith("/cart.html"):
            sys.exit(1)

        # Check cart item
        if not driver.find_element(By.XPATH, "//div[@class='inventory_item_name']").text == "Sauce Labs Backpack":
            sys.exit(1)

        # Checkout process
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, locators["checkout_btn"])))
        driver.find_element(By.XPATH, locators["checkout_btn"]).click()
        sleep(wait_time)

        # Assert on Checkout Step 1 Page
        current_url = driver.current_url
        if not current_url.endswith("/checkout-step-one.html"):
            sys.exit(1)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, locators["first_name"])))
        driver.find_element(By.XPATH, locators["first_name"]).send_keys("John")
        sleep(wait_time)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, locators["last_name"])))
        driver.find_element(By.XPATH, locators["last_name"]).send_keys("Doe")
        sleep(wait_time)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, locators["postal_code"])))
        driver.find_element(By.XPATH, locators["postal_code"]).send_keys("12345")
        sleep(wait_time)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, locators["continue_btn"])))
        driver.find_element(By.XPATH, locators["continue_btn"]).click()
        sleep(wait_time)

        # Assert on Checkout Step 2 Page
        current_url = driver.current_url
        if not current_url.endswith("/checkout-step-two.html"):
            sys.exit(1)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, locators["finish_btn"])))
        driver.find_element(By.XPATH, locators["finish_btn"]).click()
        sleep(wait_time)

        # Assert on Order Confirmation Page
        current_url = driver.current_url
        if not current_url.endswith("/checkout-complete.html"):
            sys.exit(1)

        confirmation_message_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, locators["order_confirmation_msg"])))
        if not compare_sentences(confirmation_message_element.text, "Thank you for your order!"):
            sys.exit(1)

        # If we reach here, the test has passed
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        driver.quit()

run_checkout_test()
