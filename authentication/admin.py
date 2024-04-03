from django.contrib import admin
from .models import User,Student,Parent,Teacher,Orthophoniste
# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Orthophoniste)