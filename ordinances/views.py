from django.http import HttpResponse
from django.template import Context, loader

from ordinances.models import Ancestor

def index(request):
    user_ward = request.user.wardmember.ward.name
    all_ancestors_list = Ancestor.objects.filter(ward__name = user_ward).order_by('surname', 'given_name')
    baptism_count = all_ancestors_list.filter(baptism_date__year = 2013).count()
    confirmation_count = all_ancestors_list.filter(confirmation_date__year = 2013).count()
    initiatory_count = all_ancestors_list.filter(initiatory_date__year = 2013).count()
    endowment_count = all_ancestors_list.filter(endowment_date__year = 2013).count()
    sealing_to_parents_count = all_ancestors_list.filter(sealing_to_parents_date__year = 2013).count()
    sealing_to_spouse_count = all_ancestors_list.filter(sealing_to_spouse_date__year = 2013).count()
    ordinance_count = baptism_count + confirmation_count + initiatory_count + endowment_count + sealing_to_parents_count + sealing_to_spouse_count
    template = loader.get_template('ordinances/index.html')
    context = Context({
        'all_ancestors_list': all_ancestors_list,
        'ordinance_count': ordinance_count,
        'ward_name':user_ward
    })
    return HttpResponse(template.render(context))
