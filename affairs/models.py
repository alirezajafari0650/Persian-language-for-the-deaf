from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class AffairCategory(models.Model):
    icon = models.FileField(upload_to='media/icon/', null=True, blank=True)
    parent = models.ForeignKey('affairs.AffairCategory', on_delete=models.CASCADE, null=True, blank=True)
    sort_id = models.IntegerField(null=True, blank=True)
    farsi_name = models.CharField(max_length=50, null=True, blank=True)
    english_name = models.CharField(max_length=50, null=True, blank=True)
    arabic_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.farsi_name if self.farsi_name else str(self.id)


class Affair(models.Model):
    farsi_description = models.CharField(max_length=256, null=True, blank=True)
    english_description = models.CharField(max_length=256, null=True, blank=True)
    arabic_description = models.CharField(max_length=256, null=True, blank=True)
    sort_id = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(AffairCategory, on_delete=models.CASCADE, null=True, blank=True)
    video = models.FileField(upload_to='media/videos/', null=True, blank=True)

    def __str__(self):
        return self.farsi_description if self.farsi_description else str(self.id)


class AffairLinkManager(models.Model):
    link = models.URLField(blank=True)
    affair = models.ForeignKey(Affair, on_delete=models.CASCADE, related_name='video_link')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def generate_link(self):
        lid = urlsafe_base64_encode(force_bytes(self.id))
        token = default_token_generator.make_token(self.user)
        domain = 'http://127.0.0.1:8080/affair-api'
        self.link = "%s/affair_video/%s/%s/" % (domain, token, lid)
        self.save()
        return self.link

    def check_link(self, token, path):
        print(token, path)
        response = bool(
            default_token_generator.check_token(self.user, token) and
            self.link == path and
            self.user.is_authenticated and
            self.user.is_professional
        )
        self.generate_link()
        return response

    def __str__(self):
        return str(self.user.username) + ' - ' + self.affair.farsi_description
