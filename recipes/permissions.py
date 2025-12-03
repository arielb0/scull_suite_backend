from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class RecipePermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        
        user_is_owner = request.user.id == obj.user.id

        if request.method in SAFE_METHODS:
            return (not obj.private) or user_is_owner
        
        if request.user.is_authenticated:
            return user_is_owner
        
        return False
        
    
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.is_authenticated    