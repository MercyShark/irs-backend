from django.shortcuts import render
from elasticsearch import Elasticsearch
from .extractor import TextExtractor
from django.shortcuts import HttpResponse
from .forms import DocumentForm
from django.views.decorators.csrf import csrf_exempt
from .models import Documents
# Initialize Elasticsearch client

# es = Elasticsearch('http://localhost:9200')
# Create an index
# print(es.ping()) # True if connected


# indices = es.indices.get_alias()
# for index in indices:
#     print(index)
index_name = "gg_index"
# if not es.indices.exists(index=index_name):
    # es.indices.create(index=index_name)
@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
            files = request.FILES.getlist('file') # memoryuploadfile object .. having name, content_type, size, charset, content, read, chunks, multiple_chunks
            # file_contents = []
            for file in files:
                Documents.objects.create(file=file)
            # form = DocumentForm(request.POST, request.FILES)
            # if form.is_valid():
                # form.save()
            return render(request, 'retriever/upload_success.html')
            # print(form.errors)
            # return HttpResponse("Form is not valid")

            # file_contents = []
            # extractor = TextExtractor()
            # image_file_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
            # for i, file in enumerate(files, start=1):
            #     name, extension = file.name.split('.')
            #     if extension in image_file_extensions:
            #         text = extractor.fromImageFileEasyOCR(file)
            #         file_contents.append({
            #             "file_name": file.name,
            #             "title": name,
            #             "type": "image",
            #             "content": text
            #         })
            #     elif extension == 'pdf':
            #         text = extractor.fromPDFFile(file)
            #         file_contents.append({
            #             "file_name": file.name,
            #             "title": name,
            #             "type": "pdf",
            #             "content": text
            #         })
            #     elif extension == 'txt':
            #         text = extractor.fromTextFile(file)
            #         file_contents.append({
            #             "file_name": file.name,
            #             "title": name,
            #             "type": "text",
            #             "content": text
            #         })
            #     elif extension == 'html':
            #         text = extractor.fromHTMLFile(file)
            #         file_contents.append({
            #             "file_name": file.name,
            #             "title": name,
            #             "type": "html",
            #             "content": text
            #         })
            
            # return render(request, 'retriever/upload_success.html', context={'file_contents': file_contents})
    else:
        return render(request, 'retriever/upload_file.html')

def handle_uploaded_file(uploaded_file):
    # Read the content of the file
    file_content = uploaded_file.read().decode('utf-8')  # Assuming UTF-8 encoding
    return file_content
# def document_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('search')  # Redirect to a search page (to be implemented)
#     else:
#         form = DocumentForm()
#     return render(request, 'retriever/document_form.html', {'form': form})



# def search(request):
#     form = SearchForm()
#     results = []
#     query = request.GET.get('query')
#     if query:
#         results = Document.objects.filter(content__icontains=query)
#     return render(request, 'retriever/search.html', {'form': form, 'results': results})