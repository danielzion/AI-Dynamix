from django.contrib.auth import get_user_model, forms
from .models import Profile
from django import forms as djforms

User = get_user_model()

APPROVAL_CHOICES = (
    ('n', 'Not Requested For Approval'),
    ('p', 'Pending'),
    ('d', 'Declined'),
    ('a', 'Verified')
)

class UserUpdateForm(djforms.ModelForm):
    approval_status = djforms.ChoiceField(
        choices=APPROVAL_CHOICES,
        widget=djforms.HiddenInput(),  # Use HiddenInput widget to hide the field
        initial='n',
    )

    class Meta:
        model = User
        fields = ['username', 'approval_status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

class ProfileUpdateForm(djforms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'housefinder_location', 'bio', 'phone_number', 'mobile_number']
        widgets = {
            'profile_picture': djforms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture is None:  # User cleared the field
            self.instance.profile_picture.delete()  # Delete the existing picture
            self.instance.profile_picture = 'profile_pics/default.jpg'  # Set the default picture path
            return 'profile_pics/default.jpg'
        return profile_picture