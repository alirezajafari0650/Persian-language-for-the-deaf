from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class WordCategory(models.Model):
    icon = models.FileField(upload_to='media/icon/', null=True, blank=True)
    parent = models.ForeignKey('words.WordCategory', on_delete=models.CASCADE, null=True, blank=True)
    sort_id = models.IntegerField(null=True, blank=True)
    farsi_name = models.CharField(max_length=50, null=True, blank=True)
    english_name = models.CharField(max_length=50, null=True, blank=True)
    arabic_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.farsi_name if self.farsi_name else str(self.id)


class Word(models.Model):
    farsi_name = models.CharField(max_length=50, null=True, blank=True)
    farsi_description = models.CharField(max_length=256, null=True, blank=True)
    farsi_description2 = models.CharField(max_length=256, null=True, blank=True)
    english_name = models.CharField(max_length=50, null=True, blank=True)
    english_description = models.CharField(max_length=256, null=True, blank=True)
    english_description2 = models.CharField(max_length=256, null=True, blank=True)
    arabic_name = models.CharField(max_length=50, null=True, blank=True)
    arabic_description = models.CharField(max_length=256, null=True, blank=True)
    arabic_description2 = models.CharField(max_length=256, null=True, blank=True)
    sort_id = models.IntegerField(default=0)
    category = models.ForeignKey(WordCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)
    video = models.FileField(upload_to='media/videos/', null=True, blank=True)

    def __str__(self):
        return self.farsi_name if self.farsi_name else str(self.id)


class LinkManager(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(blank=True)

    def generate_link(self):
        lid = urlsafe_base64_encode(force_bytes(self.id))
        token = default_token_generator.make_token(self.user)
        domain = 'http://127.0.0.1:8000'
        self.link = "%s/video/%s/%s/" % (domain, token, lid)
        self.save()
        return self.link

    def check_link(self, token, path):
        return bool(
            default_token_generator.check_token(self.user, token) and
            self.link == path and
            self.user.is_authenticated
        )

    def __str__(self):
        return str(self.user.username) + ' - ' + self.word.farsi_name
