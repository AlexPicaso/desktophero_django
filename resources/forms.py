from django import forms
from django.forms import ModelForm
from resources.models import Asset, BoneGroup, Pose, Preset, AssetForProcessing
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AssetForm(ModelForm):
	category = forms.CharField(max_length=30, help_text="Options: capes, collars, male shirts, female shirts, male torso, female torso, headgear, head, hair, beards, arms, armwear, hands, shields, weapons, wings, items, skirts, legwear, pants, robes, neck, platforms, footwear, shoes")
	mesh = forms.FileField(required=True, help_text="Required. This is the mesh that most people will see while creating their character.")

	class Meta:
		model = Asset
		fields = ['name', 'description', 'category', 'license', 'thumbnail', 'mesh', 'mesh_hires', 'mesh_lowres']

class BoneGroupForm(ModelForm):
	class Meta:
		model = BoneGroup
		fields = ['name', 'description', 'categories', 'thumbnail', 'file']

class PoseForm(ModelForm):
	class Meta:
		model = Pose
		fields = ['name', 'description', 'license', 'thumbnail', 'file']

class PresetForm(ModelForm):
	class Meta:
		model = Preset
		fields = ['name', 'description', 'license', 'thumbnail', 'file']

class RegistrationForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False)
	last_name = forms.CharField(max_length=30, required=False)
	email = forms.EmailField(max_length=254)
	subscribed = forms.BooleanField(initial=True, required=False, help_text="Notify me about DesktopHero updates/news")
	accepted_terms = forms.BooleanField(required=True)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'subscribed', 'password1', 'password2', 'accepted_terms', )

	def clean(self):
		from django.conf import settings
		form_data = self.cleaned_data

class AssetForProcessingForm(ModelForm):
	from editor.views import EditorView

	categories = list(set([(item['asset_category'], item['asset_category'].replace('_', ' ').title()) for item in EditorView.simple_mode_categories()]))
	categories.sort(key=lambda tup: tup[0])
	CATEGORY_CHOICES = (
	    categories
	)

	category = forms.ChoiceField(CATEGORY_CHOICES)
	mesh = forms.FileField(required=True)

	class Meta:
		model = AssetForProcessing
		fields = ["name", "description", "category", "mesh", "license", "rigid", 
				  "attachToGroup", "attachToBone", 
				  "px", "py", "pz", 
				  "rx", "ry", "rz", 
				  "sx", "sy", "sz",]