from django.db import models


class Image(models.Model):
    file = models.ImageField(blank=False, null=False, upload_to='queries/%Y/%m/%d')

    def __str__(self):
        return self.file.name
