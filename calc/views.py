from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def calculator(request):
    return render(request, "calc.html")