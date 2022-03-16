from django.db import models


class Exam(models.Model):
    start_word = models.IntegerField()
    end_word = models.IntegerField()

    def __str__(self):
        return str(self.start_word) + "-" + str(self.end_word)
