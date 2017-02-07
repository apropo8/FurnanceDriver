from django.db import models
from django.forms import ModelForm


class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = ['savefurnacepower', 'saveweatherpower', 'pub_date']


