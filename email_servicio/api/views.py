from django.shortcuts import render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def contact(request):
    if request.method == "POST":
        name= request.POST["name"]
        email= request.POST["email"]
        subject= request.POST["subject"]
        message= request.POST["message"]