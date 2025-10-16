import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from app.dependencies.firefoxDriver import get_firefox_pool
from selenium.webdriver.support.ui import WebDriverWait

# --- Nutrition key mapping ---
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
    """Handle cookie consent popup"""
    try:
        consent_button = wait.until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonDecline"))
        )
        consent_button.click()
        time.sleep(1)
    except TimeoutException:
        pass


def click_modal_close_button(driver, wait):
    """Close modal popup if present"""
    try:
        close_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="modal__close"]'))
        )
        driver.execute_script("arguments[0].click();", close_button)
        time.sleep(1)
    except TimeoutException:
        pass


def parse_nutrition_value(name: str, value: str):
    """Parse nutrition value from text"""
    name = name.strip().lower()
    value = value.replace(",", ".").strip()

    if "enerģētiskā vērtība" in name and "/" in value:
        parts = re.findall(r"(\d+(?:\.\d+)?)", value)
        if len(parts) >= 2:
            return {"kcal": float(parts[1])}
        elif parts:
            return {"kcal": float(parts[0])}

    match = re.search(r"(\d+(?:\.\d+)?)", value)
    if match:
        key = NUTRITION_MAP.get(name, None)
        if key:
            return {key: float(match.group(1))}
    return {}


def scrape_rimi_product(url: str, mass_g: float = None):
    """
    Scrapes product name, price per kg/100g, and nutrition info from Rimi.lv.
    Uses driver from pool to avoid connection issues.

    Args:
        url: Product URL from rimi.lv
        mass_g: Mass in grams (required if price is per unit)

    Returns:
        dict: Product data including name, prices, and nutrition info
    """
    pool = get_firefox_pool()

    with pool.get_driver() as driver:
        # Create a wait object for this driver
        wait = WebDriverWait(driver, 2)

        try:
            driver.get(url)
            time.sleep(1)
            handle_cookie_consent(driver, wait)
            click_modal_close_button(driver, wait)

            data = {}

            # --- NAME ---
            try:
                name_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.name")))
                data["productName"] = name_elem.text.strip()
            except Exception as e:
                print(f"Failed to extract name: {e}")
                data["productName"] = None

            # --- PRICE ---
            try:
                price_elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "price-per")))
                price_text = price_elem.text.strip()

                match = re.search(r"(\d+[.,]?\d*)", price_text)
                if match:
                    price_value = float(match.group(1).replace(",", "."))

                    if "/gab" in price_text.lower():
                        if not mass_g:
                            raise ValueError("Mass per unit is required when price is per unit (/gab.)")

                        price_per_kg = round(price_value / (mass_g / 1000), 2)
                        price_per_100g = round(price_per_kg / 10, 2)
                    else:
                        price_per_kg = price_value
                        price_per_100g = round(price_per_kg / 10, 2)

                    data["price1Kg"] = price_per_kg
                    data["price100g"] = price_per_100g
                else:
                    data["price1Kg"] = None
                    data["price100g"] = None
            except Exception as e:
                print(f"Failed to extract price: {e}")
                data["price1Kg"] = None
                data["price100g"] = None

            # --- NUTRITION TABLE ---
            nutrition = {}
            try:
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
            raise