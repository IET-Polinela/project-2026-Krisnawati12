from django.http import HttpResponse

def welcome_view(request):
    return HttpResponse("<h1>Selamat Datang</h1>")