from django.contrib.auth.forms import UserCreationForm,gettext
from django.contrib.auth.models import User
from django import forms
from django_select2.forms import Select2MultipleWidget
from database import models
from ckeditor.fields import RichTextFormField
from django_select2 import forms as s2forms
from django.forms import FileField, Form, ModelForm


class ActorWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]


class CampaignWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "title__contains",
    ]


class ProducerWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__contains",
    ]


class PartyWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__contains",
    ]


class PCWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__contains",
    ]


class SystemWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__contains",
    ]


class PublisherWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__contains",
    ]


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class SendNotificationForm(forms.ModelForm):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea, required=True)


class ComposeMessageForm(forms.Form):
    sender = forms.ModelChoiceField(queryset=User.objects.all(),
                                    widget= forms.HiddenInput)
    recipients = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=Select2MultipleWidget)
    subject = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)

    def save(self, commit):
        pass


class ActorEditForm(forms.ModelForm):
    class Meta:
        model = models.Actor
        fields = ['name', 'characters', 'link', 'image_url', 'blurb']
        widgets = {
            "characters": PCWidget(
                {'data-width': '300px'}
            ),
        }


class CampaignEditForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = ['title', 'medium', 'gm', 'blurb', 'link', 'produced_by', 'image_url', 'party', 'guests', 'system']
        widgets = {
            "produced_by": ProducerWidget(
                {'data-width': '300px'}
            ),
            "gm": ActorWidget(
                {'data-width': '300px'}
            ),
            "party": PartyWidget(
                {'data-width': '300px'}
            ),
            "guests": PCWidget(
                {'data-width': '300px'}
            ),
            "system": SystemWidget(
                {'data-width': '300px'}
            ),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class EpisodeEditForm(forms.ModelForm):
    class Meta:
        model = models.Episode
        fields = ['title', 'medium', 'blurb', 'link', 'in_campaign', 'runtime', 'airdate', 'image_url', 'ep_count']
        widgets = {
            "airdate": DateInput()
        }


class ProducerEditForm(forms.ModelForm):
    class Meta:
        model = models.Producer
        fields = ['name', 'link', 'campaigns', 'blurb', 'image_url']
        widgets = {
            "campaigns": CampaignWidget(
                {'data-width': '300px'}
            ),
        }


class PublisherEditForm(forms.ModelForm):
    class Meta:
        model = models.Publisher
        fields = ['name', 'link', 'systems', 'blurb', 'image_url']
        widgets = {
            "campaigns": CampaignWidget(
                {'data-width': '300px'}
            ),
            "systems": SystemWidget(
                {'data-width': '300px'}
            ),
        }


class SystemEditForm(forms.ModelForm):
    class Meta:
        model = models.System
        fields = ['name', 'link', 'published_by', 'blurb', 'image_url', 'campaigns']
        widgets = {
            "campaigns": CampaignWidget(
                {'data-width': '300px'}
            ),
            "published_by": PublisherWidget(
                {'data-width': '300px'}
            ),
        }


class PCEditForm(forms.ModelForm):
    class Meta:
        model = models.PC
        fields = ['name', 'played_by', 'fandom_page', 'image_url', 'member_of', 'guest_of', 'blurb']
        widgets = {
            "played_by": ActorWidget(
                {'data-width': '300px'}
            ),
            "member_of": PartyWidget(
                {'data-width': '300px'}
            ),
            "guest_of": CampaignWidget(
                {'data-width': '300px'}
            ),
        }


class UploadForm(Form):
    episodes_file = FileField()

class PartyEditForm(forms.ModelForm):
    class Meta:
        model = models.Party
        fields = ['name', 'members', 'fandom_page', 'image_url', 'blurb']
        widgets = {
            "members": PCWidget(
                {'data-width': '300px'}
            ),
        }


class AddActorForm(forms.ModelForm):
    class Meta:
        model = models.Actor
        fields = ["name", "characters", "image_url", "link", "blurb"]
        widgets = {
            "characters": PCWidget(
                {'data-width': '300px'}
            ),
        }





class AddEpisodeForm(forms.ModelForm):
    class Meta:
        model = models.Episode
        fields = ["title", "runtime", "airdate", "medium", "in_campaign", "image_url", "link", "blurb", "ep_count"]
        widgets = {
            "in_campaign": CampaignWidget(
                {'data-width': '300px'}
            ),
            "airdate": DateInput
        }


class AddCampaignForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = ['title', 'medium', 'gm', 'blurb', 'link', 'image_url', 'party', 'guests', 'system']
        widgets = {
            "gm": ActorWidget(
                {'data-width': '300px'}
            ),
            "party": PartyWidget(
                {'data-width': '300px'}
            ),
            "guests": PCWidget(
                {'data-width': '300px'}
            ),
            "system": SystemWidget(
                {'data-width': '300px'}
            ),
        }


class AddProducerForm(forms.ModelForm):
    class Meta:
        model = models.Producer
        exclude = ['followers']
        widgets = {
            "campaigns": CampaignWidget(
                {'data-width': '300px'}
            )
        }


class AddSystemForm(forms.ModelForm):
    class Meta:
        model = models.System
        exclude = []
        widgets = {
            "campaigns": CampaignWidget(
                {'data-width': '300px'}
            ),
            "published_by": PublisherWidget(
                {'data-width': '300px'}
            )
        }


class AddPartyForm(forms.ModelForm):
    class Meta:
        model = models.Party
        fields = ["name", "blurb", "members", "fandom_page", "image_url"]
        widgets = {
            "members": PCWidget(
                {'data-width': '300px'}
            ),
        }


class AddPCForm(forms.ModelForm):
    class Meta:
        model = models.PC
        fields = ["name", "played_by", "fandom_page", "image_url", "guest_of", "blurb"]
        widgets = {
            "played_by": ActorWidget(
                {'data-width': '300px'}
            ),
            "guest_of": CampaignWidget(
                {'data-width': '300px'}
            ),
        }


class AddGuestPCForm(forms.ModelForm):
    class Meta:
        model = models.PC
        exclude = []
        widgets = {
        }


class AddPublisherForm(forms.ModelForm):
    class Meta:
        model = models.Publisher
        exclude = []
        widgets = {
            "systems": SystemWidget(
                {'data-width': '300px'}
            )
        }
