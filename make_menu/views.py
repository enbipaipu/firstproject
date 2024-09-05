from django.shortcuts import render, redirect
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

import csv
from .models import Average
from django.http import HttpResponse
from django.conf import settings

from .function.scrape import scrape_cookpad



# Create your views here.
def index(request):
    # 冷蔵庫DBから食材を取得
    ingredientsInRefrigerator = ["ニンジン", "玉ねぎ", "レタス"]
    
    # (API-平均)の値を返す
    CheaperFoods = ["じゃがいも(-20円)", "キャベツ(-15円)", "ナス(-30円)"]
    
    request = request
    context = {"text": "hello world",
        "refrigerator": ingredientsInRefrigerator,
        "cheaper": CheaperFoods,
    }
    return render(request, "make_menu/index.html", context)
    
    
def result(request):
    context = ""
    if request.method == 'POST':
        cheaper = request.POST.get('select_cheaper')
        ingredients = request.POST.get('select_ingredients')
        question = request.POST.get('detail')
        
        # .envファイルの内容を読み込みます
        load_dotenv()
        
        
        # LLMを定義。今回はChatGPTの4o-miniを利用する
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0,
            openai_api_base= os.getenv("URL"),
            openai_api_key = os.getenv("OPEN_API_KEY"),
            verbose=True
            )
        
        template = """以下の食材とdetailに沿った献立を考えてください。
        安くなっている食材: {cheaper}
        冷蔵庫の中の食材: {ingredients}
        detail: {question}
        食材はなるべく多く使用してください。
        """
        
        Input = """回答のフォーマットは以下のようにしてください。料理を３つ提案してください。
        ----
        料理名:料理名
        使用する食材：使用する食材1(冷蔵庫の中にあるor例年より何円安くなっているか)
                  使用する食材2(冷蔵庫の中にあるor例年より何円安くなっているか)
    
        作り方：1. 手順1
               2. 手順2
    
        特徴：子供でも食べやすい、ヘルシー、夏バテ解消など
        ----
        見やすくするための空白行
        """
        response = llm.invoke(template.format(cheaper=cheaper, ingredients=ingredients, question=question))
        
        output_by_simple_llm = response.content
        
        print(type(response))
        print(type(output_by_simple_llm))
        print(output_by_simple_llm)
        
        context = {
            "res": output_by_simple_llm,
        }

    return render(request, 'make_menu/result.html', context)

    
    
def read_csv(request):
    # プロジェクトのベースディレクトリを取得
    base_dir = settings.BASE_DIR
    file_path = os.path.join(base_dir, "make_menu", "csv", "merged_avg.csv")
    
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # ヘッダーをスキップ
            for row in reader:
                if len(row) < 14:
                    return HttpResponse(f"CSVファイルの行に不足している列があります。行: {row}")
                
                # 空文字列を0に変換
                def to_decimal(value):
                    return float(value) if value else 0
                
                # 新規作成または更新
                obj, created = Average.objects.update_or_create(
                    code=row[0],
                    defaults={
                        'name': row[1],
                        'price_01': to_decimal(row[2]),
                        'price_02': to_decimal(row[3]),
                        'price_03': to_decimal(row[4]),
                        'price_04': to_decimal(row[5]),
                        'price_05': to_decimal(row[6]),
                        'price_06': to_decimal(row[7]),
                        'price_07': to_decimal(row[8]),
                        'price_08': to_decimal(row[9]),
                        'price_09': to_decimal(row[10]),
                        'price_10': to_decimal(row[11]),
                        'price_11': to_decimal(row[12]),
                        'price_12': to_decimal(row[13]),
                    }
                )
            return HttpResponse("CSVファイルのインポートに成功しました。")
    except FileNotFoundError:
        return HttpResponse("指定されたCSVファイルが見つかりませんでした。")


def scrape(request):
    if request.method == 'POST':
        # フォームから入力されたテキストを取得
        input_text = request.POST.get('input_text')
        
        if input_text:
            # スクレイピング関数を呼び出し
            scraped_recipes = scrape_cookpad(input_text)
            
            if scraped_recipes:
                # 各要素をHTMLとしてテンプレートに渡す
                return render(request, 'make_menu/scrape.html', {'recipes': scraped_recipes})
            else:
                return render(request, 'make_menu/scrape.html', {'error': 'データが取得できませんでした。'})
    
    # フォームを表示
    return render(request, 'make_menu/scrape.html')

