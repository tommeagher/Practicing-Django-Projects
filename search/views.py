# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.flatpages.models import FlatPage
from django.http import HttpResponseRedirect

def search(request):
    query = request.GET.get('q', '')
    keyword_results = []
    results = []
    if query: 
        keyword_results = FlatPage.objects.filter(
searchkeyword__keyword__in=query.split()).distinct()
        if keyword_results.count() == 1:
            return HttpResponseRedirect(keyword_results[0].get_absolute_url())
        results = FlatPage.objects.filter(content__icontains=query)
    return render_to_response('search/search.html', 
        { 'query': query, 
        'keyword_results': keyword_results,
        'results': results })

#This view displays all of the objects in a data model. 
#In this case, it lists all of the flatpages in the FlatPage model imported above, passing the "all_entries" variable to the context in the template, where a for loop lists each page. Brilliant
#note 'self' as the argument. can't leave it empty when it's referring to itself.
#note the database queries page: https://docs.djangoproject.com/en/dev/topics/db/queries/

def listpages(self):
    all_entries = FlatPage.objects.all()
    return render_to_response('search/list.html', {'all_entries': all_entries})
    
