from rest_framework import permissions
from .permissions import IsStaffEditorPermissions

class StaffEditorPermissionsMixin():
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermissions]

class UserQuerySetMixin():
    userfield = 'user'
    def get_queryset(self, *args, **kwargs):
        lookup_data = {}
        lookup_data[self.user_field] = self.request.user
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(**lookup_data)