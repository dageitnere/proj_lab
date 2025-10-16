from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

from app.dependencies.firefoxDriver import get_firefox_pool


def consent(wait):
    """Handle cookie consent popup"""
    try:
        consent_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fc-button-label")))
        consent_button.click()
        print("Cookie consent accepted.")
        time.sleep(1)
    except (TimeoutException, NoSuchElementException):
        print("Cookie consent popup not found")


def safe_extract(xpath, driver):
    """Safely extract nutrition value from table row"""
    try:
        row = driver.find_element(By.XPATH, xpath)
        text = row.find_element(By.XPATH, "./td[@class='right']").text.strip()
        return float(text.split(" ")[0]) if text else 0.0
    except NoSuchElementException:
        return 0.0


def get_product_data_from_url(url):
    """
    Extract nutrition data from a product URL

    Args:
        url (str): Direct product URL from nutritionvalue.org
        driver: Selenium webdriver instance
        wait: WebDriverWait instance

    Returns:
        dict: Product data with nutrition values, or error message
    """

    pool = get_firefox_pool()
    with pool.get_driver() as driver:
        wait = WebDriverWait(driver, 1)
        try:
            driver.get(url)
            time.sleep(2)
            # Handle cookie consent
            consent(wait)
            # Extract product name
            try:
                product_name = driver.find_element(By.ID, "food-name").text
            except NoSuchElementException:
                product_name = "Unknown Product"

            # Select 100g serving
            try:
                dropdown = Select(driver.find_element(By.CSS_SELECTOR, "select.serving[name='size']"))
                dropdown.select_by_visible_text("100 g")
                time.sleep(1)
            except NoSuchElementException:
                print(f"Could not find serving dropdown for {product_name}")

            # Extract calories
            try:
                calories = float(driver.find_element(By.ID, 'calories').text)
            except (NoSuchElementException, ValueError):
                calories = 0.0

            # Extract nutrients
            fat = safe_extract("//tr[td/a[@data-tooltip='Fat']]", driver)
            saturated_fats = safe_extract("//tr[td/a[@data-tooltip='Saturated fatty acids']]", driver)
            sodium = safe_extract("//tr[td/a[@data-tooltip='Sodium']]", driver)
            carbs = safe_extract("//tr[td/a[@data-tooltip='Carbohydrate']]", driver)
            sugar = safe_extract("//tr[td/a[@data-tooltip='Sugars']]", driver)
            protein = safe_extract("//tr[td/a[@data-tooltip='Protein']]", driver)

            data = {
                "productName": product_name,
                "kcal": calories,
                "fat": fat,
                "satFat": saturated_fats,
                "carbs": carbs,
                "sugars": sugar,
                "protein": protein,
                "salt": sodium
            }

            print(f"{product_name}: kcal={calories}, carbs={carbs}, protein={protein}, fat={fat}")
            return data

        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            return {"error": str(e), "URL": url}