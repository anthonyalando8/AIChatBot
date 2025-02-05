from django.shortcuts import render
from . gemini_model import Model
from django.http import HttpResponse, JsonResponse
from .forms import CreateChatForm
from .gemini_model import Model
import random
import string
from django.core.cache import cache
from django.core.serializers import serialize

genai = Model()

def index_view(request):
    return render(request, 'chat/index.html', {})

def index(request):
    user = request.user
    image = None

    if request.method == "POST":
        if request.POST.get("send_prompt"):
            request_session_id = request.POST.get("session_id")
            request_chat_id = request.POST.get("request_chat_id")
            form = CreateChatForm(request.POST, request.FILES)
            if form.is_valid():
                message = form.cleaned_data['message']
                if 'image' in form.cleaned_data and form.cleaned_data['image']:
                    image = form.cleaned_data['image']
                    # process image prompt
                    
                else:
                    try:
                        model_response = genai.response_model("Anthony", message)
                        response = {
                            "message":"Success",
                            "prompt": message,
                            "response": model_response,
                            "status": 200
                        }
                        return JsonResponse(response, status=response["status"])
                    except KeyError as e:
                        response = {
                                "message": f"Error {e}",
                                "status": 500
                        }
                        return JsonResponse(response, status=response["status"])
    else:
        return redirect_page(request)


def generate_id(length=25):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_user_cache(user, key):
    return cache.get(f"{user.id}_{key}")

def redirect_page(request):
    form = CreateChatForm()

    cached_chat_id = get_user_cache(request.user, "previous_chat_id")
    session_id = str(request.session._get_or_create_session_key())
    context = {
        "user": request.user,
        "form": form,
        "default": {
            "chat_id": "new_chat",
            "session_id": session_id
        }
    }
    
    if cached_chat_id is not None:
        context["default"]["chat_id"] = cached_chat_id
               
    return HttpResponse(render(request, 'chat/chat.html', context))