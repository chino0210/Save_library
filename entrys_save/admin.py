from django.contrib import admin
from .models import (EntryModel, LibraryModel, LibraryDetailModel, TagsModel)

# Register your models here.
admin.site.register(EntryModel)
admin.site.register(TagsModel)
admin.site.register(LibraryModel)
admin.site.register(LibraryDetailModel)