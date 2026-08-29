import os
import pytest

from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.selenium
def test_dashboard_loads_in_chrome(
    frontend_base_url: str,
) -> None:
    options = webdriver.ChromeOptions()

    if os.getenv("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(frontend_base_url)

        wait = WebDriverWait(driver, 10)

        invoice_table = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'table[aria-label="Invoices"]')
            )
        )

        assert invoice_table.is_displayed()

    finally:
        driver.quit()


@pytest.mark.selenium
def test_invoice_search_works_in_chrome(
    frontend_base_url: str,
) -> None:
    options = webdriver.ChromeOptions()

    if os.getenv("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(frontend_base_url)

        wait = WebDriverWait(driver, 10)

        search_input = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "customer-search")
            )
        )

        search_input.send_keys("CUST-001")

        matching_row = wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    '[data-testid="invoice-row-INV-1001"]',
                )
            )
        )

        assert matching_row.is_displayed()

    finally:
        driver.quit()