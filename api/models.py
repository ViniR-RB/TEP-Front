from django.contrib.auth.models import User
from django.db import models


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Notice(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=100, null=False,
                             blank=False),
    image = models.ImageField()
    body = models.CharField(max_length=255, null=False,
                            blank=False)
    creation_date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.image_url.named = f'{self.creator.id}/{self.title}.%s' % self.image_url.name.split('.')[
                1]
        return super(Notice, self).save(*args, **kwargs)

    def __str__(self):
        return self.descricao
