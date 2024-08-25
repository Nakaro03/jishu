from bs4 import BeautifulSoup
import csv
import os

# 保存されたHTMLファイルのディレクトリ
save_directory = 'html-pages'

# HTMLファイルのリストを取得
html_files = [os.path.join(save_directory, f) for f in os.listdir(save_directory) if f.endswith('.html')]

# データを格納するリスト
data_list = []

# 各HTMLファイルから情報を取得してリストに追加する
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

        # 店名を取得
        shop_name = soup.select_one('tr > th:contains("店名") + td > div > span').get_text(strip=True) if soup.select_one('tr > th:contains("店名") + td > div > span') else "N/A"
        print("[INFO] 店名: ", shop_name)

        # 評価を取得
        try:
            rating = soup.select_one(".rdheader-rating__score-val > span").get_text(strip=True)
        except AttributeError:
            rating = "N/A"
        print("[INFO] 評価: ", rating)

        # レビュー件数を取得
        try:
            review_count = soup.select_one('.rdheader-rating__hozon-target .num').get_text(strip=True)
        except:
            review_count = "N/A"
        print("[INFO] レビュー件数: ", review_count)

        # 口コミ件数を取得
        try:
            kuchikomi_count = soup.select_one('.rstdtl-navi__total-count em').get_text(strip=True)
        except Exception as e:
            kuchikomi_count = "N/A"
        print("[INFO] 口コミ件数: ", kuchikomi_count)

        # 口コミテキストを取得
        try:
            review_texts = [text.get_text(strip=True) for text in soup.select('.rstdtl-rvw__comment')]
            review_text = " | ".join(review_texts) if review_texts else "N/A"
        except Exception as e:
            review_text = "N/A"
        print("[INFO] 口コミテキスト: ", review_text)    

        # ジャンルを取得
        genre = soup.select_one('tr > th:contains("ジャンル") + td > span').get_text(strip=True) if soup.select_one('tr > th:contains("ジャンル") + td > span') else "N/A"
        print("[INFO] ジャンル: ", genre)

        # データをリストに追加
        data_list.append([shop_name, rating, review_count, kuchikomi_count, review_text, genre])

# データをCSVファイルに書き込む
csv_filename = "output.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8', errors='replace') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['店名', '評価', 'レビュー件数', '口コミ件数', '口コミテキスト', 'ジャンル'])
    for data in data_list:
        csv_writer.writerow(data)

print("HTMLファイルから情報を取得してCSVファイルに書き込みました。")
