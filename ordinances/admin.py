from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from ordinances.models import Ancestor, Ward, WardMember

# Inline admin descriptor for wardmember
class WardMemberInline(admin.StackedInline):
    model = WardMember
    can_delete = False
    verbose_name_plural = 'ward member'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (WardMemberInline, )
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'ward', # Calls ward method below
                    'email',
                    'is_staff',
                    'is_superuser')

    def ward(self, instance):
        return instance.wardmember.ward.name.encode('utf8')

class AncestorAdmin(admin.ModelAdmin):
    list_display = ('submitter',
                    'ward',
                    'surname',
                    'given_name',
                    'birth_year',
                    'location',
                    'baptism_date',
                    'confirmation_date',
                    'initiatory_date',
                    'endowment_date',
                    'sealing_to_spouse_date',
                    'sealing_to_parents_date')
    list_display_links = ('surname',
			  'given_name',
			  'birth_year',
			  'location',
			  'baptism_date',
			  'confirmation_date',
			  'initiatory_date',
			  'endowment_date',
			  'sealing_to_spouse_date',
			  'sealing_to_parents_date')

    fieldsets = [
        (None, {'fields': ['given_name', 'surname', 'birth_year', 'location']}),
        ('Ordinance information', {'fields': ['baptism_date',
                                              'confirmation_date',
                                              'initiatory_date',
                                              'endowment_date',
                                              'sealing_to_spouse_date',
                                              'sealing_to_parents_date']})
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'submitter', None) is None:
            obj.submitter = request.user
            obj.ward = Ward.objects.all()[0] # TODO: get the user's ward
        obj.save()

    def queryset(self, request):
        if request.user.is_superuser:
            return Ancestor.objects.order_by('surname', 'given_name')
        else:
            return Ancestor.objects.filter(submitter=request.user).order_by('surname', 'given_name')

admin.site.register(Ancestor, AncestorAdmin)
admin.site.register(Ward)

# Re-register UserAdmin to get WardMember customizations
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
