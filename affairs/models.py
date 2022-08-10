from django.db import models


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
    category = models.ForeignKey(AffairCategory, on_delete=models.CASCADE,null=True, blank=True)
    video = models.FileField(upload_to='media/videos/', null=True, blank=True)

    def __str__(self):
        return self.farsi_description if self.farsi_description else str(self.id)

