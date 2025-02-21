from django.urls import path
from users.views import View_profile, Login_view, Logout_view, edit_profile, Register_view

urlpatterns = [
    path("profile/", View_profile, name="profile"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("login/", Login_view, name="login"),
    path("logout/", Logout_view, name="logout"),
    path("register/", Register_view, name="register"),
]
