from django.http import HttpResponse
from django.template import loader

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

def index(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render(request))

def hot(request):
    output = '200'
    return  HttpResponse(output)

def tag(request, tagname):
    output = '200'
    return  HttpResponse(output)

def question(request, qid):
    output = '200'
    return  HttpResponse(output)

def login(request):
    output = '200'
    return  HttpResponse(output)

def signup(request):
    output = '200'
    return  HttpResponse(output)

def ask(request):
    output = '200'
    return  HttpResponse(output)
