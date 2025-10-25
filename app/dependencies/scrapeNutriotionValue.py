from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

from app.dependencies.firefoxDriver import get_firefox_pool


def consent(wait):
    """
    Handle cookie consent popup if it appears on the page.

    Args:
        wait (WebDriverWait): WebDriverWait instance used to wait for elements.
    """
    try:
        # Wait until the consent button is clickable and click it
        consent_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fc-button-label")))
        consent_button.click()
        print("Cookie consent accepted.")
        time.sleep(1)  # Small delay to ensure popup is dismissed
    except (TimeoutException, NoSuchElementException):
        # If popup is not found within the timeout or doesn't exist, skip
        print("Cookie consent popup not found")


def safe_extract(xpath, driver):
    """
    Safely extract a numeric nutrition value from a table row using its XPath.

    Args:
        xpath (str): XPath expression for the target nutrient row.
        driver (WebDriver): Active Selenium Firefox driver.

    Returns:
        float: Extracted nutrient value, or 0.0 if element not found.
    """
    try:
        # Locate the row and get the text content from the right-aligned cell
        row = driver.find_element(By.XPATH, xpath)
        text = row.find_element(By.XPATH, "./td[@class='right']").text.strip()
        # Convert text like "12.3 g" → 12.3
        return float(text.split(" ")[0]) if text else 0.0
    except NoSuchElementException:
        # Return default value if the element is missing
        return 0.0


def get_product_data_from_url(url):
    """
    Extract nutrition data for a product from a given nutritionvalue.org URL.

    Steps:
        1. Open the URL in a pooled Firefox driver.
        2. Handle cookie consent popup (if any).
        3. Select a 100g serving size.
        4. Extract key nutrient values (calories, fat, protein, carbs, etc.).
        5. Return structured nutrition data.

    Args:
        url (str): Product page URL on nutritionvalue.org.

    Returns:
        dict: Dictionary containing product name and nutrition data,
              or an error message if extraction fails.
    """
    pool = get_firefox_pool()  # Get the shared Firefox driver pool

    # Use a context manager to acquire and release a driver safely
    with pool.get_driver() as driver:
        wait = WebDriverWait(driver, 1)
        try:
            # Load the product page
            driver.get(url)
            time.sleep(2)  # Allow the page to fully render

            # Handle cookie consent popup
            consent(wait)

            # Try to extract the product name, fallback if not found
            try:
                product_name = driver.find_element(By.ID, "food-name").text
            except NoSuchElementException:
                product_name = "Unknown Product"

            # Attempt to select the "100 g" serving option
            try:
                dropdown = Select(driver.find_element(By.CSS_SELECTOR, "select.serving[name='size']"))
                dropdown.select_by_visible_text("100 g")
                time.sleep(1)
            except NoSuchElementException:
                print(f"Could not find serving dropdown for {product_name}")

            # Extract calorie value
            try:
                calories = float(driver.find_element(By.ID, 'calories').text)
            except (NoSuchElementException, ValueError):
                calories = 0.0

            # Extract macronutrients and sodium values
            fat = safe_extract("//tr[td/a[@data-tooltip='Fat']]", driver)
            saturated_fats = safe_extract("//tr[td/a[@data-tooltip='Saturated fatty acids']]", driver)
            sodium = safe_extract("//tr[td/a[@data-tooltip='Sodium']]", driver)
            carbs = safe_extract("//tr[td/a[@data-tooltip='Carbohydrate']]", driver)
            sugar = safe_extract("//tr[td/a[@data-tooltip='Sugars']]", driver)
            protein = safe_extract("//tr[td/a[@data-tooltip='Protein']]", driver)

            # Combine extracted data into a structured dictionary
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
            # Log and return error details for debugging
            print(f"Error processing URL {url}: {e}")
            return {"error": str(e), "URL": url}