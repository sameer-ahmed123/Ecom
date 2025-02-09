from django.shortcuts import render

# Create your views here.


def View_profile(request):
    return render(request, "profile.html")
