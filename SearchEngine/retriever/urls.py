from django.urls import path
# from .views import document_upload, search

from .views import upload_files, searchView,ViewDocuments,deleteDocumentView
urlpatterns = [
    path('upload/', upload_files, name='upload'),
    path('', ViewDocuments, name='uploaded_documents'),
    path('search/', searchView, name='search'),
    path("delete_documents/", deleteDocumentView, name="delete_documents")
] 