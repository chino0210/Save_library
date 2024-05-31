from django.urls import path
from .views import (

  EntryView,
  EntryCreateView,
  EntrysUpdateView,
  EntryDeleteView,
  EntrysUploadDocumentView,
  EntryFilterID,

  LibraryView,
  LibraryCreateView,
  LibraryUpdateView,
  LibraryFilter,
  LibraryDeleteView,

  RegisterView,
  LoginView,
  usersView,
)

urlpatterns = [
  path ('entrys/all', EntryView.as_view()),
  path ('entrys/create', EntryCreateView.as_view()),
  path ('entrys/filter/<int:pk>', EntryFilterID.as_view()),
  path ('entrys/update/<int:pk>', EntrysUpdateView.as_view()),
  path ('entrys/delete/<int:pk>', EntryDeleteView.as_view()),
  path ('entrys/upload-document', EntrysUploadDocumentView.as_view()),
  path ('library/all', LibraryView.as_view()),
  path ('library/create', LibraryCreateView.as_view()),
  path ('library/filter/<int:pk>', LibraryFilter.as_view()),
  path ('library/update/<int:pk>', LibraryUpdateView.as_view()),
  path ('library/delete/<int:pk>', LibraryDeleteView.as_view()),
  path ('user/register', RegisterView.as_view()),
  path ('user/login', LoginView.as_view()),
  path ('user/all', usersView.as_view())
]
