import requests
from bs4 import BeautifulSoup
import json
import csv

url = "https://fitaudit.ru/food"
headers = {
    "accept": "*/*",
    "User-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

req = requests.get(url, headers=headers)
src = req.text

with open("index.html", "w") as file:
    file.write(src)

with open("index.html") as file:
    src = file.read()

def shearing(prod):
    result = prod.split()
    final = ""
    for i in result:
        final += i + " "
    return final.strip()

soup = BeautifulSoup(src, "lxml")
all_categories_href = soup.find_all(class_="fimlist__title_groups")
all_fimlist_href = soup.find_all(class_="fimlist__items")

fimlist_array = []
for item in all_categories_href:
    fimlist_array.append(item.text)

all_products_dict = {}
iteration_count = 0
counter = 0
for item in all_fimlist_href:
    product_dict = {}
    products_href = item.find_all(class_="vertical_pseudo")
    for products in products_href:
        text = shearing(products.text)
        url = products.get("href")
        product_dict[text] = url
        iteration_count += 1
    all_products_dict[fimlist_array[counter]] = product_dict
    counter += 1

with open("all_categories_dict.json", "w") as file:
    json.dump(all_products_dict, file, indent=4, ensure_ascii=False)

with open("all_categories_dict.json") as file:
    all_categories = json.load(file)
counter = 0
count = 0
print(f"Всего итераций: {iteration_count}")
for category_name, product_name in all_categories.items():
    with open(f"data/СSV and JSON/{counter}_{category_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Продукт",
                "Калорийность",
                "Белки",
                "Жиры",
                "Углеводы",
                " ",
                "Витамин А",
                "Бета-каротин",
                "Альфа-каротин",
                "Витамин D",
                "Витамин D2",
                "Витамин D3",
                "Витамин E",
                "Витамин K",
                "Витамин C",
                "Витамин B1",
                "Витамин B2",
                "Витамин B3",
                "Витамин B4",
                "Витамин B5",
                "Витамин B6",
                "Витамин B9",
                "Витамин B12",
                " ",
                "Кальций",
                "Железо",
                "Магний",
                "Фосфор",
                "Калий",
                "Натрий",
                "Цинк",
                "Медь",
                "Марганец",
                "Селен",
                "Фтор"
            )
        )
    for item in product_name:
        req = requests.get(url=product_name[item], headers=headers)
        src = req.text

        # with open(f"data/HTMLs/{count}_{item}.html", "w") as file:
        #     file.write(src)

        with open(f"data/HTMLs/{count}_{item}.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        # Собираем заголовки страницы
        table_head = soup.find_all(class_="tbl-value")
        values = [item, soup.find(class_="him_bx__legend_text").find(class_="js__msr_cc").text]
        for i in range(33):
            if i != 3 or i != 21:
                values.append(shearing(table_head[i].text))
            else:
                values.append(" ")

        with open(f"data/СSV and JSON/{counter}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(values)

        # Собираем данные продуктов
        products_info = {
            "Продукт": values[0],
            "Калорийность": values[1],
            "Белки": values[2],
            "Жиры": values[3],
            "Углеводы": values[4],
            "Витамин А": values[6],
            "Бета-каротин": values[7],
            "Альфа-каротин": values[8],
            "Витамин D": values[9],
            "Витамин D2": values[10],
            "Витамин D3": values[11],
            "Витамин E": values[12],
            "Витамин K": values[13],
            "Витамин C": values[14],
            "Витамин B1": values[15],
            "Витамин B2": values[16],
            "Витамин B3": values[17],
            "Витамин B4": values[18],
            "Витамин B5": values[19],
            "Витамин B6": values[20],
            "Витамин B9": values[21],
            "Витамин B12": values[22],
            "Кальций": values[24],
            "Железо": values[25],
            "Магний": values[26],
            "Фосфор": values[27],
            "Калий": values[28],
            "Натрий": values[29],
            "Цинк": values[30],
            "Медь": values[31],
            "Марганец": values[32],
            "Селен": values[33],
            "Фтор": values[34],
        }

        with open(f"data/СSV and JSON/{counter}_{category_name}.json", "a", encoding="utf-8") as file:
            json.dump(products_info, file, indent=4, ensure_ascii=False)

        count += 1
        print(f"# Итерация {count}. {item} записан...")
        iteration_count -= 1

        if iteration_count == 0:
            print("Работа завершена")
            break

        print(f"Осталось итераций: {iteration_count}")

    counter += 1
