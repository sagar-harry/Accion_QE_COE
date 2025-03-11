
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from compare_sentences import compare_sentences
import time
import sys

# Disable notifications, pop ups and run in incognito mode
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--incognito")

# Start the WebDriver
driver = webdriver.Chrome(options=options)

try:
    # Maximize the window
    driver.maximize_window()

    # Navigate to the SauceDemo login page
    driver.get("https://www.saucedemo.com/")
    time.sleep(3)  # Wait 3 seconds before every action

    # Wait for the username input to appear and enter the username
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@data-test='username']"))
    )
    username_input.send_keys("standard_user")
    time.sleep(3)

    # Wait for the password input to appear and enter the password
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@data-test='password']"))
    )
    password_input.send_keys("secret_sauce")
    time.sleep(3)

    # Wait for the login button to appear and click it
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@data-test='login-button']"))
    )
    login_button.click()
    time.sleep(3)

    # Verify that the URL is now the product listing page
    product_listing_url = "https://www.saucedemo.com/inventory.html"
    current_url = driver.current_url
    if not compare_sentences(current_url, product_listing_url):
        raise AssertionError("URLs do not match!")
    time.sleep(3)

    # Wait for the add to cart button for the first product and click it
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test='add-to-cart-sauce-labs-backpack']"))
    )
    add_to_cart_button.click()
    time.sleep(3)

    # Validate the cart icon shows a badge with a count of 1
    cart_icon_badge = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='shopping_cart_badge']"))
    )
    cart_count = cart_icon_badge.text
    if not compare_sentences(cart_count, "1"):
        raise AssertionError("Cart count is not 1!")

    # If all assertions pass
    sys.exit(0)

except (AssertionError, TimeoutException) as e:
    print(f"Test failed: {str(e)}")
    sys.exit(1)

finally:
    # Close the browser
    driver.quit()
