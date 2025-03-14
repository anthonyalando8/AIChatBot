from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.serializers import serialize
from .gemini_model import Model
from .forms import CreateChatForm
import json
import random
import string

# Initialize AI model
genai = Model()

def index_view(request):
    return render(request, 'chat/index.html', {})

def chat_view(request):
    user = request.user
    image = None

    if request.method == "POST":
        if request.POST.get("send_prompt"):
            request_session_id = request.POST.get("session_id")
            form = CreateChatForm(request.POST, request.FILES)
            
            if form.is_valid():
                message = form.cleaned_data['message']

                if 'image' in form.cleaned_data and form.cleaned_data['image']:
                    image = form.cleaned_data['image']
                    # Process image input here if needed

                else:
                    try:
                        username = request_session_id
                        if user.is_authenticated:
                            username = user.username
                        model_response = genai.response_model(username, message)

                        response = {
                            "message": "Success",
                            "prompt": message,
                            "response": model_response,
                            "status": 200
                        }
                        return JsonResponse(response, status=200)

                    except KeyError as e:
                        return JsonResponse({"message": f"Error: {e}", "status": 500}, status=500)

    return redirect_page(request)

def signup_view(request):
    if request.method == "GET":
        return render(request, 'chat/signup.html')

    elif request.method == "POST":
        try:
            email = request.POST.get("email", None)
            password = request.POST.get("password", None)
            first_name = request.POST.get("first_name", None)
            last_name = request.POST.get("last_name", None)

            if not all([email, password, first_name, last_name]):
                return JsonResponse({"message": "All fields are required"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "User already exists"}, status=400)

            user = User.objects.create_user(
                email=email, 
                username=email, 
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            return JsonResponse({"message": "User created successfully!"}, status=201)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"message": "Something went wrong."}, status=400)

    return JsonResponse({"message": "Method not allowed"}, status=405)

def login_view(request):
    if request.method == "GET":
        return render(request, 'chat/login.html')

    elif request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        if all([username, password]): 
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "User logged in successfully", "status": 200}, status=200)
            else:
                return JsonResponse({"message": "Invalid credentials", "status": 401}, status=401)
        else:
            return JsonResponse({"message": "All fields are required", "status": 400}, status=400)

    return HttpResponse("Method not allowed", status=405)

def about_view(request):
    return render(request, 'chat/about.html', {})

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
               
    return render(request, 'chat/chat.html', context)
