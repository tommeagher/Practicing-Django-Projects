from django.db import models



class Category(models.Model):
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text='Suggested value automatically generated from title. Must be unique.')
    description = models.TextField()
    
    class Meta: 
        ordering = ['title']
        verbose_name_plural="Categories"
    
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return "/categories/%s" % self.slug