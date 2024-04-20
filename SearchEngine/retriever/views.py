from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Documents, es
from .forms import SearchForm
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import collection
from .utils import get_positions
import re
@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
            files = request.FILES.getlist('file') # memoryuploadfile object .. having name, content_type, size, charset, content, read, chunks, multiple_chunks
            urls = request.POST.getlist('links')
            urls = "".join(urls).split(',')
            for file in files:
                Documents(file=file).save()
            if urls[0] == '': urls = []
            for url in urls:
                Documents(url=url).save()
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

            def stringMod(sentence,position,length):
                li = list(sentence.split())
                flag =False
                correctingFactor = 0
                temp=-1
                print(position)
                for element in position:
                    print(correctingFactor)
                    element +=correctingFactor
                    if(element<=temp):
                        element -=1
                        flag =True
                    li.insert(element,"<span style='color:red;background-color:yellow;'>")
                    print(element)
                    after = element+length+1
                    if(flag):
                        after +=1
                    temp=after
                    li.insert(after,"</span>")
                    correctingFactor += 2
                    print(after)
                return ' '.join(li)
            def highlight_exact_word(input_string, word, tag_name="span", **kwargs):
                pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
                highlighted_string = pattern.sub("<{} {}>{}</{}>".format(tag_name, ' '.join([f'{key}="{value}"' for key, value in kwargs.items()]), word, tag_name), input_string)
                return highlighted_string

            # def highlight_substring(input_string, substring, tag_name="span", **kwargs):
                # highlighted_string = re.sub(re.escape(substring), f"<{tag_name} {' '.join([f'{key}="{value}"' for key, value in kwargs.items()])}>{substring}</{tag_name}>", input_string, flags=re.IGNORECASE)
                # return highlighted_string
            # print("query", len(query.split()))
            query = query.lower()
            query = re.sub(r'[^a-zA-Z\s]', '', query)
            data = get_positions(collection.find(), query)
            for d in data:
                d['org_document'] = Documents.objects.get(id = d['id'])
                d['highlighted_content'] = highlight_exact_word((d['org_document'].text).replace("\n", "<br>"), query, tag_name="span", style='color:red;background-color:yellow;')
                # d['highlighted_content'] = mark_safe((d['org_document'].text).replace(query, f"<span style='color:red;background-color:yellow;'>{query}</span>").replace("\n", "<br>").replace('"',''))
                # d['highlighted_content'] = re.sub(r"\b" + query + r"\b", lambda x: f"<span style='color:red;background-color:yellow;'>{x.group()}</span>", d['org_document'].text, flags=re.IGNORECASE)
                # d['highlighted_content'] = stringMod(d['org_document'].text, d['start_positions'], len(query.split()))

            # for d in data:
                # html = ""
                # highlight the contain in the span tag .. and the return the whole text with hightlighted text in it.. 
                # for pos in d['start_positions']:
                    

            # highlight text from start postiton and to the end of the word query length
            
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
                "data": data
            }



            # results = {
            # "time_taken": search_results['took'],
            # "total_documents_found": search_results['hits']['total']['value'],
            # "total_documents": Documents.objects.all().count(),
            # "pdf_found": pdf_found_count,
            # "text_found": text_found_count,
            # "html_found": html_found_count,
            # "image_found": image_found_count,
            # "url_found": url_found_count,
            # "data": [
            #     {
            #         "title": hit["_source"]["title"],
            #         "id": hit["_id"],
            #         "highlighted_content": mark_safe("".join(hit["highlight"]["content"]).replace("\n", "<br>").replace('"','')),
            #         "occurrences": "".join(hit["highlight"]["content"]).count("</span>"),
            #         "extension": hit["_source"]["title"].split('/')[-1].split('.')[-1],
            #     } for hit in search_results["hits"]["hits"]
            # ]
            # }

            # compare occurance of the query in the document and the highlighted content

            print("*****************************************")
            for d in data:
                print(d['total_occurances'])

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
    return render(request, 'retriever/all_documents.html',context=context_data )