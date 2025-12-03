from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.http import HttpRequest
from rest_framework.exceptions import AuthenticationFailed
    
class CreateAndReadPermission(BasePermission):

    def has_permission(self, request: HttpRequest, view):
        if (request.method in (SAFE_METHODS + ('POST',))):
            if (request.user.is_authenticated):
                return True
            else:
                raise AuthenticationFailed
        return False
