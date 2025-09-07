from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.upload, name='upload'),
    path('login/', views.login_view, name='login'),
    path('files/', views.file_list, name='file_list'),
    path('delete/<str:filename>/', views.delete_file, name='delete_file'),
    path('logout/', views.logout_view, name='logout'),
]

# Serve media files in production through Django (not recommended for high traffic)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
