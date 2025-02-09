from django.shortcuts import render
from users.models import Profile


# Create your views here.
# create login logout and register views

def View_profile(request):
    image = Profile.objects.get(user=request.user)
    return render(request, "profile.html", {"img": image})
