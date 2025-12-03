from rest_framework.viewsets import ModelViewSet
from .serializers import RecipeSerializer
from .models import Recipe
from django.db.models import Q
from .permissions import RecipePermissions

# Create your views here.

class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [RecipePermissions]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipe.objects.exclude(~Q(user=self.request.user) & Q(private=True))
        return Recipe.objects.exclude(private=True)
