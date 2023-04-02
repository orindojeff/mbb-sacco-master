from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model, logout
from django.forms import forms, ModelForm, ChoiceField
from django.utils.translation import gettext_lazy as _
from accounts.mixins import StyleFormMixin
from accounts.models import Profile, Feedback

User = get_user_model()

USER_TYPES = [
    ('RD', 'Rider'),
    ('CM', 'Customer'),
]


class UserAdminChangeForm(ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admins
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password', 'is_active']

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.upper()

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RegistrationForm(UserCreationForm):
    type = ChoiceField(choices=USER_TYPES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['name', 'email', 'username', 'type', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.upper()


class AdminRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['name', 'email', 'username', 'type', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.upper()


class UserAuthenticationForm(AuthenticationForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.upper()

    def clean(self):
        super().clean()
        if self.user_cache is not None and self.user_cache.is_staff:
            logout(self.request)
            raise forms.ValidationError('Invalid username or password for customer login', code='invalid login')
        elif self.user_cache.is_archived:
            logout(self.request)
            raise forms.ValidationError('Sorry your account is archived', code='invalid login')

        elif not self.user_cache.is_verified:
            logout(self.request)
            raise forms.ValidationError(
                'Your account is inactive. Please wait for account approval', code='invalid login'
            )


class ProfileModelForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'phone_number']


class UserModelForm(StyleFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']


FEEDBACK_TYPES = [
    ('CST_SMR', _('Send to Sales Manager')),
    ('CST_FMR', _('Send to Finance Manager')),
]


class FeedbackModelForm(StyleFormMixin, ModelForm):
    type = ChoiceField(choices=FEEDBACK_TYPES)

    class Meta:
        model = Feedback
        fields = ['type', 'content']


class StaffFeedbackModelForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Feedback
        fields = ['content']
