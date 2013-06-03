from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ordinances.models import Ancestor, Ward
from auth.models import WardUser

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
            obj.ward = request.user.ward
        obj.save()

    def queryset(self, request):
        if request.user.is_superuser:
            return Ancestor.objects.order_by('surname', 'given_name')
        else:
            return Ancestor.objects.filter(submitter=request.user).order_by('surname', 'given_name')

class WardUserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'email',
                    'ward',
                    'is_staff',
                    'is_superuser'
                    )
    list_editable = ('first_name', 'last_name', 'email', 'ward')
    list_filter = ('is_staff', 'is_superuser', 'ward__name')
    search_fields = ['username', 'first_name', 'last_name', 'email', 'ward__name']

class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_goal', 'ordinance_goal'
                    )
    list_editable = ('member_goal', 'ordinance_goal')

admin.site.register(Ancestor, AncestorAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(WardUser, WardUserAdmin)
