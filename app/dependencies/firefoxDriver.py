from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from contextlib import contextmanager
from queue import Queue
import threading
import os


class FirefoxWebdriverPool:
    """
    Thread-safe connection pool for Selenium Firefox webdrivers.
    This class maintains a pool of driver instances that can be reused across threads,
    avoiding the overhead of repeatedly starting new browser instances.
    """

    def __init__(self, pool_size=2, geckodriver_path=None, headless=True):
        """
        Initialize the webdriver pool.

        Args:
            pool_size (int): Number of Firefox webdriver instances to create.
            geckodriver_path (str): Optional path to the geckodriver executable.
            headless (bool): Whether to run Firefox in headless mode (no GUI).
        """
        self.pool_size = pool_size
        self.geckodriver_path = geckodriver_path
        self.headless = headless
        self.available_drivers = Queue(maxsize=pool_size)  # Thread-safe queue for available drivers
        self.lock = threading.Lock()                       # Lock to ensure thread-safe initialization
        self.initialized = False                           # Prevent re-initialization

    def _create_driver(self):
        """
        Internal method to create a single Firefox webdriver instance.

        Returns:
            webdriver.Firefox | None: A configured Firefox driver or None if creation fails.
        """
        options = webdriver.FirefoxOptions()

        # Enable headless mode if specified
        if self.headless:
            options.add_argument("--headless")

        # Disable Firefox notifications
        options.set_preference("dom.webnotifications.enabled", False)

        try:
            # Use a specific geckodriver path if provided, otherwise install automatically
            if self.geckodriver_path and os.path.exists(self.geckodriver_path):
                service = Service(self.geckodriver_path)
            else:
                try:
                    # Attempt to install geckodriver automatically via webdriver-manager
                    from webdriver_manager.firefox import GeckoDriverManager
                    service = Service(GeckoDriverManager().install())
                except Exception:
                    # Fall back to default Service configuration if manager fails
                    service = Service()

            # Create and return the Firefox driver
            driver = webdriver.Firefox(service=service, options=options)
            return driver

        except Exception as e:
            print(f"Failed to create Firefox webdriver: {e}")
            return None

    def initialize(self):
        """
        Create and populate the pool with Firefox driver instances.
        Should be called once before using the pool.
        """
        with self.lock:
            if self.initialized:
                # Avoid initializing twice
                return

            print(f"Initializing Firefox webdriver pool with {self.pool_size} instances...")

            # Create drivers and add them to the queue
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
        Context manager to safely acquire and release a driver.

        Args:
            timeout (int): How long to wait (in seconds) for a driver to become available.

        Yields:
            webdriver.Firefox: A Firefox driver from the pool.

        Raises:
            Exception: If no driver is available within the timeout.
        """
        driver = None
        try:
            # Attempt to get a driver from the queue
            driver = self.available_drivers.get(timeout=timeout)
            if not driver:
                raise Exception("No driver available in pool")
            yield driver  # Provide the driver to the calling context
        except Exception as e:
            print(f"Error getting driver: {e}")
            raise
        finally:
            # Always return the driver back to the pool, even if an error occurred
            if driver:
                try:
                    self.available_drivers.put(driver, timeout=1)
                except Exception as e:
                    print(f"Failed to return driver to pool: {e}")

    def shutdown(self):
        """
        Gracefully close all drivers and empty the pool.
        Should be called when the application is shutting down.
        """
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


# --- Global Pool Instance and Helper Functions ---

driver_pool = None  # Singleton-like global reference to the pool


def init_firefox_pool(pool_size=2, geckodriver_path=None, headless=True):
    """
    Initialize the global Firefox webdriver pool.

    Args:
        pool_size (int): Number of drivers to maintain.
        geckodriver_path (str): Optional custom path to geckodriver.
        headless (bool): Run Firefox in headless mode.
    """
    global driver_pool
    driver_pool = FirefoxWebdriverPool(
        pool_size=pool_size,
        geckodriver_path=geckodriver_path,
        headless=headless
    )
    driver_pool.initialize()


def get_firefox_pool():
    """
    Retrieve the global Firefox webdriver pool instance.

    Returns:
        FirefoxWebdriverPool: The global driver pool.

    Raises:
        RuntimeError: If the pool has not been initialized yet.
    """
    global driver_pool
    if driver_pool is None:
        raise RuntimeError("Firefox driver pool not initialized. Call init_firefox_pool() first")
    return driver_pool
