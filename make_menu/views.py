from django.shortcuts import render
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# Create your views here.
def index(request):
    ingredientsInRefrigerator = ["ニンジン", "玉ねぎ", "レタス"]
    request = request
    context = {"text": "hello world", "foods": ingredientsInRefrigerator}
    return render(request, "make_menu/index.html", context)
    
    
def result(request):
    context = ""
    if request.method == 'POST':
        selectIngredients = request.POST.get('select_ingredients')
        detail = request.POST.get('detail')
        
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
        食材: {context}
        detail: {question}
        """
        order = """回答のフォーマットは以下のようにしてください。料理を３つ提案してください。
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
        output_by_simple_llm = llm.invoke(order)
        context = {
            "selectIngredients": selectIngredients,
            "detail": detail,
        }

    return render(request, 'make_menu/result.html', context)
    