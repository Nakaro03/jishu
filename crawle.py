from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from time import sleep
import os
import requests

def get_urls_to_csv(url, csv_filename, max_urls=2500):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = '/usr/bin/chromium'

    service = Service('/usr/bin/chromedriver')

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URLを開く
    driver.get(url)
    sleep(5)

    # URLリストの初期化
    href_list = []

    # スクレイピングループを開始
    while len(href_list) < max_urls:
        try:
            # 現在のページの全てのレストランリンクを取得
            wait = WebDriverWait(driver, 15)  # タイムアウトを15秒に設定
            hrefs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.list-rst__rst-name-target.cpy-rst-name")))
            for href in hrefs:
                href_title = href.get_attribute("href")
                if href_title not in href_list:
                    href_list.append(href_title)
                # 必要なURL数に達したらループを終了
                if len(href_list) >= max_urls:
                    break

            # ステータスを表示
            print(f"[INFO] 現在のURL収集数: {len(href_list)}")

            # 次のページに移動
            try:
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@class="c-pagination__item" and position()=last()]/a')))
                next_button.click()
                sleep(3)  # 次のページが読み込まれるのを待つ
            except Exception as e:
                print(f"[ERROR] 次のページに移動できませんでした: {e}")
                break
        except Exception as e:
            print(f"[ERROR] 例外が発生しました: {e}")
            break

    # 収集したURLをCSVファイルに書き込む
    with open(csv_filename, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows([[href] for href in href_list])

    # ドライバーを閉じる
    driver.quit()
    print(f"[INFO] スクレイピングが完了しました。収集したURLの総数: {len(href_list)}")

    return href_list

def save_html_pages(urls, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, url in enumerate(urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"page_{i+1}.html"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"[INFO] Saved {url} as {filename}")
            else:
                print(f"[ERROR] Failed to fetch {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] An error occurred while fetching {url}: {e}")

        sleep(1)  # ウェブサイトに負荷をかけないよう1秒待機

if __name__ == "__main__":
    start_url = "https://tabelog.com/tokyo/rstLst/ramen/"
    output_csv = "ramen_shop_urls.csv"
    html_pages_dir = "html-pages"

    urls = get_urls_to_csv(start_url, output_csv)
    save_html_pages(urls, html_pages_dir)