from rest_framework.serializers import ModelSerializer
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Recipe

class RecipeSerializer(ModelSerializer):
    
    class Meta:
        model = Recipe
        fields = ['id', 'user', 'image', 'title', 'ingredients', 'tools', 'description', 'private']
        read_only_fields = ['user']
