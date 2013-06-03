from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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
    list_editable = ('surname',
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
        obj.submitter = request.user
        obj.ward = request.user.ward
        obj.save()

    def queryset(self, request):
        if request.user.is_superuser:
            return Ancestor.objects.order_by('surname', 'given_name')
        else:
            return Ancestor.objects.filter(submitter=request.user).order_by('surname', 'given_name')


# Thank you https://groups.google.com/forum/?fromgroups#!topic/django-users/kOVEy9zYn5c !
class WardUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = WardUser

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            # Not sure why UserCreationForm doesn't do this in the first place,
            # or at least test to see if _meta.model is there and if not use User...
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class WardUserChangeForm(UserChangeForm):
    class Meta:
        model = WardUser


class WardUserAdmin(UserAdmin):
    form = WardUserChangeForm
    add_form = WardUserCreationForm
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
    # A little hacky; put the ward in the first section
    fieldsets = UserAdmin.fieldsets
    fieldsets[0][1]['fields'] = UserAdmin.fieldsets[0][1]['fields'] + ('ward',)
    add_fieldsets = UserAdmin.add_fieldsets
    add_fieldsets[0][1]['fields'] = UserAdmin.add_fieldsets[0][1]['fields'] + ('ward',)



class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_goal', 'ordinance_goal'
                    )
    list_editable = ('member_goal', 'ordinance_goal')

admin.site.register(Ancestor, AncestorAdmin)
admin.site.register(WardUser, WardUserAdmin)
admin.site.register(Ward, WardAdmin)
