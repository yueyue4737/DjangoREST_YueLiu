from django.shortcuts import render, get_object_or_404
from .models import Album

def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums}
    return render(request, 'img/index.html', context)

def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'img/detail.html', {'album': album})

def favourite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_image = album.image_set.get(pk=request.POST['song'])
    except(KeyError, Image.DoesNotExist):
        return render(request, 'img/detail.html', {
                    'album': album,
                    'error_message': 'invalid',
        })
    else:
        selected_image.is_favourite = True
        selected_image.save()
        return render(request, 'img/detail.html', {'album': album})