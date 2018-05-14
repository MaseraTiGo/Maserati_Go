from django.contrib import admin
from .models import Test
# Register your models here.
class LearnTest(admin.ModelAdmin):
    list_display = ['name', 'sex', 'age']
    search_fields = ['name']
    list_filter = ['sex']
admin.site.register(Test, LearnTest)