from django.conf.urls import patterns, include, url

from fontly.views import *

urlpatterns = patterns('',
    url(r'^$', Home.as_view()),
    url(r'^(?P<params>.*)$', Font.as_view()),
)
