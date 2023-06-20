import csv, json


def import_store_data(file_path):
    store_data = []

    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i >= 1000:
                break

            id = int(row['상가업소번호'])
            name = row['상호명']

            industry_id = row['상권업종대분류코드']
            industry_name = row['상권업종대분류명']

            if industry_id != 'D' and industry_id != 'Q' and industry_id != 'N':
                continue

            city_id = int(row['시도코드'])
            city_name = row['시도명']

            country_id = int(row['시군구코드'])
            country_name = row['시군구명']

            if country_id != 11110 and country_name != 11410:
                continue

            store = {
                'model': 'account_diary.store',
                'fields': {
                    'id': id,
                    'name': name,
                    'industry': industry_id,
                    'city': city_id,
                    'country': country_id,
                }
            }
            store_data.append(store)

    json_file_path = 'store-data.json'
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(store_data, json_file, indent=4, ensure_ascii=False)


# Usage:


def create_industry_records():
    industries = [
        {
            "model": "your_app.industry",
            "pk": "D",
            "fields": {
                "name": "소매"
            }
        },
        {
            "model": "account_diary.industry",
            "pk": "Q",
            "fields": {
                "name": "음식"
            }
        },
        {
            "model": "account_diary.industry",
            "pk": "N",
            "fields": {
                "name": "관광/여가/오락"
            }
        }
    ]

    with open("master-data.json", "w", encoding='utf-8') as jsonfile:
        json.dump(industries, jsonfile, indent=4)


def create_city_records():
    cities = [
        {
            "model": "account_diary.city",
            "pk": 11,
            "fields": {
                "name": "서울특별시"
            }
        }
    ]

    with open("city-data.json", "w", encoding='utf-8') as jsonfile:
        json.dump(cities, jsonfile, indent=4)


def create_country_records():
    countries = [
        {
            "model": "account_diary.country",
            "pk": 11110,
            "fields": {
                "name": "종로구"
            }
        },
        {
            "model": "account_diary.country",
            "pk": 11410,
            "fields": {
                "name": "서대문구"
            }
        }
    ]

    with open("country-data.json", "w", encoding='utf-8') as jsonfile:
        json.dump(countries, jsonfile, indent=4)


if __name__ == '__main__':

    import_store_data('store-info.csv')
