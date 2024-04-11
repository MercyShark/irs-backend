from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Documents, es
from .forms import SearchForm
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect

@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
            files = request.FILES.getlist('file') # memoryuploadfile object .. having name, content_type, size, charset, content, read, chunks, multiple_chunks
            urls = request.POST.getlist('links')
            for file in files:
                Documents.objects.create(file=file)
            for url in urls:
                Documents.objects.create(url=url)
            context_data = { 
                "show": True
            }
            return render(request, 'retriever/upload_file.html',context=context_data)
    else:
        return render(request, 'retriever/upload_file.html')
    

@csrf_exempt
def searchView(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_body = {
                "query": {
                    "match_phrase": {
                        "content": query
                    },
                },
                "highlight": {
                    "number_of_fragments": 0,
                    "fields": {
                        "content": {
                            "pre_tags": ["<span style='color:red;background-color:yellow;'>"],
                            "post_tags": ["</span>"]
                        } 
                    }
                }
            }


            search_results = es.search(index="my_document_index", body=search_body)

            pdf_found_count = 0
            text_found_count = 0
            html_found_count = 0
            image_found_count = 0
            url_found_count = 0
            for hit in search_results["hits"]["hits"]:
                extension = hit["_source"]["title"].split('/')[-1].split('.')[-1]
                if extension == 'pdf':
                    pdf_found_count += 1
                elif extension == 'txt':
                    text_found_count += 1
                elif extension == 'html':
                    html_found_count += 1
                elif extension in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
                    image_found_count += 1
                else:
                    url_found_count += 1


            results = {
            "time_taken": search_results['took'],
            "total_documents_found": search_results['hits']['total']['value'],
            "total_documents": Documents.objects.all().count(),
            "pdf_found": pdf_found_count,
            "text_found": text_found_count,
            "html_found": html_found_count,
            "image_found": image_found_count,
            "url_found": url_found_count,
            "data": [
                {
                    "title": hit["_source"]["title"],
                    "id": hit["_id"],
                    "highlighted_content": mark_safe("".join(hit["highlight"]["content"]).replace("\n", "<br>").replace('"','')),
                    "occurrences": "".join(hit["highlight"]["content"]).count("</span>"),
                    "extension": hit["_source"]["title"].split('/')[-1].split('.')[-1],
                } for hit in search_results["hits"]["hits"]
            ]
            }

            print(results)
            context_data = {
                "form": form,
                "results": results
            }
            return render(request, 'retriever/search.html', context=context_data)
        else:
            return HttpResponse("Invalid form")
    if request.method == 'GET':
        form = SearchForm()
    return render(request, 'retriever/search.html', {'form': form})

@csrf_exempt
def deleteDocumentView(request):
    if request.method == 'POST':
        path = request.POST.get('path_redirect')
        print(request.POST)
        Documents.objects.all().delete()
        es.delete_by_query(index="my_document_index", body={"query": {"match_all": {}}})
        return HttpResponseRedirect(path)
    return HttpResponse("Invalid Request")

def ViewDocuments(request):
    documents = Documents.objects.all()

    context_data = { 
        "documents": documents,
        "pdf_count": Documents.count_pdf(Documents),
        "text_count": Documents.count_text(Documents),
        "html_count": Documents.count_html(Documents),
        "image_count": Documents.count_image(Documents),
        "url_count": Documents.count_url(Documents),
            }
    return render(request, 'retriever/all_documents.html',context=context_data )