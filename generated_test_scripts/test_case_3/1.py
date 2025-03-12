
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from compare_sentences import compare_sentences

def run_checkout_process_test():
    # Set up Chrome options
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # Initialize the driver
    driver = webdriver.Chrome(options=options)
    
    # Maximize the window
    driver.maximize_window()
    
    # Open the SauceDemo login page
    driver.get("https://www.saucedemo.com/")
    
    # Implicit wait
    wait = WebDriverWait(driver, 10)
    
    try:
        # Wait for elements and perform actions
        time.sleep(3)
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='user-name']")))
        username_field.send_keys("standard_user")
        
        time.sleep(3)
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_field.send_keys("secret_sauce")
        
        time.sleep(3)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']")))
        login_button.click()
        
        # Validate redirection to the Product Listing Page
        time.sleep(3)
        current_url = driver.current_url
        assert "/inventory.html" in current_url, "Not redirected to Product Listing Page"
        
        time.sleep(3)
        add_to_cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']")))
        add_to_cart_button.click()
        
        time.sleep(3)
        cart_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-test='shopping-cart-link']")))
        cart_icon.click()
        
        # Validate redirection to the Shopping Cart Page
        time.sleep(3)
        current_url = driver.current_url
        assert "/cart.html" in current_url, "Not redirected to Shopping Cart Page"
        
        time.sleep(3)
        cart_item = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='inventory_item_name']")))
        assert cart_item.text == "Sauce Labs Backpack", "Sauce Labs Backpack not in cart"
        
        time.sleep(3)
        checkout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='checkout']")))
        checkout_button.click()
        
        # Validate redirection to Checkout Step 1 User Info Page
        time.sleep(3)
        current_url = driver.current_url
        assert "/checkout-step-one.html" in current_url, "Not redirected to Checkout Step 1 User Info Page"
        
        time.sleep(3)
        first_name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='first-name']")))
        first_name_field.send_keys("John")
        
        time.sleep(3)
        last_name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='last-name']")))
        last_name_field.send_keys("Doe")
        
        time.sleep(3)
        postal_code_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='postal-code']")))
        postal_code_field.send_keys("12345")
        
        time.sleep(3)
        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='continue']")))
        continue_button.click()
        
        # Validate redirection to Checkout Step 2 Order Overview Page
        time.sleep(3)
        current_url = driver.current_url
        assert "/checkout-step-two.html" in current_url, "Not redirected to Checkout Step 2 Order Overview Page"
        
        time.sleep(3)
        order_item = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='inventory_item_name']")))
        assert order_item.text == "Sauce Labs Backpack", "Sauce Labs Backpack not in order overview"

        time.sleep(3)
        total_price = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='summary_total_label']")))
        assert compare_sentences(total_price.text, "Total: $32.39"), "Total price does not match expected value"
        
        time.sleep(3)
        finish_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='finish']")))
        finish_button.click()
        
        # Validate redirection to the Order Confirmation Page
        time.sleep(3)
        current_url = driver.current_url
        assert "/checkout-complete.html" in current_url, "Not redirected to Order Confirmation Page"
        
        time.sleep(3)
        thank_you_message = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[@data-test='complete-header']")))
        assert compare_sentences(thank_you_message.text, "Thank you for your order!"), "Thank you message not displayed correctly"
        
        sys.exit(0)  # Test passed
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)  # Test failed
    finally:
        # Close the browser
        driver.quit()

run_checkout_process_test()
