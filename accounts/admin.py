from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserChangeForm, MyUserCreationForm
from .models import CustomUser, LoginEvent

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = CustomUser


    list_display = ['email', 'full_name', 'university', 'number', 'last_login']

    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'year', 'university', 'number', 'university_society',
                           'university_society_position', 'streak')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'full_name', 'year', 'university', 'number', 'university_society',
                           'university_society_position', 'streak')}),
    )
    ordering = ['email', 'full_name', 'university', 'number', 'last_login']

admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(LoginEvent)