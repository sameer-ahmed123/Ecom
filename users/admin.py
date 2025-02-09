from django.contrib import admin
from users.models import Profile

# Register your models here.


class UserProfile(admin.ModelAdmin):
    list_display = ["user", "location", "birth_date", "date_joined"]
    search_fields = ["user", "location", "birth_date"]
    list_filter = ["location", "date_joined"]


admin.site.register(Profile, UserProfile)
