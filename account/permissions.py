from rest_framework.permissions import BasePermission,SAFE_METHODS

class EditDestroyPersonalAccount(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return view.kwargs['pk']==view.request.user.id or view.request.user.is_staff