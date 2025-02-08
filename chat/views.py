from django.shortcuts import render
from . gemini_model import Model
from django.http import HttpResponse, JsonResponse
from .forms import CreateChatForm
from .gemini_model import Model
import random
import string
from django.core.cache import cache
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

genai = Model()

def index_view(request):
    return render(request, 'chat/index.html', {})

def chat_view(request):
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
                        username = request_session_id
                        user = request.user
                        if user.is_authenticated:
                            username = user.username
                        model_response = genai.response_model(username, message)
                        response = {
                            "message":"Success",
                            "prompt": message,
                            "response": model_response,
                            "status": 200
                        }
                        return JsonResponse(response, status=response["status"])
                    except KeyError as e:
                        print(f"Error: {e}")
                        response = {
                                "message": f"Error {e}",
                                "status": 500
                        }
                        return JsonResponse(response, status=response["status"])
    else:
        return redirect_page(request)
    
# Create account view
def signup_view(request):
    if request.method == "GET":
        return render(request, 'chat/signup.html', {})

    elif request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if all([username, password, first_name, last_name]):
            # Check if the email is already registered
            if User.objects.filter(username=username).exists():
                return JsonResponse({"message": "User already exists"}, status=400)

            # Create the user
            user = User.objects.create_user(
                username=username, email=username, password=password, first_name=first_name, last_name=last_name
            )
            user.save()

            return JsonResponse({"message": "User created"}, status=201)

        else:
            return JsonResponse({"message": "All fields are required"}, status=400)

    else:
        return HttpResponse("Method not allowed", status=405)
# login view

def login_view(request):
    if request.method == "GET":
        return render(request, 'chat/login.html', {})
    elif request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        if all in [username, password]:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response = {
                    "message": "User logged in successfully",
                    "status": 200
                }
                return JsonResponse(response, status=response["status"])
            else:
                response = {
                    "message": "Invalid credentials",
                    "status": 401
                }
                return JsonResponse(response, status=response["status"])
        else:
            response = {
                "message": "All fields are required",
                "status": 400
            }
            return JsonResponse(response, status=response["status"])
    else:
        return HttpResponse("Method not allowed", status=405)

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