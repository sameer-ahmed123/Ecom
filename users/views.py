from django.shortcuts import get_object_or_404, render, redirect
from users.models import Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from users.forms import ProfileForm

# Create your views here.
# create login logout and register views


def View_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "profile.html", {"profile": profile})


def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileForm(
            instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form
    }
    return render(request, "edit_profile.html", context)


def Login_view(request):
    context = {
        "form": AuthenticationForm()
    }
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to profile view after login
                return redirect('profile')
            else:
                context["error"] = "Invalid username or password"
        else:
            context["error"] = "Form is invalid"
    return render(request, "login.html", context)


def Logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return render(request, "logout.html")


def Register_view(request):
    context = {
        "form": UserCreationForm()
    }
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
        else:
            context["error"] = "Form is invalid"
    return render(request, "register.html", context)
