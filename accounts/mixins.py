import csv

from django.conf import settings
from django.contrib import messages
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from accounts.models import Profile

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ProfileMixin:
    """
    mixin for getting profile object for logged in user.
    """
    user_form = None

    def get_context_data(self, **kwargs):
        context = super(ProfileMixin, self).get_context_data(**kwargs)
        context['user_form'] = self.user_form(instance=self.request.user)
        return context

    def get_queryset(self):  # noqa
        return Profile.objects.all()

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        user_form = self.user_form(self.request.POST, instance=self.request.user)
        user_form.save()
        return super(ProfileMixin, self).form_valid(form)


class InfoMessageMixin:
    """
    Add a info message on a class.
    """

    info_message = ""

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        info_message = self.info_message
        if info_message:
            messages.info(self.request, info_message)
        return response


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            _ = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class CacheMixin:
    cache_timeout = CACHE_TTL

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super(StyleFormMixin, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if str(type(visible.field)) == "<class 'django.forms.fields.DateTimeField'>":
                visible.field.widget.attrs['class'] = 'datetimepicker'
            elif str(type(visible.field)) == "<class 'django.forms.fields.DateField'>":
                visible.field.widget.attrs['class'] = 'datepicker'
            elif str(type(visible.field)) == "<class 'django.forms.fields.TypedChoiceField'>":
                visible.field.widget.attrs['class'] = 'form-select'
            elif str(type(visible.field)) == "<class 'django.forms.models.ModelChoiceField'>":
                visible.field.widget.attrs['class'] = 'form-select'
            elif str(type(visible.field)) == "<class 'django_countries.fields.LazyTypedChoiceField'>":
                visible.field.widget.attrs['class'] = 'form-select'
