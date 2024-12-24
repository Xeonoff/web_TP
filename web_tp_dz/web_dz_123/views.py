from django.shortcuts import render, redirect, get_object_or_404
from web_dz_123.models import *
from django.http import  HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib import auth
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from web_dz_123.forms import LoginForm, RegisterForm, SettingsForm, AskForm, AnswerForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse, resolve, Resolver404
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
import json
from json import JSONDecodeError

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
    page_obj = paginate(request, Question.objects.get_new())
    pop_tags = Tag.objects.get_popular()
    b_mem = Profile.objects.best_members()
    return render(request, "index.html", {"questions": page_obj, "popular_tags" : pop_tags, "best_members" : b_mem})

@require_http_methods(['GET', 'POST'])
def question(request, pk):
    pop_tags = Tag.objects.get_popular()
    b_mem = Profile.objects.best_members()
    item = Question.objects.get_one_question(pk)
    if request.method == 'GET':
        answer_form = AnswerForm()
        print("I`m here")
    if request.method == 'POST':
        print("I`m here")
        if request.user.is_authenticated:
            answer_form = AnswerForm(data = request.POST, author=Profile.objects.get(user=request.user), question=item)
            if answer_form.is_valid():
                new_answer = answer_form.save()
                if new_answer:
                    answers = Answer.objects.all().filter(question=pk)
                    pos = 0
                    for answer in answers:
                        pos += 1
                        if (answer == new_answer):
                            break
                    return redirect(reverse('question', kwargs={'pk':pk}) + '?page=' + str(pos // 5 + 1))
        else:
            return redirect(reverse('login'))
    page_obj = paginate(request, Answer.objects.by_question(pk))
    return render(request, "question.html", {"question": item, "answers": page_obj, "form":answer_form, "popular_tags" : pop_tags, "best_members" : b_mem})

@login_required(login_url='login')
def ask(request):
    pop_tags = Tag.objects.get_popular()
    b_mem = Profile.objects.best_members()
    if request.method == 'GET':
        ask_form = AskForm()
        print("I`m here")
    if request.method == 'POST':
        print("I`m here")
        ask_form = AskForm(data = request.POST, author=Profile.objects.get(user=request.user))
        if ask_form.is_valid():
            question = ask_form.save()
            return redirect(reverse('question', kwargs={'pk':question.id}))
    return render(request, "ask.html", {'form' : ask_form, "popular_tags" : pop_tags, "best_members" : b_mem})


@require_http_methods(['GET', 'POST'])
def login(request):
    pop_tags = Tag.objects.get_popular()
    b_mem = Profile.objects.best_members()
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
    pop_tags = Tag.objects.get_popular()
    b_mem = Profile.objects.best_members()
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
    page_obj = paginate(request, Question.objects.get_hot())
    pop_tags = Tag.objects.get_popular()
    b_mem = Profile.objects.best_members()
    return render(request, "hot.html", {"questions": page_obj, "popular_tags" : pop_tags, "best_members" : b_mem})

def tag(request, name):
    page_obj = paginate(request, Question.objects.by_tag(name))
    pop_tags = Tag.objects.get_popular()
    b_mem = Profile.objects.best_members()
    return render(request, "tag.html", {"questions": page_obj, "tag": name, "popular_tags" : pop_tags, "best_members" : b_mem})

@login_required(login_url='login')
def settings(request):
    pop_tags = Tag.objects.get_popular()
    b_mem = Profile.objects.best_members()
    if request.method == 'GET':
        settings_form = SettingsForm(user=request.user, avatar=Profile.objects.get(user=request.user).avatar)
    if request.method == 'POST':
        settings_form = SettingsForm(user=request.user, data=request.POST, files=request.FILES)
        if settings_form.is_valid():
            user = settings_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('settings'))
            
    return render(request, "settings.html", {'form':settings_form, 'user':request.user, "popular_tags" : pop_tags, "best_members" : b_mem})

def member(request, member_name):
    profile = Profile.objects.get_one_member(member_name)
    pop_tags = Tag.objects.get_popular()
    b_mem = Profile.objects.best_members()
    return render(request, "member.html", {"member": profile, "popular_tags" : pop_tags, "best_members" : b_mem})

@csrf_protect
@require_http_methods(['POST'])
def like_question(request):
    try:
        body = json.loads(request.body)
        question = get_object_or_404(Question, pk=body['questionId'])
        profile = get_object_or_404(Profile, user=request.user)
    except JSONDecodeError:
        return JsonResponse('Bad JSON', status=500)
    
    if body['isLike']:
        like_status = 1
    else:
        like_status = -1
    is_liked_already = LikeQuestion.objects.filter(question=question, user=profile)
    print(like_status)
    if is_liked_already.exists():
        if is_liked_already.first().status == like_status:
            question.rating -= like_status
            is_liked_already.first().delete()
        else:
            question.rating += like_status * 2
            is_liked_already.first().delete()
            LikeQuestion.objects.create(question=question, user=profile, status=like_status)
    else:
        question.rating += like_status
        LikeQuestion.objects.create(question=question, user=profile, status=like_status)

    question.save()
    return JsonResponse({
        'rating': question.rating
    })

@csrf_protect
@require_http_methods(['POST'])
def like_answer(request):
    try:
        body = json.loads(request.body)
        answer = get_object_or_404(Answer, pk=body['answerId'])
        profile = get_object_or_404(Profile, user=request.user)
    except JSONDecodeError:
        return JsonResponse('Bad JSON', status=500)
    
    if body['isLike']:
        like_status = 1
    else:
        like_status = -1
    is_liked_already = LikeAnswer.objects.filter(answer=answer, user=profile)
    print(like_status)
    if is_liked_already.exists():
        if is_liked_already.first().status == like_status:
            answer.rating -= like_status
            is_liked_already.first().delete()
        else:
            answer.rating += like_status * 2
            is_liked_already.first().delete()
            LikeAnswer.objects.create(answer=answer, user=profile, status=like_status)
    else:
        answer.rating += like_status
        LikeAnswer.objects.create(answer=answer, user=profile, status=like_status)

    answer.save()
    return JsonResponse({
        'rating': answer.rating
    })

@csrf_protect
@require_POST
def mark_answer(request):
    try:
        body = json.loads(request.body)
        answer = get_object_or_404(Answer, pk=body['answerId'])
        question = get_object_or_404(Question, pk=body['questionId'])
        is_correct = body['isCorrect']
    except KeyError or JSONDecodeError:
        return JsonResponse('Bad JSON', status=500)

    if question.author.id != request.user.user_profile.id:
        return HttpResponseBadRequest('Only author of the question is able to mark answer as correct')

    if is_correct:
        answer.status = 'm'
    else:
        answer.status = 'mn'
    answer.save()
    return JsonResponse('Marked', status=200)