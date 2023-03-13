from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class LoginForm(forms.Form):
    email=forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        # model=get_user_model()
        fields=['email', 'password']


class RegistrationForm(UserCreationForm):
    name=forms.CharField()
    email=forms.EmailField()
    class Meta:
        model=get_user_model()
        fields = ("name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(widget=forms.TextInput(
#         attrs={'class': 'form-control','type':'text','name': 'email'}),
#         label="Email")
#     name = forms.CharField(widget=forms.TextInput(
#         attrs={'class': 'form-control','type':'text','name': 'name'}),
#         label="Name")
#     password1 = forms.CharField(widget=forms.PasswordInput(
#         attrs={'class':'form-control','type':'password', 'name':'password1'}),
#         label="Password")
#     password2 = forms.CharField(widget=forms.PasswordInput(
#         attrs={'class':'form-control','type':'password', 'name': 'password2'}),
#         label="Password (again)")

#     '''added attributes so as to customise for styling, like bootstrap'''
#     class Meta:
#         model = get_user_model()
#         fields = ['Name','email','password1','password2']
#         field_order = ['email','Name','password1','password2']

#     def clean(self):
#         """
#         Verifies that the values entered into the password fields match NOTE : errors here will appear in 'non_field_errors()'
#         """
#         cleaned_data = super(RegistrationForm, self).clean()
#         if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
#             if self.cleaned_data['password1'] != self.cleaned_data['password2']:
#                 raise forms.ValidationError("Passwords don't match. Please try again!")
#         return self.cleaned_data

#     def save(self, commit=True):
#         user = super(RegistrationForm,self).save(commit=False)
#         user.set_password(self.cleaned_data['password1'])
#         if commit:
#             user.save()
#         return user

# #The save(commit=False) tells Django to save the new record, but dont commit it to the database yet

# class LoginForm(forms.Form): # Note: forms.Form NOT forms.ModelForm
#     email = forms.EmailField(widget=forms.TextInput(
#         attrs={'class': 'form-control','type':'text','name': 'email','placeholder':'Email'}), 
#         label='Email')
#     password = forms.CharField(widget=forms.PasswordInput(
#         attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Password'}),
#         label='Password')

#     class Meta:
#         fields = ['email', 'password']