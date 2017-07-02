from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ask.models import Profile, Question, Tag, Answer
from django.core.files import File
from django import forms
import urllib

class LoginForm(forms.Form):
    login = forms.CharField(
            widget=forms.TextInput(
                attrs={ 'class': 'form-control col-md-12 col-xs-12 inp-radius', 'placeholder': 'login', }
                ),
            max_length=30,
            label=u'Login'
            )

    password = forms.CharField(
            widget=forms.PasswordInput(
                attrs={ 'class': 'form-control col-md-12 col-xs-12 inp-radius', 'type': 'password', 'placeholder': 'password'}),
            label=u'Password'
            )

    def clean(self):
        data = self.cleaned_data
        print("!")
        user = authenticate(username=data.get('login', ''), password=data.get('password', ''))
        print(user)
        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError(u'This user don\'t active')
        else:
            raise forms.ValidationError(u'Uncorrect login or password')

class SignupForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Login', }),
            label=u'Login'
            )
    first_name = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'John', }),
            label=u'First name'
            )
    last_name = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Smith', }),
            label=u'Last name'
            )
    email = forms.EmailField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'type': 'email', 'placeholder': u'example@email.com', }),
            required = True, label=u'E-mail'
            )
    password1 = forms.CharField(
            widget=forms.PasswordInput( attrs={ 'class': 'form-control', 'type': 'password', 'placeholder': u'*****' }),
            min_length=6, label=u'Password'
            )
    password2 = forms.CharField(
            widget=forms.PasswordInput( attrs={ 'class': 'form-control', 'type': 'password', 'placeholder': u'*****' }),
            min_length=6, label=u'Repeat password'
            )
    info = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': u'About you :)', }),
            required=False, label=u'About'
            )
    avatar = forms.FileField(
            widget=forms.ClearableFileInput( attrs={ 'value': 'no-avatar.png', 'class': 'form-control upload-img', 'type': 'file', 'style' : 'display: none;',}),
            required=False, label=u'Avatar',
            )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError(u'User exist')
        except User.DoesNotExist:
            return username

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1', '')
        pass2 = self.cleaned_data.get('password2', '')

        if pass1 != pass2:
            raise forms.ValidationError(u'Passwords not equal')

    def save(self):
        data = self.cleaned_data
        password = data.get('password1')
        u = User()

        u.username = data.get('username')
        u.password = make_password(password)
        u.email = data.get('email')
        u.first_name = data.get('first_name')
        u.last_name = data.get('last_name')
        u.is_active = True
        u.is_superuser = False
        u.save()

        up = Profile()
        up.user = u
        up.info = data.get('info')
        if data.get('avatar') == None:
            up.avatar = "no-avatar.png"
        else:
            up.avatar = data.get('avatar')
        print(up.avatar)
        up.save()
        return authenticate(username=u.username, password=password)

class SettingsForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control inp-radius', 'placeholder': 'Login', }),
            max_length=30, label=u'Login'
            )
    email = forms.EmailField(
            widget=forms.TextInput( attrs={ 'class': 'form-control inp-radius', 'type': 'email', 'placeholder': 'ivanov@gmail.com', }),
            max_length=254, label=u'E-mail'
            )
    avatar = forms.FileField(
            widget=forms.ClearableFileInput( attrs={ 'class': 'ask-signup-avatar-input', 'style' : 'display: none;',}),
            required=False, label=u'Avatar'
            )

    def __init__(self, user, avatar, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.user = user
        self.avatar = avatar
        self.fields['username'].initial = self.user.username
        self.fields['email'].initial = self.user.email
        self.path_avatar = self.avatar

    def clean_username(self):
        username = self.cleaned_data.get('username')
        print(username)
        if username == self.user.username:
            return username
        try:
            u=User.objects.get(username=username)
            print(u)
            raise forms.ValidationError(u'User with this name exist')
        except User.DoesNotExist:
            return username

    def save(self, user):
        data = self.cleaned_data
        username = data.get('username')
        user.username = username
        user.email = data.get('email')
        user.save()

        up = Profile.objects.get(user_id=user.id)
        if data.get('avatar') != None:
            up.avatar = data.get('avatar')
        print("!")
        print(data.get('avatar'))
        print("!")
        up.save()

        return authenticate(username=user.username, password=user.password)




class NewQuestionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Title'}),
        required=True, max_length=40, label=u'Title'
        )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Input your question'}),
        required=True,  label=u'Question'
        )

    tags=forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input tags: tag1, tag2,...'}),
        required=True, max_length=100, label=u'Tags'
        )

    def clean_tags(self):
        tags_list = self.cleaned_data.get('tags', '').split(',')
        if tags_list:
            for sym in ['\\', ']', '[', '%']:
                for tag in tags_list:
                    if tag.find(sym) != -1:
                        raise forms.ValidationError(u'Error symbol in tag')
        return tags_list

    def save(self, owner):
        data = self.cleaned_data
        title = data.get('title')
        text = data.get('text')
        tags_list = data.get('tags')
        if tags_list:
            tags_list = [tag.replace(' ', '') for tag in tags_list]
            tags_list = [tag.replace('-', '_') for tag in tags_list]

        q = Question()
        q.title = title
        q.text = text
        q.owner = Profile.objects.get(user_id=owner.id)
        q.save()

        for tag in tags_list:
            tag_obj = Tag.objects.get_or_create(tag)
            q.tags.add(tag_obj)

        return q

class AnswerForm(forms.Form):
    textarea = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your answer', 'rows': '5'}),
        required=True
        )

    def save(self, request, question):
        owner = Profile.objects.get(user_id=request.user.id)
        answer = Answer.objects.create(owner=owner, question=question, text=self.cleaned_data.get('textarea'))
        page = Answer.objects.get_page(answer.id, 6)
        return answer, page
