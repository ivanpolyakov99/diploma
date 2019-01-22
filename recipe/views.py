from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("Hello world it's Conway's Game of Life")