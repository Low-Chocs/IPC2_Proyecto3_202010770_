from django.shortcuts import render
import requests

# Create your views here.
def home(request):
    try:
        response = requests.get('http://127.0.0.1:4000')
        return render(request, 'index.html')
    except:
        print('La api no esta activa')

    