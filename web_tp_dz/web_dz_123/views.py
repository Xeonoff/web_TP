from django.shortcuts import render
from web_dz_123 import models
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#def getAnswers():
#    return [
#    {
#        "id": i,
#        "text": f"Dear {i}, in our fast-paced world, effective communication often demands brevity without sacrificing substance. Short answers, characterized by their conciseness and clarity, are crucial tools in the communicator's arsenal.",
#    } for i in range(50)
#] 

#def getQuestions():
#    return[
#        {
#            'title': 'title' + str(i),
#            'id': i,
#            'text': 'text' + str(i),
#            "tags": ['tag'+'tag'*(i%3), 'tag2'+'tag2'*(i%3)],
#        }for i in range(1,30)
#    ]

#questions = getQuestions()
#answers = getAnswers() #Вот бы в жизни такую функцию иметь, даже без http запроса

def paginate(request, items, num_items=5): #напишем одну функцию для пагинации чтобы не писать в каждой вьюююююююю
    page_num = request.GET.get('page', 1)
    paginator = Paginator(items, num_items)
    
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def index(request):
    page_obj = paginate(request, models.Question.objects.get_new())
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    return render(request, "index.html", {"questions": page_obj, "popular_tags" : pop_tags, "best_members" : b_mem})

def question(request, pk):
    item = models.Question.objects.get_one_question(pk)
    page_obj = paginate(request, models.Answer.objects.by_question(pk))
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    return render(request, "question.html", {"question": item, "answers": page_obj, "popular_tags" : pop_tags, "best_members" : b_mem})

def ask(request):
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    return render(request, 'ask.html', {"popular_tags" : pop_tags, "best_members" : b_mem})

def login(request):
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    return render(request, "login.html", {"popular_tags" : pop_tags, "best_members" : b_mem})

def signup(request):
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    return render(request, 'signup.html', {"popular_tags" : pop_tags, "best_members" : b_mem})

def hot(request):
    page_obj = paginate(request, models.Question.objects.get_hot())
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    return render(request, "hot.html", {"questions": page_obj, "popular_tags" : pop_tags, "best_members" : b_mem})

def tag(request, name):
    page_obj = paginate(request, models.Question.objects.by_tag(name))
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    return render(request, "tag.html", {"questions": page_obj, "tag": name, "popular_tags" : pop_tags, "best_members" : b_mem})

def settings(request):
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    return render(request, "settings.html", {"popular_tags" : pop_tags, "best_members" : b_mem})

def member(request, member_name):
    user_profile = models.Profile.objects.get_one_member(member_name)
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    return render(request, "member.html", {"member": user_profile, "popular_tags" : pop_tags, "best_members" : b_mem})