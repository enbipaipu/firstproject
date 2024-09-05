from django.shortcuts import render, redirect
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

import csv
from .models import Average
from django.http import HttpResponse
from django.conf import settings

from .function.scrape import scrape_cookpad
from .function.db import create_chroma, read_text_chroma, add_text_chroma


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
        
        query = cheaper + question + question
        recipe = read_text_chroma(query)
        
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
        これらのレシピも必要であれば、使用してください。
        {recipe}
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
        response = llm.invoke(template.format(cheaper=cheaper, ingredients=ingredients, question=question, recipe=recipe))
        
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
                Average.objects.update_or_create(
                    code=row[0],
                    defaults={
                        'name': row[1],
                        'g_per_price': to_decimal(row[2]),
                        'price_01': to_decimal(row[3]),
                        'price_02': to_decimal(row[4]),
                        'price_03': to_decimal(row[5]),
                        'price_04': to_decimal(row[6]),
                        'price_05': to_decimal(row[7]),
                        'price_06': to_decimal(row[8]),
                        'price_07': to_decimal(row[9]),
                        'price_08': to_decimal(row[10]),
                        'price_09': to_decimal(row[11]),
                        'price_10': to_decimal(row[12]),
                        'price_11': to_decimal(row[13]),
                        'price_12': to_decimal(row[14]),
                    }
                )
            return HttpResponse("CSVファイルのインポートに成功しました。")
    except FileNotFoundError:
        return HttpResponse("指定されたCSVファイルが見つかりませんでした。")

def create(request):
        result = create_chroma()
        message = result["status"] +":"+ result["message"]
        return HttpResponse(message)


def add_text(request):
    text = ["name:クリスマス＊.°ミニトマトでミニサンタ,comment子供に人気のチーズ、トマトで作ったミニサンタです＊.°このレシピの生い立ちミニトマトと子供のチーズがあったので作ってみました。ミニトマト2パックプロセスチーズ1袋魚肉ソーセージ1袋黒ゴマ少量トマトケチャップ少量ミニトマトを3分の1の所で切ります。2間にプロセスチーズを挟みます。3下に土台で、魚肉ソーセージを輪切りにしたものを置き、ピックですべて刺します。4黒ゴマで目を、ケチャップでほっぺをつけて完成です＊.°子供達から大好評でしたブラックペッパーで目を作ってみました♪",
"クリスマス手作りツナのカプレーゼ切ってのせただけ手作りツナをいただきました。そのままでめっちゃ鬼旨ツナを、Xmas用にカプレーゼにアレンジしました。このレシピの生い立ち職場のお料理上手な先生から、手作りツナを頂戴しました♪缶詰めしか知らなかったのでもう感激。取引のある銀座のお寿司屋さんから分けてもらった貴重な高級マグロ！Xmasメニューに、夕食に考えだしたらワクワクが止まらない。しばらくお付き合いしてね。トマト1個モッツァレラ1個ツナ(手作り)適量バジル4枚マグロの切り身から、2種類のツナを作って、プレゼントしてくれました。両方共、めっちゃ旨一方は味がしっかりついているタイプこちらは、塩気が少ないバージョン。ツナ缶の場合は、水気をしっかりとって使ってねトマトを輪切りモッツァレラも輪切りにし、トマトにのせるバジルの葉を飾り、※をふる味付けはお好みでいいよクックパッドアンバサダー",
"子供パーティ用★手巻きクレープ子どもたちのクリスマスに、手巻き寿司ならぬ、手巻きクレープのパーティはいかがでしょう？　安上がりにも、贅沢にもなります。このレシピの生い立ち赤ちゃん～小中学生～大人の10人以上のパーティで楽な料理を考えました。市販のクレープみたいに何でも巻けます。中身が足りなくなっても、おつまみとしておいてあるサラダや、ソーセージ類を巻けばいいので、大人は飲んでいられます。牛乳400㏄食用油大匙２杯食紅適量食用油（クレープ焼き用）適量クレープの具ミニハンバーグ（orナゲット）４個薄切りハム４枚スモークサーモン４枚トマト1/2個レタス60グラム玉ねぎ１/２個スライスチーズクレープミックス・牛乳・卵・油を滑らかに混ぜ、焼いて冷ます(前日でもOK)。食紅や抹茶で色を付けておくとパーティっぽい。ミニハンバーグ、ナゲットなどを準備し、隠し包丁を入れて、並べておく。（ハンバーグは作っても、市販品でも）野菜も、オニオンスライスはあまり大きくならないようにし、トマトの皮部分にも、切れ目を入れておく。缶詰のミックスフルーツ、あるいは、好みで苺やキウイなども、薄切りにしておく。テーブルに具を並べ、それぞれが好きなものを巻いて食べる。スクランブルエッグやツナマヨディップも子供に好評でした。大きめのお皿を二つくらい用意してテーブルに置き、その上で各自が包めるようにしておくと、パーティテーブルがうまく回ります。例えば子ども系：ハンバーグ・チーズ・レタスマヨネーズ贅沢系：スモークサーモン・オニオンスライス・サワークリーム例えばデザート系：イチゴ・バナナ・キウイ・生クリーム(ココアクレープ皮)和風：柿・生クリーム(抹茶クレープ皮）娘の友だちとクレープパーティー！！いろいろな具で楽しめた♪具材のアイデアいただきま"
]
    result = add_text_chroma(text)
    message = result["status"] +":"+ result["message"]
    return HttpResponse(message)

def read_text(request):
    text = "とまととチーズを使った。子供が喜ぶクリスマス料理"
    result = read_text_chroma(text)
    print(result)
    return HttpResponse(result)
    
    
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

