import re
import requests
from django.utils.timezone import datetime, now
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.views.generic import ListView

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")

def hello_there(request, name):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

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