from django.urls import path
from afip import views

urlpatterns = [
    path("status/", views.CheckStatusApi.as_view()),
    path("history/", views.ListCheckStatusApi.as_view()),
]
