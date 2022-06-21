from django.contrib import admin
from .models import file,Letter,Direction,ScannedNum,Mode
# Register your models here.
admin.site.register(file)
admin.site.register(Letter)
admin.site.register(Direction)
admin.site.register(ScannedNum)
admin.site.register(Mode)