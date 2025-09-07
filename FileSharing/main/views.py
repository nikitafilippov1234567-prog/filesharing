import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, Http404
from django.conf import settings
from django.contrib import messages

def login_view(request):
    """Handle login page"""
    if request.method == 'POST':
        password = request.POST.get('password', '')
        if password == settings.SITE_PASSWORD:
            request.session['authenticated'] = True
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Неправильный пароль'})
    return render(request, 'login.html')

def logout_view(request):
    """Handle logout"""
    request.session['authenticated'] = False
    return redirect('/login/')

def upload(request):
    """Handle file upload"""
    context = {}
    
    if request.method == 'POST':
        if 'document' in request.FILES:
            upload_file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(upload_file.name, upload_file)
            context['url'] = fs.url(name)
            context['success'] = f'Файл "{upload_file.name}" успешно загружен'
        else:
            context['error'] = 'Файл не выбран'
    
    # Get list of uploaded files
    try:
        media_path = settings.MEDIA_ROOT
        if os.path.exists(media_path):
            files = []
            for filename in os.listdir(media_path):
                file_path = os.path.join(media_path, filename)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    # Convert bytes to human readable format
                    if file_size < 1024:
                        size_str = f"{file_size} B"
                    elif file_size < 1024 * 1024:
                        size_str = f"{file_size / 1024:.1f} KB"
                    else:
                        size_str = f"{file_size / (1024 * 1024):.1f} MB"
                    
                    files.append({
                        'name': filename,
                        'size': size_str,
                        'url': f"{settings.MEDIA_URL}{filename}"
                    })
            context['files'] = files
    except Exception as e:
        context['files'] = []
    
    return render(request, 'upload.html', context)

def file_list(request):
    """API endpoint to get file list"""
    try:
        media_path = settings.MEDIA_ROOT
        files = []
        if os.path.exists(media_path):
            for filename in os.listdir(media_path):
                file_path = os.path.join(media_path, filename)
                if os.path.isfile(file_path):
                    files.append({
                        'name': filename,
                        'size': os.path.getsize(file_path),
                        'url': f"{settings.MEDIA_URL}{filename}"
                    })
        return JsonResponse({'files': files})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def delete_file(request, filename):
    """Delete a file"""
    if request.method == 'POST':
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'success': True, 'message': f'Файл "{filename}" удален'})
                else:
                    messages.success(request, f'Файл "{filename}" успешно удален')
                    return redirect('/')
            else:
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'success': False, 'error': 'Файл не найден'}, status=404)
                else:
                    messages.error(request, 'Файл не найден')
                    return redirect('/')
        except Exception as e:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
            else:
                messages.error(request, f'Ошибка при удалении файла: {str(e)}')
                return redirect('/')
    else:
        raise Http404("Method not allowed")
