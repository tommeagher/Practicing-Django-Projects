import datetime

from django.contrib.auth.models import User
from django.db import models

from markdown import markdown
from tagging.fields import TagField

from django.conf import settings

class Category(models.Model):
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text='Suggested value automatically generated from title. Must be unique.')
    description = models.TextField()
    
    def live_entry_set(self):
        from coltrane.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)
    
    class Meta: 
        ordering = ['title']
        verbose_name_plural="Categories"
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_category_detail', (), { 'slug': self.slug })
        

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)
        
class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    
    #core fields
    title = models.CharField(max_length=250, help_text="Maximum 250 characters.")
    excerpt = models.TextField(blank=True, help_text="A short summary of the entry. Optional.")
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    
    #fields to store generated HTML
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank = True)
    
    #metadata
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique_for_date='pub_date', help_text="Suggested value automatically generated from title. Must be unique.")
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS, help_text="Only entries with live status will be publicly displayed.")
    
    #Categorization
    categories = models.ManyToManyField(Category)
    tag = TagField(help_text="Separate tags with spaces.")
    
    #For the filtering of live entries
    objects = models.Manager()
    live = LiveEntryManager()
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "Entries"
    
    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save(force_insert, force_update)

    @models.permalink
    def get_absolute_url(self):
        #return "/weblog/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)
        return ('coltrane_entry_detail', (), { 'year': self.pub_date.strftime("%Y"), 'month': self.pub_date.strftime("%b").lower(), 'day': self.pub_date.strftime("%d"), 'slug': self.slug })
    
    #get_absolute_url = models.permalink(get_absolute_url)
    
class Link(models.Model):
    #Metadata
    enable_comments = models.BooleanField(default = True)
    post_elsewhere = models.BooleanField('Post to Pinboard', default=True, help_text='If checked, this link will be posted both to your weblog and to your pinboard account.')
    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique_for_date='pub_date', help_text='Must be unique for the publication date.')


    #The actual link-y bits.
    description = models.TextField(blank=True)
    description_html = models.TextField(editable=False, blank=True)
    via_name = models.CharField('Via', max_length=250, blank=True, help_text='The name of the person whose site you spotted the link on. Optional.')
    via_url = models.URLField('Via URL', blank=True, help_text='The URL of the site where you spotted the link. Optional.')
    tags = TagField()
    url = models.URLField(unique=True)
    
    class Meta:
        ordering = ['-pub_date']
    
    def __unicode__(self):
        return self.title
    
    def save(self):
        if not self.id and self.post_elsewhere:
            import pinboard
            from django.utils.encoding import smart_str
            pin = pinboard.connect(settings.PINBOARD_USER, settings.PINBOARD_PASS)
            pin.add(smart_str(self.url), smart_str(self.title), smart_str(self.description), smart_str(self.tags))
        if self.description:
            self.description_html = markdown(self.description)
        super(Link, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return('coltrane_link_detail', (), {   'year': self.pub_date.strftime('%Y'),
        								   'month': self.pub_date.strftime('%b').lower(), 
        								   'day': self.pub_date.strftime('%d'), 
        								   'slug': self.slug })
    #get_absolute_url = models.permalink(get_absolute_url)
    
from akismet import Akismet
from django.conf import settings            
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_will_be_posted
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str

def moderate_comment(sender, comment, request, **kwargs):
    if not comment.id:
        entry = comment.content_object
        delta = datetime.datetime.now() - entry.pub_date
        if delta.days > 30:
            comment.is_public = False
        else: 
            akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url="http:/%s/" %Site.objects.get_current().domain)
            if akismet_api.verify_key():
                akismet_data = { 'comment_type': 'comment',
                                    'referrer': request.META['HTTP_REFERER'],
                                    'user_ip': comment.ip_address,
                                    'user-agent': request.META['HTTP_USER_AGENT'] }
                if akismet_api.comment_check(smart_str(instance.comment), akismet_data, build_date=True):
                    comment.is_public=False

comment_will_be_posted.connect(moderate_comment, sender=Comment)
    