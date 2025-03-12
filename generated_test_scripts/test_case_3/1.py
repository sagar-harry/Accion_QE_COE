
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from compare_sentences import compare_sentences
import sys

def run_test():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--disable-notifications')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Step 1 - Given I am on the login page
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()
        sleep(3)

        # Step 2 - When I enter username as 'standard_user'
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='user-name']"))
        )
        username_input.send_keys("standard_user")
        sleep(3)

        # Step 3 - And I enter password as 'secret_sauce'
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']"))
        )
        password_input.send_keys("secret_sauce")
        sleep(3)

        # Step 4 - And I click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']"))
        )
        login_button.click()
        sleep(3)

        # Step 5 - Then I should be redirected to the product listing page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='title'][contains(text(), 'Products')]"))
        )
        
        # Step 6 - When I click on the 'Add to cart' button for 'Sauce Labs Backpack'
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']"))
        )
        add_to_cart_button.click()
        sleep(3)

        # Step 7 - And I click on the cart icon
        cart_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='shopping_cart_container']/a"))
        )
        cart_icon.click()
        sleep(3)

        # Step 8 - Then I should be on the shopping cart page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='title'][contains(text(), 'Your Cart')]"))
        )

        # Step 9 - When I click the 'Checkout' button
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='checkout']"))
        )
        checkout_button.click()
        sleep(3)

        # Step 10 - Then I should be on the checkout step 1 page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='title'][contains(text(), 'Checkout: Your Information')]"))
        )

        # Step 11 - When I enter 'First Name' as 'John' and 'Last Name' as 'Doe' and 'Zip/Postal Code' as '12345'
        first_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='first-name']"))
        )
        first_name_input.send_keys("John")
        sleep(3)

        last_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='last-name']"))
        )
        last_name_input.send_keys("Doe")
        sleep(3)

        zip_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='postal-code']"))
        )
        zip_input.send_keys("12345")
        sleep(3)

        # Step 12 - And I click the 'Continue' button
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='continue']"))
        )
        continue_button.click()
        sleep(3)

        # Step 13 - Then I should be on the checkout step 2 - Order Overview page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='title'][contains(text(), 'Checkout: Overview')]"))
        )

        # Step 14 - When I click the 'Finish' button
        finish_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='finish']"))
        )
        finish_button.click()
        sleep(3)

        # Step 15 - Then I should see the order confirmation page
        confirmation_heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[@class='complete-header']"))
        )
        confirmation_message_text = confirmation_heading.text
        assert compare_sentences(confirmation_message_text, "Thank you for your order!")
        
        # If all steps pass
        sys.exit(0)
    
    except Exception as e:
        print(f"Test failed: {str(e)}")
        sys.exit(1)
    
    finally:
        driver.quit()

run_test()
