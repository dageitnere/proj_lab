from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from contextlib import contextmanager
from queue import Queue
import threading
import os


class FirefoxWebdriverPool:
    """
    Thread-safe connection pool for Selenium Firefox webdrivers.
    Ensures drivers are reused and properly managed.
    """

    def __init__(self, pool_size=2, geckodriver_path=None, headless=True):
        """
        Args:
            pool_size: Number of driver instances to maintain
            geckodriver_path: Path to geckodriver executable (optional)
            headless: Run Firefox in headless mode
        """
        self.pool_size = pool_size
        self.geckodriver_path = geckodriver_path
        self.headless = headless
        self.available_drivers = Queue(maxsize=pool_size)
        self.lock = threading.Lock()
        self.initialized = False

    def _create_driver(self):
        """Create a new Firefox webdriver instance"""
        options = webdriver.FirefoxOptions()

        if self.headless:
            options.add_argument("--headless")

        options.set_preference("dom.webnotifications.enabled", False)

        try:
            if self.geckodriver_path and os.path.exists(self.geckodriver_path):
                service = Service(self.geckodriver_path)
            else:
                # Try to use from PATH or system
                try:
                    from webdriver_manager.firefox import GeckoDriverManager
                    service = Service(GeckoDriverManager().install())
                except Exception:
                    service = Service()

            driver = webdriver.Firefox(service=service, options=options)
            return driver
        except Exception as e:
            print(f"Failed to create Firefox webdriver: {e}")
            return None

    def initialize(self):
        """Initialize the driver pool (call once at startup)"""
        with self.lock:
            if self.initialized:
                return

            print(f"Initializing Firefox webdriver pool with {self.pool_size} instances...")
            for i in range(self.pool_size):
                driver = self._create_driver()
                if driver:
                    self.available_drivers.put(driver)
                    print(f"Driver {i + 1}/{self.pool_size} initialized")
                else:
                    print(f"Failed to initialize driver {i + 1}/{self.pool_size}")

            self.initialized = True
            print("Firefox webdriver pool ready!")

    @contextmanager
    def get_driver(self, timeout=15):
        """
        Get a driver from the pool (context manager for safe cleanup)

        Usage:
            with driver_pool.get_driver() as driver:
                driver.get(url)
        """
        driver = None
        try:
            driver = self.available_drivers.get(timeout=timeout)
            if not driver:
                raise Exception("No driver available in pool")
            yield driver
        except Exception as e:
            print(f"Error getting driver: {e}")
            raise
        finally:
            # Return driver to pool for reuse
            if driver:
                try:
                    self.available_drivers.put(driver, timeout=1)
                except Exception as e:
                    print(f"Failed to return driver to pool: {e}")

    def shutdown(self):
        """Close all drivers (call at application shutdown)"""
        print("Shutting down Firefox webdriver pool...")
        while not self.available_drivers.empty():
            try:
                driver = self.available_drivers.get_nowait()
                if driver:
                    driver.quit()
            except Exception as e:
                print(f"Error closing driver: {e}")
        self.initialized = False
        print("Firefox webdriver pool closed")


# Global pool instance
driver_pool = None


def init_firefox_pool(pool_size=2, geckodriver_path=None, headless=True):
    """Initialize the global Firefox driver pool"""
    global driver_pool
    driver_pool = FirefoxWebdriverPool(
        pool_size=pool_size,
        geckodriver_path=geckodriver_path,
        headless=headless
    )
    driver_pool.initialize()


def get_firefox_pool():
    """Get the global Firefox driver pool"""
    global driver_pool
    if driver_pool is None:
        raise RuntimeError("Firefox driver pool not initialized. Call init_firefox_pool() first")
    return driver_pool