from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.auth import authenticate, login, get_user_model
from django.core.serializers import serialize
from .gemini_model import Model
from .forms import CreateChatForm
import json
import random
import string

# Initialize AI model
genai = Model()

# Get user model
User = get_user_model()

# ✅ Index page view
def index_view(request):
    return render(request, 'chat/index.html', {})

# ✅ Chat page view
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

# ✅ Signup view
def signup_view(request):
    if request.method == "GET":
        return render(request, 'chat/signup.html')

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            first_name = data.get("first_name")
            last_name = data.get("last_name")

            if not all([email, password, first_name, last_name]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "User already exists"}, status=400)

            user = User.objects.create_user(email=email, username=email, password=password,
                                            first_name=first_name, last_name=last_name)

            return JsonResponse({"message": "User created successfully!"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

# ✅ Login view
def login_view(request):
    if request.method == "GET":
        return render(request, 'chat/login.html')

    elif request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        if all([username, password]):  # ✅ Corrected syntax
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "User logged in successfully", "status": 200}, status=200)
            else:
                return JsonResponse({"message": "Invalid credentials", "status": 401}, status=401)
        else:
            return JsonResponse({"message": "All fields are required", "status": 400}, status=400)

    return HttpResponse("Method not allowed", status=405)

# ✅ About page view
def about_view(request):
    return render(request, 'chat/about.html', {})

# ✅ Utility function to generate a random session ID
def generate_id(length=25):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# ✅ Function to get cached user data
def get_user_cache(user, key):
    return cache.get(f"{user.id}_{key}")

# ✅ Redirect function for chat
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
