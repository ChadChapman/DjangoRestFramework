from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	#custom permission, only object owners can edit said object

	def has_object_permission(self, request, view, obj):
		"""
		read permissions = any request
		so then, always allow GET, HEAD, OPTIONS requests
		"""
		if request.method in permissions.SAFE_METHODS:
			return True

		#write permissions belong only to object owner/creator
		return obj.owner == request.user

		