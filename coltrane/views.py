from django.shortcuts import get_object_or_404, render_to_response
from coltrane.models import Entry, Category
from django.views.generic.list_detail import object_list

#do I still need/want this?
def entries_index(request):
    return render_to_response('coltrane/entry_index.html', {'object_list': Entry.live.all() })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return object_list(request, queryset=category.live_entry_set(), extra_context={ 'category': category })

# From Ben Welsh's excellent palewire.com code
def tag_detail(request, tag):
    """
    A list that reports all of the content with a particular tag.
    """
    try:
        tag = Tag.objects.get(name=tag)
    except Tag.DoesNotExist:
        # If the tag isn't found, try it with hyphens removed, which
        # was the convention on my old Wordpress blog. This can help
        # keep old tag page links alive.
        try:
            tag = Tag.objects.get(name=tag.replace("-", ""))
        except Tag.DoesNotExist:
            raise Http404
    
    # Pull all the items with that tag.
    taggeditem_list = TaggedItem.objects.filter(tag=tag).fetch_generic_relations()
    
    # Loop through the tagged items and return just the items
    object_list = [i.object for i in taggeditem_list if getattr(i.object, 'pub_date', False)]
    
    # Now resort them by the pub_date attribute we know each one should have
    object_list.sort(key=lambda x: x.pub_date, reverse=True)
    
    # Slice it to 500 max
    object_list = object_list[:500]

    if len(object_list) == 500:
        maxed_out = True
    else:
        maxed_out = False

    # Pass it out
    return render(request, 'coltrane/tag_detail.html', { 
            'tag': tag, 
            'object_list': object_list,
            'maxed_out': maxed_out,
        })


#made redundant by generic view    
#def category_list(request):
#    return render_to_response('coltrane/category_list.html', {'object_list': Category.objects.all() })

#def category_detail(request):
#    category = get_object_or_404(Category, slug=slug)
#    return render_to_response('coltrane/category_detail.html', {'object_list': category.entry_set.all(), 'category': category'})
    
#def entry_detail(request, year, month, day, slug):
#    import datetime, time
#    date_stamp = time.strptime(year+month+day, "%Y%b%d")
#    pub_date = datetime.date(*date_stamp[:3])
#    entry = get_object_or_404(Entry, pub_date__year=pub_date.year, pub_date__month=pub_date.month, pub_date__day=pub_date.day, slug=slug) 
#    return render_to_response('coltrane/entry_detail.html', { 'entry': entry })
    