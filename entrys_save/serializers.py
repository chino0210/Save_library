from rest_framework import serializers
from .models import (
  EntryModel,
  LibraryModel,
  LibraryDetailModel,
  MyUser)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# UsersSerializer
class UserCreateSerializer (serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = MyUser
    exclude = ['last_login']

  def save(self):
    try:
      name = self.validated_data['name']
      document_type = self.validated_data['document_type']
      document_number = self.validated_data['document_number']
      email = self.validated_data['email']
      password = self.validated_data['password']

      user = MyUser(
        document_type=document_type,
        document_number=document_number,
        email=email,
        name=name,
      )
      user.set_password(password)
      user.save()
      return user

    except KeyError as e:
      print(e, 1000000000000)
      raise serializers.ValidationError(f'Error: {e}')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token['email'] = user.email
    return token

class EntrySerializer (serializers.ModelSerializer):
  class Meta:
    model = EntryModel
    fields = '__all__'

  def to_representation(self, instance):
    representation =  super().to_representation(instance)
    representation ['document'] = instance.document.url
    return representation

class EntryUpdateSeliarizer (serializers.ModelSerializer):
  name = serializers.CharField(required=False)
  autor = serializers.CharField(required=False)
  description = serializers.CharField(required=False)
  document = serializers.FileField(required=False)
  status = serializers.BooleanField(required=False)

  class Meta:
    model = EntryModel
    fields = '__all__'

# Serializadores para listar librerias
class LibraryDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = LibraryDetailModel
    fields = '__all__'

class LibrarySerializer(serializers.ModelSerializer):
  details = LibraryDetailSerializer(source='libraryDetails',many=True)
  class Meta:
    model = LibraryModel
    fields = '__all__'

# Serializadores para crear librerias
class LibraryDetailCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = LibraryDetailModel
    exclude = ['library_id']

class LibraryCreateSerializer(serializers.ModelSerializer):
  details = LibraryDetailCreateSerializer (source='LibraryDetails', many=True)

  class Meta:
    model = LibraryModel
    fields = '__all__'