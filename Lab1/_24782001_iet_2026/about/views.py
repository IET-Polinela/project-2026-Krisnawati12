from django.shortcuts import render

# Pastikan nama fungsinya 'about_view' (pakai underscore)
def about_view(request):
    return render(request, 'about/about.html')