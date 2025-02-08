from django.urls import path
from chat.views import index_view, chat_view, signup_view, login_view, about_view  # ✅ Import from chat

app_name = 'chatbot'

urlpatterns = [
    path('', index_view, name='index'),
    path('chat/', chat_view, name='chat'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('about/', about_view, name='about'),
]
