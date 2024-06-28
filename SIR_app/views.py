from django.shortcuts import render
from .BooleanModel import show
from .ExtentedBooleanModel import show_a
from .VectorsModel import show_b
from .Read import read_doc_file
import os

list_files=['1.doc','2.doc','3.doc','4.doc','5.doc','6.doc','7.doc','8.doc','9.doc','M0.doc','M1.doc','M2.doc','M3.doc','M4.doc','M5.doc','M6.doc','M7.doc','M8.doc','M9.doc','M10.doc','M11.doc','M12.doc',]
def home(request):
    search_results = []
    content = ''

    if request.method == 'POST':
        search_input = request.POST.get('search-input', '')
        search_option = request.POST.get('select-option')

        if search_input:
            if search_option == 'Boolean Model':
                search_results_str = show(search_input)
            elif search_option == 'Extended Boolean':
                search_results_str = show_a(search_input)
            elif search_option == 'Vector Model':
                search_results_str = show_b(search_input)
            else:
                pass
                

            # Split the string into a list using ',' as the separator
            search_results = search_results_str.split(', ')
            x=list_files.index(search_results[0])
            content=read_doc_file(list_files[x])
          

           
            
    return render(request, 'index.html', {'search_results': search_results, 'CONT': content  })
def read(request, pk):
    content = ''

  
    content = read_doc_file(pk)

    return render(request, 'content.html', {'CONT': content,'pk':pk})