from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('chat/', views.chat_view, name='chat'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about_view, name='about'),
    path('logout/', views.logout_view, name='logout'),
    
]