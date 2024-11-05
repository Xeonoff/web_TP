from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def question(request, pk):
    return render(request, 'question.html')

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')