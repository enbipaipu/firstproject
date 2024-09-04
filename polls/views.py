from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question

from openai import OpenAI


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    chat_ans_header=""
    chat_results=""

    # 「選択肢の候補を表示する」ボタンを押した時の動き
    if request.method == "POST":
        #選択肢のデータを入手
        choice_set = []
        if question.choice_set.exists():
            for choice in question.choice_set.all():
                choice_set.append(choice.choice_text)
        else:
            choice_set = ""

        #プロンプトを定義
        prompt = "次のQuestionとChoiceを参考にして、質問（Question）に対する他の選択肢（Choice）を5つ提示してください。\n出力では引用符や括弧など、リストの構造を示す記号を除去してください。\n" + "Question:" + str(question) + "\n" + "Choice:" + str(choice_set)

        #ターミナル上にChatGPTへのプロンプトを表示させる
        print("============(ChatGPTへのプロンプト)============\n",prompt,"\n========================")

       # ChatGPT
        client = OpenAI(
            base_url = "https://api.openai.iniad.org/api/v1", #INIAD用APIエンドポイント
            api_key = "gaeB7mTywN1CBvomySitOWQZ0fhE0nHowbSf_91CRp3WbpVGt7WoiYDG4Ie5FLO45_4SxaUuQRfY8yXjATMTAhQ", #自身のAPIキーを貼り付け
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini", #3.5-turboでも動くが、INIADが本モデルを推奨

            messages=[
                {
                    "role": "system",
                    "content": "日本語で応答してください。可能な限り少ない文字数で回答してください。"
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
        )

        #ChatGPTの出力結果
        chat_ans_header = 'ChatGPTによる他の選択肢の候補'
        chat_results = response.choices[0].message.content

    context = {
        "question": question,
        'chat_results': chat_results,
        'ans_header': chat_ans_header
    }
    return render(request, "polls/detail.html", context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "ラジオボタンを選択してください",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


#↓追加箇所
def addchoice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        question.choice_set.create(choice_text=request.POST.get('add'), votes=0)
        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))

    else:
        return render(request, "polls/addchoice.html", {"question": question})