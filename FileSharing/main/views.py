from django.shortcuts import render

# Create your views here.
from django.core.files.storage import FileSystemStorage

def upload(request):
    context = {}

    if request.method == 'POST'
        upload_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(upload_file.name, upload_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)
