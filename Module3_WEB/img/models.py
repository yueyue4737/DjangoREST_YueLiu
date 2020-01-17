from django.db import models

class Album(models.Model):
    # Charfield, Textfield, Imagefield ...
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.album_title + '-' + self.artist

class Image(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10) # i.e, .jpg, .png. etc.
    image_title = models.CharField(max_length=250)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.image_title