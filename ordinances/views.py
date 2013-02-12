from django.http import HttpResponse
from django.template import Context, loader

from ordinances.models import Ancestor

def index(request):
    all_ancestors_list = Ancestor.objects.order_by('surname', 'given_name')
    baptism_count = Ancestor.objects.filter(baptism_date__year = 2013).count()
    confirmation_count = Ancestor.objects.filter(confirmation_date__year = 2013).count()
    initiatory_count = Ancestor.objects.filter(initiatory_date__year = 2013).count()
    endowment_count = Ancestor.objects.filter(endowment_date__year = 2013).count()
    sealing_to_parents_count = Ancestor.objects.filter(sealing_to_parents_date__year = 2013).count()
    sealing_to_spouse_count = Ancestor.objects.filter(sealing_to_spouse_date__year = 2013).count()
    ordinance_count = baptism_count + confirmation_count + initiatory_count + endowment_count + sealing_to_parents_count + sealing_to_spouse_count
    template = loader.get_template('ordinances/index.html')
    context = Context({
        'all_ancestors_list': all_ancestors_list,
        'ordinance_count': ordinance_count,
    })
    return HttpResponse(template.render(context))
