from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, CASCADE, CharField, BooleanField, DateTimeField, TextField, SlugField
from django.utils.text import slugify


# Create your models here.
class Task(models.Model):
    user = ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    title = CharField(max_length=255)
    description = TextField(null=True, blank=True)
    slug = SlugField(max_length=255, unique=True)
    complete = BooleanField(default=False)
    create = DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        while Task.objects.filter(slug=self.slug).exists():
            slug = Task.objects.filter(slug=self.slug).first().slug
            if '-' in slug:
                try:
                    if slug.split('-')[-1] in self.title:
                        self.slug += '-1'
                    else:
                        self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                except:
                    self.slug = slug + '-1'
            else:
                self.slug += '-1'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'
