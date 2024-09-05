import requests
import pandas as pd
import math
from make_menu.models import Average

def call_food_api(cat):
    base_url = "https://api.cultivationdata.net/mcdata"
    params = {
        "mc": 51300,
        "cat": cat,

    }

    # APIリクエスト
    response = requests.get(base_url, params=params)
    return response.json()
    
    
def read_average_price(itemName, month):
    MONTH = f"price_{month:02}"
    try:
        my_object = Average.objects.get(name=itemName)
        return getattr(my_object, MONTH), my_object.g_per_price
    except Average.DoesNotExist:
        return None, None  # 該当するレコードが存在しない場合




def get_cheap_foods(cat):
    food_data = call_food_api(cat)
    Low_price = []

    for key in food_data:
        price = 0
        weight = 0
        yenPerKg = 0
        if key not in ["Date", "MarketName", "MarketCode"]:
            # itemCodeの前後の空白文字を削除
            itemName = key.strip()
            Average_price, gram = read_average_price(itemName, 9)
            if Average_price is not None and gram > 0:
              for key in food_data[itemName]:
                  # Ignoring the 'ItemCode' key, only considering data entries
                  if key != "ItemCode":
                      item = food_data[itemName][key]
                      # Converting relevant fields to floats or integers
                      PRICE = item["LowPrice"]
                      if PRICE == '-':
                        PRICE = item["MediumPrice"]
                      if PRICE == '-' or PRICE == 'nan':
                        continue
                      low_price = int(PRICE)
                      wgt_per_package = float(item["WeightPerPackage"])

                      price += low_price
                      weight += wgt_per_package
              # Ensure weight is not zero to avoid division by zero
              if price == 0:
                continue
              if weight != 0:
                  yenPerKg = math.floor(price / weight)
              else:
                  yenPerKg = 0

              diff = (yenPerKg - Average_price) // gram
              if diff < 0:
                Low_price.append([itemName, diff])
    print(Low_price)
    return Low_price


def diff():
    vegetables = get_cheap_foods("v")
    fruit = get_cheap_foods("f")
    cheap_foods = [*vegetables, *fruit]
    return cheap_foods
    
    
