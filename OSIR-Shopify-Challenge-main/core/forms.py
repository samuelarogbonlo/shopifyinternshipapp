from django.forms import ModelForm
from core.models import ImageItem, User

class ImageForm(ModelForm):
    class Meta:
        model = ImageItem
        fields = ['name','description','image','public']

class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['email','password']