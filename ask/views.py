import random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import *
from ask.models import Question, Profile, Answer, LikeToQuestion, LikeToAnswer, Tag
from ask.forms import LoginForm, SignupForm, SettingsForm, NewQuestionForm, AnswerForm
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
import simplejson as json
from django.db import connection

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

def paginate(blocks, blocks_on_page, cur_page):
    paginator = Paginator(blocks, blocks_on_page)
    try:
        current_page = int(cur_page)
    except ValueError:
        current_page = 1

    if (current_page > paginator.num_pages):
        current_page = paginator.num_pages

    first_index = 0 if (paginator.num_pages <= 5 or current_page <= 3) else current_page - 3
    last_index = paginator.num_pages if (paginator.num_pages <= 5 or paginator.num_pages - 2 <= current_page) else current_page + 2
    page_range = paginator.page_range[first_index:last_index]
    #print(page_range)
    return paginator.page(current_page), page_range

def index(request, page=1):
    questionObjs = Question.objects.list_ordered_date()
    questions, page_range = paginate(questionObjs, 4, page)
    context = {
        "questions" : questions,
        "page_range" : page_range,
        "pag_url": 'new-questions',
    }
    print(connection.queries)
    return render(request, 'newquestionslist.html', context)

def hot(request, page=1):
    questionObjs = Question.objects.list_hot()
    questions, page_range = paginate(questionObjs, 4, page)
    print(page)
    context = {
        "questions" : questions,
        "page_range" : page_range,
        "pag_url": 'hot-questions',
    }
    print(connection.queries)
    return render(request, 'newquestionslist.html', context)

def tag(request, tagname, page=1):
    try:
        tag = Tag.objects.get_by_title(tagname)
    except Tag.DoesNotExist:
        raise Http404()
    questionsObjs = Question.objects.list_tag(tag)

    questions, page_range = paginate(questionsObjs, 4, page)
    context = {
        "questions" : questions,
        "page_range" : page_range,
        "pag_url": 'tag',
        "tag": tag,
    }
    print(connection.queries)
    return render(request, 'tag.html', context)

def question(request, qid, page=1):
    try:
        q = Question.objects.get_single(int(qid))
        answersObjs = Answer.objects.by_id(q.id)
        answers, page_range = paginate(answersObjs, 4, page)
        if request.method == "POST":
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer, page = form.save(request, q)
                print(connection.queries)
                return HttpResponseRedirect('/question/' + str(q.id) + '/' + str(page))
        else:
            form = AnswerForm()
    except Question.DoesNotExist:
        raise Http404()
    context = {
        "question" : q,
        "answers" : answers,
        "page_range" : page_range,
        "pag_url": 'questions',
        "form": form,
    }
    print(connection.queries)
    return render(request, 'question.html', context)

def settings(request):
    profile = Profile.objects.get(user_id=request.user.id)
    avatar = profile.avatar
    if request.method == "POST":
        form = SettingsForm(request.user, avatar, request.POST, request.FILES)
        if form.is_valid():
            user = form.save(request.user)
            auth.login(request, user)
            request.session['img'] = Profile.objects.filter(user_id=request.user.id)[0].get_avatar()
            print(connection.queries)
            return HttpResponseRedirect('/settings')
    else:
        request.session['img'] = None
        form = SettingsForm(request.user, avatar)
    context = {"form": form}
    print(connection.queries)
    return render(request, 'settings.html', context)

def login(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated():
        request.session['img'] = Profile.objects.filter(user_id=request.user.id)[0].get_avatar()
        print(connection.queries)
        return HttpResponseRedirect(redirect)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            request.session['img'] = Profile.objects.filter(user_id=request.user.id)[0].get_avatar()
            print(connection.queries)
            return HttpResponseRedirect(redirect)
    else:
        #request.img = None
        form = LoginForm()
    context = {"form": form}
    print(connection.queries)
    return render(request, 'login.html', context)

@login_required(redirect_field_name='continue')
def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    print(connection.queries)
    return HttpResponseRedirect(redirect)

def signup(request):
    if request.user.is_authenticated():
        request.session['img'] = Profile.objects.filter(user_id=request.user.id)[0].get_avatar()
        print(connection.queries)
        return HttpResponseRedirect('/')

    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            request.session['img'] = Profile.objects.filter(user_id=request.user.id)[0].get_avatar()
            print(connection.queries)
            return HttpResponseRedirect('/')
    else:
        request.session['img'] = None
        form = SignupForm()
    context = {"form": form}
    print(connection.queries)
    return render(request, 'signup.html', context)

@login_required()
def ask(request):
    if request.method == "POST":
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(request.user)
            print(connection.queries)
            return HttpResponseRedirect('/question/' + str(question.id) + '/')
    else:
        request.session['img'] = None
        form = NewQuestionForm()
    context = {"form": form}
    print(connection.queries)
    return render(request, 'ask.html', context)

@login_required()
def like(request):
    body = request.body.decode("utf-8")
    request.POST = json.loads(body)
    if request.POST['type'] == 'que':
        q = Question.objects.get(id=request.POST['qid'])
        p = Profile.objects.get(user_id=request.user.id)
        value = 1 if request.POST['type_like'] == 'like_question' else -1
        LikeToQuestion.objects.add_or_update(owner=p, question=q, value=value)
        print(connection.queries)
        return HttpResponse(
            json.dumps({"qid": request.POST['qid'], 'like': value}),
            content_type="application/json"
            )
    else:
        if request.POST['type'] == 'ans':
            a = Answer.objects.get(id=request.POST['aid'])
            p = Profile.objects.get(user_id=request.user.id)
            value = 1 if request.POST['type_like'] == 'like_answer' else -1
            LikeToAnswer.objects.add_or_update(owner=p, answer=a, value=value)
            print(connection.queries)
            return HttpResponse(
                json.dumps({"aid": request.POST['aid'], 'like': value}),
                content_type="application/json"
            )

@login_required()
def correct(request):
    body = request.body.decode("utf-8")
    request.POST = json.loads(body)
    a = Answer.objects.get(id=request.POST.get('aid', False))
    is_correct = request.POST.get('checked', False)
    #print(is_correct)
    a.correct = is_correct
    a.save()
    print(connection.queries)
    return HttpResponse(
        json.dumps({"aid": request.POST['aid'], 'correct': is_correct}),
        content_type="application/json"
    )
