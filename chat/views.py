# chat/views.py
from django.shortcuts import render


# Vista del index
def index(request):
    return render(request, 'chat/index.html')