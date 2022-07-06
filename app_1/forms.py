from django.forms import ModelForm, forms
from .models import Predmeti, Korisnik
from django.contrib.auth.forms import UserCreationForm


class PredmetiForm(ModelForm):
  class Meta:
    model = Predmeti
    fields = ['name', 'kod', 'program', 'ects', 'sem_red', 'sem_izv', 'izborni']
    exclude = ['nositelj']


class NositeljForm(ModelForm):
  class Meta:
    model = Predmeti
    fields = ['nositelj']


class NewUserForm(UserCreationForm):
  class Meta:
    model = Korisnik
    fields = ["username", "email", "password1", "password2", "role", "status"]

  def save(self, commit=True):
    user = super(NewUserForm, self).save(commit=False)
    user.role = self.cleaned_data['role']
    user.status = self.cleaned_data['status']
    if commit:
      user.save()
    return user

class EditUserForm(ModelForm):
  class Meta:
    model = Korisnik
    fields = ['username', 'email', 'role', 'status']
