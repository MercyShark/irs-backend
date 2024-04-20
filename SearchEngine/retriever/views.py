from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Documents, es
from .forms import SearchForm
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from .models import collection
from .utils import get_positions, highlight_query_in_text


@csrf_exempt
def upload_files(request):
    if request.method == "POST":
        files = request.FILES.getlist(
            "file"
        )  # memoryuploadfile object .. having name, content_type, size, charset, content, read, chunks, multiple_chunks
        urls = request.POST.getlist("links")
        urls = "".join(urls).split(",")
        for file in files:
            Documents(file=file).save()
        if urls[0] == "":
            urls = []
        for url in urls:
            Documents(url=url).save()
        context_data = {"show": True}
        return render(request, "retriever/upload_file.html", context=context_data)
    else:
        return render(request, "retriever/upload_file.html")


@csrf_exempt
def searchView(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            data = get_positions(collection.find(), query)
            for d in data:
                d["org_document"] = Documents.objects.get(id=d["id"])
                d["highlighted_content"] = highlight_query_in_text(
                    (d["org_document"].text).replace("\n", "<br>"),
                    query,
                    tag_name="span",
                    style="color:red;background-color:yellow;",
                )
                # d['highlighted_content'] = mark_safe((d['org_document'].text).replace(query, f"<span style='color:red;background-color:yellow;'>{query}</span>").replace("\n", "<br>").replace('"',''))
                # d['highlighted_content'] = re.sub(r"\b" + query + r"\b", lambda x: f"<span style='color:red;background-color:yellow;'>{x.group()}</span>", d['org_document'].text, flags=re.IGNORECASE)

            pdf_found_count = 0
            text_found_count = 0
            html_found_count = 0
            image_found_count = 0
            url_found_count = 0

            for d in data:
                if d.get("extension") == "pdf":
                    pdf_found_count += 1
                elif d.get("extension") == "txt":
                    text_found_count += 1
                elif d.get("extension") == "html":
                    html_found_count += 1
                elif d.get("extension") in ["png", "jpg", "jpeg", "gif", "bmp"]:
                    image_found_count += 1
                else:
                    url_found_count += 1

            context_data = {
                "form": form,
                "results": {
                    "total_documents_found": len(data),
                    "pdf_found": pdf_found_count,
                    "text_found": text_found_count,
                    "html_found": html_found_count,
                    "image_found": image_found_count,
                    "url_found": url_found_count,
                    "total_documents": Documents.objects.all().count(),
                    "data": data,
                },
            }
            return render(request, "retriever/search.html", context=context_data)
        else:
            return HttpResponse("Invalid form")
    if request.method == "GET":
        form = SearchForm()
    return render(request, "retriever/search.html", {"form": form})


@csrf_exempt
def deleteDocumentView(request):
    if request.method == "POST":
        path = request.POST.get("path_redirect")
        print(request.POST)
        Documents.objects.all().delete()
        collection.delete_many({})
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
    return render(request, "retriever/all_documents.html", context=context_data)
