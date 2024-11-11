from playwright.sync_api import sync_playwright
import time

# Test 1: Ověření, že stránka www.jobs.cz se správně načte
def test_homepage_load():
    with sync_playwright() as p:
        # Spuštění prohlížeče (Chromium)
        browser = p.chromium.launch(headless=False)  # headless=False pro vizuální kontrolu
        page = browser.new_page()

        # Navigace na stránku www.jobs.cz
        page.goto("https://www.jobs.cz", timeout=60000)  # čekáme až 60 sekund na načtení stránky

        # Ověření titulku stránky
        title = page.title()
        assert "Jobs.cz" in title, f"Expected 'Jobs.cz' in title, but got {title}"

        # Zavření prohlížeče
        browser.close()

# Test 2: Vyhledání pracovních nabídek
def test_job_search():
    with sync_playwright() as p:
        # Spuštění prohlížeče (Chromium)
        browser = p.chromium.launch(headless=False)  # Pro vizuální kontrolu
        page = browser.new_page()

        # Navigace na stránku www.jobs.cz
        page.goto("https://www.jobs.cz", timeout=60000)  # čekáme 60 sekund na načtení stránky

        # Počkejte na vyhledávací pole
        page.wait_for_selector('input[name="searchtext"]', timeout=60000)  # čekáme na vyhledávací pole

        # Vyhledání pozice "Tester"
        page.fill('input[name="searchtext"]', "Tester")
        time.sleep(2)  # čekání 2 sekundy pro zajištění, že se text opravdu vyplní
        page.press('input[name="searchtext"]', "Enter")

        # Počkejte na zobrazení výsledků
        page.wait_for_selector('.offers', timeout=60000)  # čekáme na zobrazení výsledků

        # Ověření, že výsledky obsahují pozici "Tester"
        first_result = page.locator('.offers .offer').first()
        first_result_text = first_result.text_content()
        assert "Tester" in first_result_text, f"Expected 'Tester' in first result, but got {first_result_text}"

        # Zavření prohlížeče
        browser.close()

# Test 3: Ověření, že je možné filtrovat nabídky podle lokality
def test_filter_jobs_by_location():
    with sync_playwright() as p:
        # Spuštění prohlížeče (Chromium)
        browser = p.chromium.launch(headless=False)  # Pro vizuální kontrolu
        page = browser.new_page()

        # Navigace na stránku www.jobs.cz
        page.goto("https://www.jobs.cz", timeout=60000)  # čekáme 60 sekund na načtení stránky

        # Počkejte na vyhledávací pole
        page.wait_for_selector('input[name="searchtext"]', timeout=60000)  # čekáme na vyhledávací pole

        # Vyplnění vyhledávacího pole pro pozici (např. "Tester")
        page.fill('input[name="searchtext"]', "Tester")
        time.sleep(2)  # čekání 2 sekundy pro zajištění, že se text opravdu vyplní
        page.press('input[name="searchtext"]', "Enter")

        # Počkejte na zobrazení výsledků
        page.wait_for_selector('.offers', timeout=60000)  # čekáme na zobrazení výsledků

        # Filtrace pracovních nabídek podle lokality "Kladno"
        page.select_option('select[name="city"]', label="Kladno")

        # Počkejte na zobrazení filtrovaných výsledků
        page.wait_for_selector('.offers', timeout=60000)

        # Ověření, že v některém z výsledků je uvedená lokalita "Kladno"
        first_result_location = page.locator('.offers .offer .location').first().text_content()
        assert "Kladno" in first_result_location, f"Expected location 'Kladno' in the first result, but got {first_result_location}"

        # Zavření prohlížeče
        browser.close()

# Spuštění všech testů
if __name__ == "__main__":
    test_homepage_load()
    test_job_search()
    test_filter_jobs_by_location()

