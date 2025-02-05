from django.urls import path
from . import views

app_name = "chatbot"

urlpatterns = [
    path('', views.index_view, name='index'),
    path("chat/", view=views.index, name="chat")
]