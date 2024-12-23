from django.shortcuts import render, redirect, get_object_or_404
from web_dz_123 import models
from django.http import  HttpResponse
from django.contrib import auth
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from web_dz_123.forms import LoginForm, RegisterForm, SettingsForm, AskForm, AnswerForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse, resolve, Resolver404
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect

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

@require_http_methods(['GET', 'POST'])
def question(request, pk):
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    item = models.Question.objects.get_one_question(pk)
    if request.method == 'GET':
        answer_form = AnswerForm()
        print("I`m here")
    if request.method == 'POST':
        print("I`m here")
        if request.user.is_authenticated:
            answer_form = AnswerForm(data = request.POST, author=models.Profile.objects.get(user=request.user), question=item)
            if answer_form.is_valid():
                new_answer = answer_form.save()
                if new_answer:
                    answers = models.Answer.objects.all().filter(question=pk)
                    pos = 0
                    for answer in answers:
                        pos += 1
                        if (answer == new_answer):
                            break
                    return redirect(reverse('question', kwargs={'pk':pk}) + '?page=' + str(pos // 5 + 1))
        else:
            return redirect(reverse('login'))
    page_obj = paginate(request, models.Answer.objects.by_question(pk))
    return render(request, "question.html", {"question": item, "answers": page_obj, "form":answer_form, "popular_tags" : pop_tags, "best_members" : b_mem})

@login_required(login_url='login')
def ask(request):
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    if request.method == 'GET':
        ask_form = AskForm()
        print("I`m here")
    if request.method == 'POST':
        print("I`m here")
        ask_form = AskForm(data = request.POST, author=models.Profile.objects.get(user=request.user))
        if ask_form.is_valid():
            question = ask_form.save()
            return redirect(reverse('question', kwargs={'pk':question.id}))
    return render(request, "ask.html", {'form' : ask_form, "popular_tags" : pop_tags, "best_members" : b_mem})


@require_http_methods(['GET', 'POST'])
def login(request):
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    redirect_page = request.GET.get('next', 'index')
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, 'Wrong login or password')
                login_form.add_error('username', '')
                login_form.add_error('password', '')
    return render(request, "login.html", context={"form":login_form, "redirect_after":redirect_page, "popular_tags" : pop_tags, "best_members" : b_mem})

@require_http_methods(['GET', 'POST'])
def signup(request):
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    if request.method == 'GET':
        print("I`m here")
        user_form = RegisterForm()
        return render(request, "signup.html", context={'form':user_form})
    if request.method == 'POST':
        print("I`m here")
        user_form = RegisterForm(data=request.POST)
        if user_form.is_valid():
            try:
                user = user_form.save()
                if user:
                    auth.login(request, user)
                    return redirect(reverse('index'))
            except IntegrityError:
                user_form.add_error(field='username', error='User already exists.')
    return render(request, "signup.html", context={'form':user_form, "popular_tags" : pop_tags, "best_members" : b_mem})

@login_required(login_url='login')
def logout(request):
    redirect_page = request.GET.get('next', 'index')

    try:
        resolve(redirect_page)
    except Resolver404:
        redirect_page = 'index'

    auth.logout(request)
    return redirect(redirect_page)

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

@login_required(login_url='login')
def settings(request):
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    if request.method == 'GET':
        settings_form = SettingsForm(user=request.user, avatar=models.Profile.objects.get(user=request.user).avatar)
    if request.method == 'POST':
        settings_form = SettingsForm(user=request.user, data=request.POST, files=request.FILES)
        if settings_form.is_valid():
            user = settings_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('settings'))
            
    return render(request, "settings.html", {'form':settings_form, 'user':request.user, "popular_tags" : pop_tags, "best_members" : b_mem})

def member(request, member_name):
    Profile = models.Profile.objects.get_one_member(member_name)
    pop_tags = models.Tag.objects.get_popular()
    b_mem = models.Profile.objects.best_members()
    return render(request, "member.html", {"member": Profile, "popular_tags" : pop_tags, "best_members" : b_mem})