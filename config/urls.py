from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from surveys.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
