from rest_framework import permissions
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        is_admin = request.user.groups.filter(name='admin').exists()
        return request.user.is_authenticated and is_admin
class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  
            return True
        return bool(request.user and request.user.is_authenticated)
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_owner= obj.owner == request.user 
        is_admin = request.user.groups.filter(name='admin').exists()
        return is_owner or is_admin
class IsTeacherOrAdmins(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.groups.filter(name__in=['admin', 'teacher']).exists()
