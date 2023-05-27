from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Docs)
admin.site.register(Comment)
admin.site.register(RoomMember)