from django.http import HttpResponse
from django.template import Context, loader

from ordinances.models import Ancestor

def index(request):
    all_ancestors_list = Ancestor.objects.order_by('surname', 'given_name')
    template = loader.get_template('ordinances/index.html')
    context = Context({
        'all_ancestors_list': all_ancestors_list,
    })
    return HttpResponse(template.render(context))
