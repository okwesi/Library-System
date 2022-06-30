from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm

from users.forms import PasswordChangeForms, SignUpForm
from .models import User

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone',   "is_active")
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email',  'password')}),
        ('Personal info', {'fields': ( 'phone', )}),
        # ('Groups', {'fields': ()}),
        ('Permissions', {'fields': ('is_staff', 'is_admin','is_superuser','is_active', 'groups')}),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    
    readonly_fields =  ('date_joined', 'last_login')

    search_fields = ('email', 'phone')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)