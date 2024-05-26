from django.contrib import admin
from .models import (EntryModel, LibraryModel, LibraryDetailModel)

# Register your models here.
admin.site.register(EntryModel)
admin.site.register(LibraryModel)
admin.site.register(LibraryDetailModel)