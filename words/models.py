from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
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
    video1 = models.FileField(upload_to='media/videos/', null=True, blank=True)
    video2 = models.FileField(upload_to='media/videos2/', null=True, blank=True)

    def __str__(self):
        return self.farsi_name if self.farsi_name else str(self.id)


class NewWord(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام')
    user = models.ManyToManyField(User)
    date = models.DateTimeField(auto_now_add=True)
    is_added = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'کلمه جدید'
        verbose_name_plural = 'کلمات جدید'


class LinkManager(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='video_link')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(blank=True)
    used_for = models.CharField(max_length=5, default='')

    def generate_link(self):
        lid = urlsafe_base64_encode(force_bytes(self.id))
        token = default_token_generator.make_token(self.user)
        domain = settings.DOMAIN + '/word-api'
        self.link = "%s/video/%s/%s/" % (domain, token, lid)
        self.used_for = ''
        self.save()
        return self.link

    def check_link(self, token, path, video_number):
        response = bool(
            video_number not in self.used_for and
            default_token_generator.check_token(self.user, token) and
            self.link == path and
            self.user.is_authenticated and
            self.user.is_professional
        )
        if response:
            self.used_for = self.used_for + '_' + video_number
            self.save()
        else:
            self.generate_link()
        return response

    def __str__(self):
        return str(self.user.username) + ' - ' + self.word.farsi_name


class Exam(models.Model):
    start_word = models.IntegerField()
    end_word = models.IntegerField()

    def __str__(self):
        return str(self.start_word) + "-" + str(self.end_word)
