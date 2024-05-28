from rest_framework import generics, status
from .serializers import (
  UserCreateSerializer,
  # Entry
  EntryModel,
  EntrySerializer,
  EntryUpdateSeliarizer,
  #Library
  LibraryModel,
  LibraryDetailModel,
  LibrarySerializer,
  LibraryDetailSerializer,
  LibraryCreateSerializer,
  LibraryUpdateSerializer,
  # Tags
  TagsModel,
  TagsDetailModel,
  TagsSerializer,
  TagsDetailSerializer,
  TagsCreateSerializer,
  TagsUpdateSerializer,
  # Token
  MyTokenObtainPairSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from cloudinary.uploader import upload
from pprint import pprint
from django.contrib.auth.models import User
from django.db import transaction
from .models import MyUser
from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import random

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
      uploadedDocument = upload (document_file, resource_type='raw')
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
      # print (data)
      # {'details': [{'status_saved': True, 'entry_id': 1}], 'user_id': 1}
      # Se valida el JSON q se envia
      serializer = self.serializer_class(data=data)
      serializer.is_valid(raise_exception=True)

      user = MyUser.objects.get(id=data['user_id'])
      userID= user.id

      existencia_library = LibraryModel.objects.filter(user_id=userID).exists() # da valor True si existe la library

      if existencia_library:
        return Response({
          'message': 'Libreria Existente'
        })

      else:
        # Se   guarda la libreria
        library = LibraryModel.objects.create(
            user_id = user,
        )
        # library.save()
        # Sumar +1 al total de veces guardado
        for item in data['details']:
          entryID = item['entry_id']
          entryStatus = item['status_saved']

          entry = EntryModel.objects.get(id=entryID)
          if entryStatus == True:
            entry.times_saved += 1
          # entry.save()

          # Guardamos el detalle de la libreria
          libraryDetail = LibraryDetailModel.objects.create(
            entry_id = entry,
            status_saved = entryStatus,
            library_id = library,
          )
          # libraryDetail.save()

          print(entry)

        return Response({
          'message': 'Libreria guardada correctamente'
        }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response({
        'errors': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LibraryUpdateView(generics.UpdateAPIView):
  queryset = LibraryModel.objects.all()
  serializer_class = LibraryUpdateSerializer

  @transaction.atomic
  def update(self, request, *args, **kwargs):
    kwargs_id = kwargs['pk']
    try:

      data = request.data
      serializer = self.serializer_class(data=data)
      serializer.is_valid(raise_exception=True)

      user_id = MyUser.objects.get(id=data['user_id'])
      existencia_library = LibraryModel.objects.filter(user_id=user_id).exists()

      if existencia_library:
        status_library = data['status']

        library = LibraryModel.objects.get(id=kwargs_id)
        library.status = status_library
        library.save()

      else:
          return Response({
            'message': 'Libreria inexistente'
          })

      for item in data ['details']:
        entryID = item['entry_id']
        libraryID = item['library_id']
        statusSave = item['status_saved']

      library_detail = EntryModel.objects.get(id=entryID)
      detail_id = library_detail.id
      existencia_detail = EntryModel.objects.filter(id=detail_id).exists()

      if existencia_detail:
        detail_status = LibraryDetailModel.objects.get(entry_id=entryID, library_id=libraryID)
        detail_status.status_saved = statusSave
        detail_status.save()

        entry = EntryModel.objects.get(id=entryID)
        if statusSave == False:
          entry.times_saved -= 1
        if statusSave == True:
          entry.times_saved += 1
        entry.save()

        return Response({
            'message': 'Detail actualizada correctamente'
          }, status=status.HTTP_200_OK)

    except LibraryDetailModel.DoesNotExist:
      new_detail = LibraryDetailModel.objects.create(
        entry_id = library_detail,
        status_saved = statusSave,
        library_id = library,
      )
      new_detail.save()

      return Response({
        'message': 'Deatail creado correctamente'
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response ({
        'errors': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LibraryDeleteView(generics.DestroyAPIView):
  queryset = LibraryModel.objects.all()
  serializer_class = LibrarySerializer

  def destroy(self, request, *args, **kwargs):
    try:
      instance = self.get_object()
      instance.status = False
      instance.save()

      return Response({
        'message': 'Libreria eliminada correctamente'
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response ({
        'errors': str(e)
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TagsView(generics.ListAPIView):
  queryset = TagsModel.objects.all()
  serializer_class = TagsSerializer

class TagsCreateView(generics.CreateAPIView):
  queryset = TagsModel.objects.all
  serializer_class = TagsCreateSerializer

  @transaction.atomic
  def create(self, request, *args, **kwargs):
    try:

      data = request.data # {'details': [{'status_saved': True, 'entry_id': 1}], 'name': 'string', 'description': 'string', 'status': True}

      serializer = self.serializer_class(data=data)
      serializer.is_valid(raise_exception=True)

      tag_code = data.get('code_tag')
      tag_existente = TagsModel.objects.filter(code_tag=tag_code).exists()

      if tag_existente:
        return Response({
          'message': 'CodeTag en uso'
        })

      else:
        tag = TagsModel.objects.create(
          name = data['name'],
          description = data['description'],
          code_tag = data['code_tag'],
        )
        tag.save

        for item in data['details']:
          entryID = item['entry_id']
          entryStatus = item['status_saved']

          entry = EntryModel.objects.get(id=entryID)

          tagDetail = TagsDetailModel.objects.create(
            entry_id = entry,
            status_saved = entryStatus,
            tags_id = tag,
          )
          tagDetail.save()

        return Response({
          'message': 'Tag Creado Correctamente'
        }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response({
        'errors': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TagsUpdateView(generics.UpdateAPIView):
  queryset = TagsModel.objects.all()
  serializer_class = TagsUpdateSerializer

  @transaction.atomic
  def update(self, request, *args, **kwargs):
    kwargs_id = kwargs['pk']
    try:

      data = request.data
      serializer = self.serializer_class(data=data)
      serializer.is_valid(raise_exception=True)

      tag_id = TagsModel.objects.get(code_tag=data['code_tag'])
      tagCODE = tag_id.code_tag
      tagID = tag_id.id
      existencia_tag = TagsModel.objects.filter(code_tag=tagCODE).exists()

      if existencia_tag:
        name_tag = data['name']
        description_tag = data ['description']
        status_tag = data['status']

        tag = TagsModel.objects.get(id=tagID)
        tag.name = name_tag
        tag.description = description_tag
        tag.status = status_tag
        tag.save()

      else:
        return Response({
          'message': 'Tag inexistente'
        })

      for item in data ['details']:
        entryID = item['entry_id']
        tagSave = item['status_saved']
        tagID = item['tags_id']

      tag_detail = EntryModel.objects.get(id=entryID)
      detail_id = tag_detail.id
      existencia_detail = EntryModel.objects.filter(id=detail_id).exists()

      if existencia_detail:
        detail_status = TagsDetailModel.objects.get(entry_id = entryID, tags_id=tagID)
        detail_status.status_saved = tagSave
        detail_status.save()

      return Response({
        'message': 'Tag actualizada correctamente'
      }, status=status.HTTP_200_OK)

    except TagsDetailModel.DoesNotExist:
      new_detail = TagsDetailModel.objects.create(
        status_saved = tagSave,
        entry_id = tag_detail,
        tags_id = tag,
      )
      new_detail.save()

      return Response({
        'message': 'Deatail creado correctamente'
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response ({
        'errors': str(e)
      }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TagsDeleteView(generics.DestroyAPIView):
  queryset = TagsModel.objects.all()
  serializer_class = TagsSerializer

  def destroy(self, request, *args, **kwargs):
    try:
      instance = self.get_object()
      instance.status = False
      instance.save()

      return Response({
        'message': 'Tag eliminado correctamente'
      }, status=status.HTTP_200_OK)

    except Exception as e:
      return Response ({
        'errors': str(e)
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)