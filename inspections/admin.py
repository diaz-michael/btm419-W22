from django.contrib import admin

# Register your models here.
from .models import warranty, claim, inspection

admin.site.register(warranty)
admin.site.register(claim)
admin.site.register(inspection)