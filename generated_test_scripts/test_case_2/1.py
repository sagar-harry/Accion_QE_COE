
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from compare_sentences import compare_sentences

# Initialize options for Chrome
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Maximize the window and navigate to the homepage
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")

    # Wait to ensure the page is loaded
    time.sleep(3)

    # Find and fill username
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@data-test='username']"))
    )
    username_input.send_keys("standard_user")
    time.sleep(3)

    # Find and fill password
    password_input = driver.find_element(By.XPATH, "//input[@data-test='password']")
    password_input.send_keys("secret_sauce")
    time.sleep(3)

    # Find and click the Login button
    login_button = driver.find_element(By.XPATH, "//input[@data-test='login-button']")
    login_button.click()
    time.sleep(3)

    # Verify if redirected to Product Listing Page
    products_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='title']"))
    )
    if not compare_sentences(products_title.text, "Products"):
        print("Failed to navigate to Product Listing Page")
        sys.exit(1)

    # Find and click the Add to Cart button for Sauce Labs Backpack
    add_to_cart_button = driver.find_element(By.XPATH, "//button[@data-test='add-to-cart-sauce-labs-backpack']")
    add_to_cart_button.click()
    time.sleep(3)

    # Verify the cart count increment
    cart_badge = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='shopping_cart_badge']"))
    )
    if not compare_sentences(cart_badge.text, "1"):
        print("Cart count did not increment to 1")
        sys.exit(1)

    # Verify the cart icon shows "1" in the badge
    cart_icon = driver.find_element(By.XPATH, "//div[@id='shopping_cart_container']/a")
    cart_icon_badge_text = cart_icon.text.strip()
    if not compare_sentences(cart_icon_badge_text, "1"):
        print("Cart icon did not show 1 in the badge")
        sys.exit(1)

    print("Test case passed")
    sys.exit(0)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

finally:
    # Quit the driver
    driver.quit()
