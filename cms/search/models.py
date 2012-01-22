from django.db import models
from django.contrib.flatpages.models import FlatPage

# Create your models here.
class SearchKeyword(models.Model):
    keyword = models.CharField(max_length=50)
    page = models.ForeignKey(FlatPage)
    
    def __unicode__(self):
        return self.keyword