"""AskZaytsev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from ask import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^helloworld', views.helloworld),
    url(r'^index/(?P<page>\w+)/', views.index, name='new-questions'),
    url(r'^index/', views.index, name='def-new-questions'),
    url(r'^hot/(?P<page>\w+)/', views.hot, name='hot-questions'),
    url(r'^hot', views.hot, name='def-hot-questions'),
    url(r'^tag/(?P<tagname>\w+)/(?P<page>\w+)/', views.tag, name='tag'),
    url(r'^tag/(?P<tagname>\w+)/', views.tag, name='tag'),
    url(r'^question/(?P<qid>\w+)/(?P<page>\w+)/', views.question, name='questions'),
    url(r'^question/(?P<qid>\w+)/', views.question, name='questions'),
    url(r'^login', views.login, name="login"),
    url(r'^logout', views.logout, name="logout"),
    url(r'^signup', views.signup, name="signup"),
    url(r'^like$', views.like, name='like'),
    url(r'^correct$', views.correct, name='correct'),
    url(r'^ask', views.ask, name='ask'),
    url(r'^settings', views.settings, name='settings'),
    url(r'^$', views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)