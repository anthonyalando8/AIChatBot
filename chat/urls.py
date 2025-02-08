from django.urls import path
from . import views

app_name = "chatbot"

urlpatterns = [
    path('', views.index_view, name='index'),
    path("chat/", view=views.chat_view, name="chat"),
    path("signup/", view=views.signup_view, name="signup"),
    path("login/", view=views.login_view, name="login"),
]