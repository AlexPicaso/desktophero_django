from django import forms
from django.forms import ModelForm
from resources.models import Asset, BoneGroup, Pose, Preset
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AssetForm(ModelForm):
	class Meta:
		model = Asset
		fields = ['name', 'description', 'author', 'category', 'thumbnail', 'mesh', 'mesh_hires', 'mesh_lowres']

class BoneGroupForm(ModelForm):
	class Meta:
		model = BoneGroup
		fields = ['name', 'description', 'author', 'categories', 'thumbnail', 'file']

class PoseForm(ModelForm):
	class Meta:
		model = Pose
		fields = ['name', 'description', 'author', 'category', 'thumbnail', 'file']

class PresetForm(ModelForm):
	class Meta:
		model = Preset
		fields = ['name', 'description', 'author', 'category', 'thumbnail', 'file']

class RegistrationForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False)
	last_name = forms.CharField(max_length=30, required=False)
	email = forms.EmailField(max_length=254)
	subscribed = forms.BooleanField(initial=True, required=False, help_text="Notify me about DesktopHero updates/news")
	accepted_terms = forms.BooleanField(required=True)
	beta_email = forms.EmailField(max_length=254)
	beta_username = forms.CharField(max_length=30)
	beta_password = forms.CharField(max_length=30)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'subscribed', 'password1', 'password2', 'accepted_terms', )

	def clean(self):
		from django.conf import settings
		form_data = self.cleaned_data

		print(form_data['beta_email'])
		print(form_data['beta_username'])
		print(form_data['beta_password'])

		if not (form_data['beta_email'].lower()) in settings.BETA_1 or not (form_data['beta_username'], form_data['beta_password']) in settings.BETA_2:
			self._errors['beta_password'] = ['Beta credentials could not be verified. Check that this is the correct email to use and that the beta username and password are correct.']