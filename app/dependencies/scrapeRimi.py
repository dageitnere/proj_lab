import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from app.dependencies.firefoxDriver import get_firefox_pool

# Map Latvian nutrition terms to standardized English keys
NUTRITION_MAP = {
    "enerģētiskā vērtība": "kcal",
    "tauki": "fat",
    "tostarp piesātinātās taukskābes": "satFat",
    "ogļhidrāti": "carbs",
    "tostarp cukuri": "sugars",
    "olbaltumvielas": "protein",
    "sāls": "salt"
}


def handle_cookie_consent(driver, wait):
    """
    Close or decline cookie consent popup on Rimi.lv (if present).

    Args:
        driver: Selenium WebDriver instance.
        wait (WebDriverWait): Wait helper to manage dynamic elements.
    """
    try:
        # Wait for the "Decline" button to become clickable, then click it
        consent_button = wait.until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonDecline"))
        )
        consent_button.click()
        time.sleep(1)  # Short pause to ensure popup closes
    except TimeoutException:
        # No consent popup appeared within timeout
        pass


def click_modal_close_button(driver, wait):
    """
    Close marketing or promotional modal popup if one appears.

    Args:
        driver: Selenium WebDriver instance.
        wait (WebDriverWait): Wait helper for synchronization.
    """
    try:
        # Wait for the close ("X") button inside modal and click it
        close_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="modal__close"]'))
        )
        driver.execute_script("arguments[0].click();", close_button)
        time.sleep(1)
    except TimeoutException:
        # Popup not found or already closed
        pass


def parse_nutrition_value(name: str, value: str):
    """
    Parse a single nutrition entry (e.g., "Tauki 12 g") into structured data.

    Args:
        name (str): Nutrient name in Latvian (e.g. "tauki").
        value (str): Raw value string, possibly containing units (e.g. "12,5 g").

    Returns:
        dict: { standardized_key: numeric_value } or empty dict if unrecognized.
    """
    name = name.strip().lower()
    value = value.replace(",", ".").strip()

    # Special case: energy value (contains both kJ and kcal)
    if "enerģētiskā vērtība" in name and "/" in value:
        parts = re.findall(r"(\d+(?:\.\d+)?)", value)
        if len(parts) >= 2:
            return {"kcal": float(parts[1])}
        elif parts:
            return {"kcal": float(parts[0])}

    # Extract the first numeric value from text
    match = re.search(r"(\d+(?:\.\d+)?)", value)
    if match:
        key = NUTRITION_MAP.get(name, None)
        if key:
            return {key: float(match.group(1))}
    return {}  # Return empty if parsing fails


def scrape_rimi_product(url: str, mass_g: float = None):
    """
    Scrape Rimi.lv product data including name, price, and nutrition values.

    Workflow:
        1. Acquire a Firefox driver from the shared pool.
        2. Visit the product page and close any modals/popups.
        3. Extract product name and price (€/kg or €/gab.).
        4. Parse nutrition table into structured fields.
        5. Return all data as a dictionary.

    Args:
        url (str): Product page URL on rimi.lv.
        mass_g (float, optional): Product mass in grams, used if price is per unit.

    Returns:
        dict: Contains:
            - productName (str)
            - price1Kg (float)
            - price100g (float)
            - nutrition fields (kcal, fat, carbs, etc.)
            - error message if applicable
    """
    pool = get_firefox_pool()

    # Acquire a driver safely using the pool context manager
    with pool.get_driver() as driver:
        wait = WebDriverWait(driver, 2)  # Short wait time for dynamic content

        try:
            # --- LOAD PAGE & HANDLE POPUPS ---
            driver.get(url)
            time.sleep(1)
            handle_cookie_consent(driver, wait)
            click_modal_close_button(driver, wait)

            data = {}

            # --- PRODUCT NAME ---
            try:
                name_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.name")))
                data["productName"] = name_elem.text.strip()
            except Exception as e:
                print(f"Failed to extract name: {e}")
                data["productName"] = None

            # --- PRICE EXTRACTION ---
            try:
                price_elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "price-per")))
                price_text = price_elem.text.strip()
                print("DEBUG:", repr(price_text))  # Example: "0,32€/gab."
                print("mass_g sent is:", mass_g)

                # Extract numeric price from text (handles commas and decimals)
                match = re.search(r"(\d+[.,]?\d*)", price_text)
                if match:
                    price_value = float(match.group(1).replace(",", "."))

                    # If price is per unit, compute per kg/100g using mass_g
                    if "/gab" in price_text.lower():
                        if not mass_g:
                            data["error"] = "Mass in grams required for unit price calculation"
                            return data
                        price_per_kg = round(price_value / (mass_g / 1000), 2)
                        price_per_100g = round(price_per_kg / 10, 2)
                    else:
                        # If price is already per kg
                        price_per_kg = price_value
                        price_per_100g = round(price_per_kg / 10, 2)

                    data["price1Kg"] = price_per_kg
                    data["price100g"] = price_per_100g
                else:
                    # Price not found or unrecognized format
                    data["price1Kg"] = None
                    data["price100g"] = None
            except Exception as e:
                print(f"Failed to extract price: {e}")
                data["price1Kg"] = None
                data["price100g"] = None

            # --- NUTRITION TABLE ---
            nutrition = {}
            try:
                # Locate and iterate through all rows in the nutrition table
                table_rows = driver.find_elements(By.CSS_SELECTOR, ".product__table table tbody tr")
                for row in table_rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) == 2:
                        name = cols[0].text.strip()
                        val = cols[1].text.strip()
                        parsed = parse_nutrition_value(name, val)
                        nutrition.update(parsed)
                data.update(nutrition)
            except Exception as e:
                print(f"Failed to extract nutrition: {e}")

            return data

        except Exception as e:
            print(f"Error scraping Rimi product: {e}")
            raise  # Propagate for higher-level error handling