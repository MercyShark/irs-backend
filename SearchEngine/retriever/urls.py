from django.urls import path
# from .views import document_upload, search
from .views import upload_files
urlpatterns = [
    path('upload/', upload_files, name='upload'),
    # path('search/', search, name='search'),
]