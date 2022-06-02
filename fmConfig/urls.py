from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register('rf-users/', )


# Admin placeholder change
admin.site.site_header = "Finance Manager"
admin.site.site_title = "Finance Manager Admin Panel"
admin.site.index_title = "Finance Manager Admin"

urlpatterns = [
    path('rf-admin/', include(router.urls)), #to access the browsable api view
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include([
        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls.jwt')),
        path('users/', include('users.api.urls', namespace='users')),
    ]))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

