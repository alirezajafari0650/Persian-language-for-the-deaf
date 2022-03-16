from django.db import models


class WordCategory(models.Model):
    icon = models.FileField(upload_to='icon/', null=True, blank=True)
    parent = models.ForeignKey('words.WordCategory', on_delete=models.CASCADE, null=True, blank=True)
    sort_id = models.IntegerField(default=0)
    farsi_name = models.CharField(max_length=50, null=True, blank=True)
    english_name = models.CharField(max_length=50, null=True, blank=True)
    arabic_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.farsi_name


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
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.farsi_name
