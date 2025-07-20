import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def get_forebet_predictions():
    options = Options()
    options.add_argument("--headless=new")                      # ✅ nowy tryb headless
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1280x720")              # ✅ mniejszy viewport
    options.add_argument("--blink-settings=imagesEnabled=false")  # ✅ brak obrazków

    driver = webdriver.Chrome(service=Service(), options=options)
    wait = WebDriverWait(driver, 10)

    url = "https://www.forebet.com/en/football-tips-and-predictions-for-today"
    driver.get(url)

    # 🔽 Cookies
    try:
        accept_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fc-button-label")))
        accept_btn.click()
    except:
        print("⚠️ Nie znaleziono cookies")

    time.sleep(2)

    # 🔄 Klikanie 'More' (ograniczenie do 3 kliknięć)
    for i in range(3):
        try:
            more_btn = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='mrows']//span[text()='More']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_btn)
            time.sleep(2)
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='mrows']//span[text()='More']"))).click()
            time.sleep(3)
        except:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    all_matches = soup.select(".rcnt")
    matches = []

    for row in all_matches:
        try:
            prediction_el = row.select_one(".ex_sc.tabonly")
            if not prediction_el:
                continue
            prediction = prediction_el.text.strip()
            if prediction in ["3 - 0", "4 - 0", "5 - 0", "0 - 3", "0 - 4", "0 - 5"]:
                home = row.select_one(".homeTeam").text.strip()
                away = row.select_one(".awayTeam").text.strip()
                time_match = row.select_one(".date_bah").text.strip()

                matches.append({
                    "match": f"{home} vs {away}",
                    "prediction": prediction,
                    "time": time_match
                })
        except:
            continue

    with open("matches.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=4)


