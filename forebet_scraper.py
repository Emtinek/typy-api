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
    options.add_argument("start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")  # odkomentuj, jeśli chcesz bez okna

    driver = webdriver.Chrome(service=Service(), options=options)
    wait = WebDriverWait(driver, 10)

    url = "https://www.forebet.com/en/football-tips-and-predictions-for-today"
    driver.get(url)

    # 🔽 Akceptuj cookies
    try:
        accept_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fc-button-label")))
        accept_btn.click()
        print("🟢 Kliknięto akceptację cookies")
    except:
        print("⚠️ Nie znaleziono przycisku cookies")

    time.sleep(3)

    # 🔄 Scrollowanie i klikanie właściwego "More"
    print("🔄 Scrolluję i klikam właściwy 'More'...")
    for i in range(10):  # max 10 razy kliknij More
        try:
            more_btn = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='mrows']//span[text()='More']")))

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_btn)
            time.sleep(2)

            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='mrows']//span[text()='More']"))).click()

            print(f"✅ Kliknięto 'More' (iteracja {i+1})")
            time.sleep(3)
        except Exception as e:
            print("⛔ Nie ma więcej przycisków 'More' lub nie można kliknąć")
            break

    # 🔄 Zbieranie danych
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    all_matches = soup.select(".rcnt")
    print(f"🔢 Znaleziono {len(all_matches)} meczów – filtruję tylko wybrane wyniki...")

    matches = []
    for i, row in enumerate(all_matches, 1):
        try:
            prediction_el = row.select_one(".ex_sc.tabonly")
            if not prediction_el:
                print(f"⚠️ Mecz #{i} brak predykcji – pomijam")
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
                print(f"✅ Mecz #{i} spełnia kryteria: {home} vs {away} - {prediction}")
            else:
                print(f"❌ Mecz #{i} - wynik to {prediction}, nie spełnia kryteriów")
        except Exception as e:
            print(f"⚠️ Mecz #{i} błąd parsowania: {e}")
            continue

    with open("matches.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=4)

    print(f"\n📥 Zapisano {len(matches)} typów do matches.json")

# 🔽 Punkt startowy do uruchamiania samodzielnie tego pliku
if __name__ == "__main__":
    get_forebet_predictions()
