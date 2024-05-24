from rest_framework import generics, status
from .serializers import (
  UserCreateSerializer,
  EntryModel,
  EntrySerializer,
  EntryUpdateSeliarizer,
  LibraryModel,
  LibraryDetailModel,
  LibrarySerializer,
  LibraryCreateSerializer,
  LibraryUpdateSerializer,
  TagsModel,
  TagsDetailModel,
  TagsSerializer,
  TagsCreateSerializer,
  MyTokenObtainPairSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from cloudinary.uploader import upload
from pprint import pprint
from django.contrib.auth.models import User
from django.db import transaction
from .models import MyUser

# UsersViews
class RegisterView (generics.CreateAPIView):
  queryset = MyUser.objects.all()
  serializer_class = UserCreateSerializer

  def post(self, request, *args, **kwargs):
    try:
      email = request.data.get('email')
      user = MyUser.objects.filter(email=email).first()

      if user:
        raise Exception('El usuario ya existe')

      serializer = self.serializer_class(data=request.data)
      serializer.is_valid(raise_exception=True)
      newUser = serializer.save()
      response = self.serializer_class(newUser).data

      return Response(response, status=status.HTTP_201_CREATED)
    except Exception as e:
      return Response({
        'errors': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer

# EntrysViews
class EntryView(generics.ListAPIView):
  queryset = EntryModel.objects.all()
  serializer_class = EntrySerializer

class EntryCreateView(generics.CreateAPIView):
  queryset = EntryModel.objects.all()
  serializer_class = EntrySerializer

class EntrysUpdateView(generics.UpdateAPIView):
  queryset = EntryModel.objects.all()
  serializer_class = EntryUpdateSeliarizer

class EntryDeleteView(generics.DestroyAPIView):
  queryset = EntryModel.objects.all()
  serializer_class = EntrySerializer

  def destroy(self, request, *args, **kwargs):
    try:
      instance = self.get_object()
      instance.status = False
      instance.save()

      return Response({
        'message': 'Producto eliminado correctamente'
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response ({
        'errors': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EntrysUploadDocumentView (generics.GenericAPIView):
  serializer_class = EntrySerializer

  def post(self, request, *args, **kwargs):
    try:
      # obtencion del archivo
      document_file = request.FILES.get('documento')
      if not document_file:
        raise Exception('No se ha enviado ningun documento')

      #subir el doc a cloudinary
      uploadedDocument = upload (document_file)
      documentName = uploadedDocument ['secure_url'].split('/')[-1]
      documentPath = f'{uploadedDocument["resource_type"]}/{uploadedDocument["type"]}/v{uploadedDocument["version"]}/{uploadedDocument["type"]}/{documentName}'

      # Retornar la URL de la imagen
      return Response({
        'url': documentPath
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response ({
        'errors': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LibraryView(generics.ListAPIView):
  queryset = LibraryModel.objects.all()
  serializer_class = LibrarySerializer

class LibraryCreateView(generics.CreateAPIView):
  queryset = LibraryModel.objects.all()
  serializer_class = LibraryCreateSerializer

  @transaction.atomic
  def create(self, request, *args, **kwargs):
    try:
      # Recuperar la data
      data = request.data

      # Se valida el JSON q se envia
      serializer = self.serializer_class(data=data)
      serializer.is_valid(raise_exception=True)

      user = MyUser.objects.get(id=data['user_id'])

      # Se   guarda la libreria
      library = LibraryModel.objects.create(
        user_id = user,
        total = data['total'],
      )
      library.save()

      # Sumar +1 al total de veces guardado
      for item in data['details']:
        entryID = item['entry_id']
        entryStatus = item['status_saved']

        entry = EntryModel.objects.get(id=entryID)
        if entryStatus == True:
          entry.times_saved += 1
        entry.save()

        # Guardamos el detalle de la libreria
        libraryDetail = LibraryDetailModel.objects.create(
          entry_id = entry,
          status_saved = entryStatus,
          library_id = library,
        )
        libraryDetail.save()

      return Response({
        'message': 'Libreria guardada correctamente'
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response({
        'errors': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LibraryUpdateView(generics.UpdateAPIView):
  queryset = LibraryModel.objects.all()
  serializer_class = LibrarySerializer

  # def update(self, request, *args, **kwargs):
  #   try:
  #     data = request.data
  #     # {'details': [{'status_saved': False, 'entry_id': 1, 'library_id': 7}], 'total': 3, 'user_id': 1}
  #     serializer = self.serializer_class(data=data)
  #     serializer.is_valid(raise_exception=True)
  #     # print(data)

  #     # user = MyUser.objects.get(id=data['user_id'])

  #     libraryID = data['id']

  #     library = LibraryModel.objects.get(id=libraryID)
  #     print(library)

  #     library = LibraryModel.objects.update(
  #       total = data['total'],
  #       user_id = user
  #     )

  #     library = LibraryModel.objects.get(pk=entryID)
  #     print(library)

  #     for item in data ['details']:
  #       entryID = item['entry_id']
  #       entryStatus = item['status_saved']

  #       entry = EntryModel.objects.get(id=entryID)
  #       # if entryStatus == False:
  #       #   entry.times_saved -= 1
  #       # if entryStatus == True:
  #       #   entry.times_saved += 1
  #       # # entry.save()
  #       # libraryDetail = LibraryDetailModel.objects.filter(pk=obj.pk)
  #       libraryDetail = LibraryDetailModel.objects.update(
  #         entry_id = entry,
  #         status_saved = entryStatus,
  #       )

  #     return Response({
  #       'message': 'Library actualizada correctamente'
  #     }, status=status.HTTP_200_OK)
  #   except Exception as e:
  #     return Response ({
  #       'errors': str(e)
  #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LibraryDeleteView(generics.DestroyAPIView):
  queryset = LibraryModel.objects.all()
  serializer_class = LibrarySerializer

class TagsView (generics.ListAPIView):
  queryset = TagsModel.objects.all()
  serializer_class = TagsSerializer

class TagsCreateView(generics.CreateAPIView):
  queryset = TagsModel.objects.all()
  serializer_class = TagsCreateSerializer

  @transaction.atomic
  def create(self, request, *args, **kwargs):
    try:
      data = request.data
      print(data)

      serializer = self.serializer_class(data=data)
      serializer.is_valid(raise_exception=True)

      # entryID = EntryModel.objects.get(id=data['entry_id'])

      # Se guarda el tag
      tag = TagsModel.objects.create(
        # name = data['tag_name'],
        # description = data['description']
        tag_name = data['tag_name'],
        description = data['description']
      )
      tag.save()

      for item in data['details']:
        tagStatus = item['status_tag']
        entryID = item['entry_id']

        entry = EntryModel.objects.get(id=entryID)

        tagDetail = TagsDetailModel.objects.create(
          status_tag = tagStatus,
          entry_id = entry,
          tag_id = tag,
        )
        tagDetail.save()

      return Response({
        'message': 'Tag creado correctamente'
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response({
        'errors': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TagsUpdateView(generics.UpdateAPIView):
  queryset = TagsModel.objects.all()
  serializer_class = TagsSerializer

class TagsDeleteView(generics.DestroyAPIView):
  queryset = TagsModel
  serializer_class = TagsSerializer