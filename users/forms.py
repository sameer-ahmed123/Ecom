from django import forms
from users.models import Profile,User


class ProfileForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.instance.user.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    username = forms.CharField(
        label='Username', max_length=100, required=True)

    class Meta:
        model = Profile
        fields = ['username', 'bio', 'location', 'birth_date', 'avatar']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
        
    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        username = self.cleaned_data.get('username')

        # Update the User model's username
        if profile.user:
            profile.user.username = username
            if commit:
                profile.user.save()  # Save the User model

        if commit:
            profile.save()  # Save the Profile model

        return profile