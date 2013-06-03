from django.http import HttpResponse
from django.db.models import Sum
from django.template import Context, loader

from ordinances.models import Ancestor, Ward

ALL_WARDS = 'Lehi Utah South Celestial Stake'

def index(request):
    # Default to all wards
    user_ward_name = ALL_WARDS
    if ('ward' in request.REQUEST):
        # Use the request's ward if available
        user_ward_name = request.REQUEST['ward']
    else:
        # Default to the ward the user is in
        user_ward_name = request.user.ward.name

    # See if we have a valid ward name, ALL_WARDS is always valid
    ward_list = Ward.objects.all()
    if (user_ward_name != ALL_WARDS):
        if (ward_list.filter(name = user_ward_name).count() < 1):
            user_ward_name = ALL_WARDS

    # Now figure out goals and ancestor list
    member_goal = 1 # If we somehow don't get a goal, avoid using 0 here so we don't divide by 0
    ordinance_goal = 1 # Same thing as ^
    if (user_ward_name == ALL_WARDS):
        all_ancestors_list = Ancestor.objects.order_by('surname', 'given_name')
        # We have to calculate the goals as an aggregate of all wards
        member_goal = Ward.objects.aggregate(Sum('member_goal'))['member_goal__sum']
        ordinance_goal = Ward.objects.aggregate(Sum('ordinance_goal'))['ordinance_goal__sum']
    else:
        all_ancestors_list = Ancestor.objects.filter(ward__name = user_ward_name).order_by('surname', 'given_name')
        myward = ward_list.filter(name = user_ward_name)
        if (myward.count() > 0):
            member_goal = myward[0].member_goal
            ordinance_goal= myward[0].ordinance_goal

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
        'ward_name': user_ward_name,
        'member_goal': member_goal,
        'ordinance_goal': ordinance_goal,
        'ward_list': ward_list,
        'all_wards_name': ALL_WARDS
    })
    return HttpResponse(template.render(context))
