from django.contrib import admin
from .models import *

# Register your models here.
# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    search_fields = ('full_name', 'outcome_target', 'user')
    list_display = ('full_name', 'outcome_target', 'user')


admin.site.register(Client, ClientAdmin)