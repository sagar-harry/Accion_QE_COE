
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from compare_sentences import compare_sentences

# Chrome options for disabling notifications, pop-ups, and running in incognito mode
options = Options()
options.add_argument('--disable-notifications')
options.add_argument('--incognito')
options.add_argument('--start-maximized')

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

try:
    # Given I am on the SauceDemo login page
    home_url = "https://www.saucedemo.com/"
    driver.get(home_url)

    # Wait for the page to load completely
    time.sleep(3)

    # When I enter username 'standard_user'
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@data-test='username']"))
    )
    username_input.send_keys("standard_user")
    time.sleep(3)

    # And I enter password 'secret_sauce'
    password_input = driver.find_element(By.XPATH, "//input[@data-test='password']")
    password_input.send_keys("secret_sauce")
    time.sleep(3)

    # And I click on login button
    login_button = driver.find_element(By.XPATH, "//input[@data-test='login-button']")
    login_button.click()
    time.sleep(3)

    # Then I should be redirected to the Product Listing Page
    WebDriverWait(driver, 10).until(
        EC.url_contains("/inventory.html")
    )

    # Assert URL
    expected_url = "https://www.saucedemo.com/inventory.html"
    if driver.current_url.endswith("/inventory.html"):
        # And the page URL should be '/inventory.html'
        print("URL assertion passed")
    else:
        raise AssertionError("URL does not match")

    # And I should see the Products header
    products_header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@data-test='title']"))
    )
    actual_text = products_header.text
    expected_text = "Products"
    
    # Use compare_sentences for assertion
    if compare_sentences(actual_text, expected_text):
        print("Products header text assertion passed")
        sys.exit(0)
    else:
        raise AssertionError("Products header text does not match")

except Exception as e:
    print(f"Test failed: {e}")
    sys.exit(1)

finally:
    # Close the browser
    driver.quit()
