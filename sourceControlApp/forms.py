from django.contrib.auth.models import User
from django import forms
from .models import UserGitStore

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UpdateUserGitStoreForm(forms.ModelForm):
    name = forms.CharField(max_length=UserGitStore._meta.get_field('name').max_length)
    repo_description = forms.CharField(max_length=UserGitStore._meta.get_field('repo_description').max_length)

    #def save(self, commit=True):
    #    instance = super(UpdateUserGitStore, self).save(commit=False)

#        if commit:
            #save
 #           instance.save(update_fields=['name', 'repo_description'])
  #      return instance

    class Meta:
        model = UserGitStore
        fields = ('name', 'repo_description',)
