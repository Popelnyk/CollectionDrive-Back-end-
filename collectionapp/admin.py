from django.contrib import admin

# Register your models here.
from collectionapp.models import Collection, Item

admin.site.register(Collection)
admin.site.register(Item)