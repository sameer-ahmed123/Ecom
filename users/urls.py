from django.urls import path
from users.views import View_profile

urlpatterns = [
    path("profile/", View_profile, name="profile"),
]
