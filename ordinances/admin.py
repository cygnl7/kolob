from ordinances.models import Ancestor
from django.contrib import admin

class AncestorAdmin(admin.ModelAdmin):
    list_display = ('submitter',
                    'name',
                    'birth_year',
                    'location',
                    'baptism_date',
                    'confirmation_date',
                    'initiatory_date',
                    'endowment_date',
                    'sealing_to_parents_date',
                    'sealing_to_spouse_date')

    fieldsets = [
        (None, {'fields': ['name', 'birth_year', 'location']}),
        ('Ordinance information', {'fields': ['baptism_date',
                                              'confirmation_date',
                                              'initiatory_date',
                                              'endowment_date',
                                              'sealing_to_parents_date',
                                              'sealing_to_spouse_date']})
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'submitter', None) is None:
            obj.submitter = request.user
        obj.save()

    def queryset(self, request):
        if request.user.is_superuser:
            return Ancestor.objects.all()
        else:
            return Ancestor.objects.filter(submitter=request.user)

admin.site.register(Ancestor, AncestorAdmin)
