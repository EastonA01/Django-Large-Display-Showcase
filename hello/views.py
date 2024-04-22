import re
import requests
from django.utils.timezone import datetime, now
from django.http import HttpResponse
from django.shortcuts import redirect, render
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page URL pattern
        else:
            # Authentication failed, show an error message
            return render(request, 'hello/login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'hello/login.html')

def register_user(request):
    # If we are registering data
    if request.method == 'POST':
        # Get all data needed for user db entry
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # Create User
        user = User.objects.create_user(f"{username}",f"{email}",f"{password}")
        # Return to login page
        return render(request, "hello/login.html", user=user)
    else:
        return render(request, "hello/register.html")

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")


def projects(request):
    # print(request.build_absolute_uri()) #optional
    return render(request, "hello/projects.html")

@login_required(login_url="/login/")
def log_message(request):
    form = LogMessageForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # Start to save message
            message = form.save(commit=False)
            # Check for profanity and filter out if any, then redirect to home
            if profanity_check(form.cleaned_data.get('message')) == False:
                # If no profanity, save the message to the database and return home
                print("Message Saved")
                message.log_date = datetime.now()
                message.save()
                return redirect("home")
            else:
                # Else filter the text and then save to db               
                message.message = text_filter(form.cleaned_data.get('message'))
                message.log_date = datetime.now()
                message.save()
                return redirect("home")
    else:
        return render(request, "hello/log_message.html", {"form": form})
    
def profanity_check(message):
    response = requests.get(f'https://www.purgomalum.com/service/containsprofanity?text={message}')
    if response.status_code == 200:
        data = response.json()  
        if data == True:
            text_filter(message)
        else:
            return False
    else:
        return HttpResponse("Error: Data Could Not Be Retrieved")
    
def text_filter(message):
    response2 = requests.get(f'https://www.purgomalum.com/service/plain?text={message}')
    if response2.status_code == 200:
        data2 = response2.text
        return data2