from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def getAnswers():
    return [
    {
        "id": i,
        "text": f"Dear {i}, in our fast-paced world, effective communication often demands brevity without sacrificing substance. Short answers, characterized by their conciseness and clarity, are crucial tools in the communicator's arsenal.",
    } for i in range(50)
] 

def getQuestions():
    return[
        {
            'title': 'title' + str(i),
            'id': i,
            'text': 'text' + str(i),
            "tags": ['tag'+'tag'*(i%3), 'tag2'+'tag2'*(i%3)],
        }for i in range(1,30)
    ]

questions = getQuestions()
answers = getAnswers() #Вот бы в жизни такую функцию иметь, даже без http запроса
def paginate(request, items):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(items, 5)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def index(request):
    page_obj = paginate(request, questions)
    return render(request, "index.html", {"questions": page_obj})

def question(request, pk):
    item = questions[pk]
    page_obj = paginate(request, answers)
    return render(request, "question.html", {"question": item, "answers": page_obj})

def ask(request):
    return render(request, 'ask.html')

def login(request):
    is_auth = True
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def hot(request):
    page_obj = paginate(request, questions)
    return render(request, "hot.html", {"questions": page_obj},)

def tag(request, name):
    Questions = [question for question in questions if name in question['tags']]
    page_obj = paginate(request, Questions)
    return render(request, "tag.html", {"questions": page_obj, "tag": name})

def settings(request):
    return render(request, "settings.html")