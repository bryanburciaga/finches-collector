from django.db import models

# Create your models here.
class Finch(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

class Feeding(models.Model):
    date = models.DateField()
    meal = models.CharField(max_length=1)


    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('finches_detail', kwargs={'finch_id': self.id })