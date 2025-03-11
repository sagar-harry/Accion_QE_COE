
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from compare_sentences import compare_sentences

def ui_test_validate_checkout_process():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--start-maximized")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Step 1: Given I am on the SauceDemo login page at "https://www.saucedemo.com/"
        driver.get("https://www.saucedemo.com/")
        time.sleep(3)

        # Step 2: When I enter the username "standard_user"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-test='username']"))
        ).send_keys("standard_user")
        time.sleep(3)

        # Step 3: And I enter the password "secret_sauce"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-test='password']"))
        ).send_keys("secret_sauce")
        time.sleep(3)

        # Step 4: And I click the login button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@data-test='login-button']"))
        ).click()
        time.sleep(3)

        # Step 5: Then I should be on the product listing page with URL ending '/inventory.html'
        WebDriverWait(driver, 10).until(EC.url_contains('/inventory.html'))

        # Step 6: When I click on the "Add to cart" button for the first product
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-test='add-to-cart-sauce-labs-backpack']"))
        ).click()
        time.sleep(3)

        # Step 7: And I click on the cart icon
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'shopping_cart_link')]"))
        ).click()
        time.sleep(3)

        # Step 8: Then I should be on the shopping cart page with URL ending '/cart.html'
        WebDriverWait(driver, 10).until(EC.url_contains('/cart.html'))
        
        # Step 9: And I click on the "Checkout" button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-test='checkout']"))
        ).click()
        time.sleep(3)

        # Step 10: Then I should be on the Checkout Step 1 page with URL ending '/checkout-step-one.html'
        WebDriverWait(driver, 10).until(EC.url_contains('/checkout-step-one.html'))

        # Step 11: When I enter "First Name" as "Test"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-test='firstName']"))
        ).send_keys("Test")
        time.sleep(3)

        # Step 12: And I enter "Last Name" as "User"
        driver.find_element(By.XPATH, "//input[@data-test='lastName']").send_keys("User")
        time.sleep(3)

        # Step 13: And I enter "Zip/Postal Code" as "12345"
        driver.find_element(By.XPATH, "//input[@data-test='postalCode']").send_keys("12345")
        time.sleep(3)

        # Step 14: And I click the "Continue" button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@data-test='continue']"))
        ).click()
        time.sleep(3)

        # Step 15: Then I should be on the Checkout Step 2 page with URL ending '/checkout-step-two.html'
        WebDriverWait(driver, 10).until(EC.url_contains('/checkout-step-two.html'))

        # Step 16: And I should see the order summary including "Sauce Labs Item"
        order_summary_label = driver.find_element(By.XPATH, "//div[contains(text(),'Sauce Labs Backpack')]").text
        if not compare_sentences("Sauce Labs Item", order_summary_label):
            raise Exception("Order summary validation failed")
        
        # Step 17: When I click the "Finish" button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-test='finish']"))
        ).click()
        time.sleep(3)

        # Step 18: Then I should be on the order confirmation page with URL ending '/checkout-complete.html'
        WebDriverWait(driver, 10).until(EC.url_contains('/checkout-complete.html'))

        # Step 19: And I should see the message "Thank you for your order!"
        confirmation_message = driver.find_element(By.XPATH, "//h2[@data-test='complete-header']").text
        if not compare_sentences("Thank you for your order!", confirmation_message):
            raise Exception("Order confirmation message validation failed")

        # Test passes if all assertions are successful
        sys.exit(0)
    except Exception as e:
        print(f"Test failed due to: {str(e)}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    ui_test_validate_checkout_process()
