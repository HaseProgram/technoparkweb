import random
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from django.template import *

def helloworld(request):
    output = '<h2>Hello World!</h2>'
    if request.method == 'GET':
        if len(request.GET):
            output += '<b>GET request data</b>: <br>'
            for data in request.GET:
                output += data
                output += ' = '
                output += request.GET[data]
                output += '<br>'
    if request.method == 'POST':
        output += '<b>POST request data</b>: <br>'
        for data in request.POST:
            output += data
            output += ' = '
            output += request.POST[data]
            output += '<br>'
    return HttpResponse(output)

def paginate(blocks, blocks_on_page, current_page):
    paginator = Paginator(blocks, blocks_on_page)
    first_index = 0 if (paginator.num_pages <= 5 or int(current_page) <= 3) else int(current_page) - 3
    last_index = paginator.num_pages if (paginator.num_pages <= 5 or paginator.num_pages - 2 <= int(current_page)) else int(current_page) + 2
    page_range = paginator.page_range[first_index:last_index]
    print(page_range)
    return paginator.page(int(current_page)), page_range

def getquestions():
    questions = []
    for i in range(1, 100):
        questions.append({
            'title': 'How to build a moon park? (' + str(i) + ')',
            'id': i,
            'text': 'Guys, I have trouble with a moon park. <br> Can\'t find the black-jack...',
            'answers': random.randint(0, 30),
            'tags': {'blackjack', 'bender'},
        })
    return questions

def index(request, page=1):
    template = loader.get_template('newquestionslist.html')
    questions, page_range = paginate(getquestions(), 4, page)
    context = Context({
        "request" : request,
        "questions" : questions,
        "page_range" : page_range,
    })
    return HttpResponse(template.render(context))

def hot(request, page=1):
    template = loader.get_template('newquestionslist.html')
    questions, page_range = paginate(getquestions(), 4, page)
    context = Context({
        "request" : request,
        "questions" : questions,
        "page_range" : page_range,
    })
    return HttpResponse(template.render(context))

def tag(request, tagname, page=1):
    template = loader.get_template('tag.html')
    questions, page_range = paginate(getquestions(), 4, page)
    context = Context({
        "request" : request,
        "questions" : questions,
        "page_range" : page_range,
    })
    return HttpResponse(template.render(context))

def question(request, qid):
    q = {
    'title': 'How to build a moon park?',
    'id': 1,
    'text': 'Guys, I have trouble with a moon park. <br> Can\'t find the black-jack...',
    'answers': random.randint(0, 30),
    'tags': {'blackjack', 'bender'},
    }
    template = loader.get_template('question.html')
    context = Context({
    "request" : request,
    "question" : q,
    })
    return HttpResponse(template.render(context))

def settings(request):
    template = loader.get_template('settings.html')
    context = Context({"request" : request})
    return HttpResponse(template.render(context))

def login(request):
    template = loader.get_template('login.html')
    context = Context({"request" : request})
    return HttpResponse(template.render(context))

def signup(request):
    template = loader.get_template('signup.html')
    context = Context({"request" : request})
    return HttpResponse(template.render(context))

def ask(request):
    template = loader.get_template('ask.html')
    context = Context({"request" : request})
    return HttpResponse(template.render(context))
