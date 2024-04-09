from typing import Iterable
from django.db import models
from .extractor import TextExtractor
from elasticsearch import Elasticsearch
from .search import DocumentIndex

es = Elasticsearch('http://localhost:9200')

class Documents(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    



    def save(self, *args, **kwargs):
        file = self.file
        extractor = TextExtractor()
        image_file_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
        name, extension = file.name.split('.')
        if extension in image_file_extensions:
            self.text = extractor.fromImageFileEasyOCR(file)
        elif extension == 'pdf':
            self.text = extractor.fromPDFFile(file)
        elif extension == 'txt':
            self.text = extractor.fromTextFile(file)
        elif extension == 'html':
            self.text = extractor.fromHTMLFile(file)
            
        self.title = self.file.name
        
        super().save(*args, **kwargs)
        # print(instance)
        
        if(es.ping()):
            doc = DocumentIndex(title=self.file.name, content=self.text, id=self.id)
            doc = doc.save(using=es)

    @property
    def get_url(self):
        return "http://localhost:8000" + self.file.url

    @property
    def get_extension(self):
        return self.file.name.split('.')[-1]
    def __str__(self):
        return self.title