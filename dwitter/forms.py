from django import forms
from .models import Dweet

class DweetForm(forms.ModelForm):
    body = forms.CharField(required=True,
    
    # A widget is Django’s representation of an HTML input element. 
    # The widget handles the rendering of the HTML, and the extraction 
    # of data from a GET/POST dictionary that corresponds to the widget.
    widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Dweet something...",
            "class": "textarea is-success is-medium",
        }
    ),
    #label="" to not show "body" label in HTML
    label=""
    )

    class Meta:
        model = Dweet
        exclude = ("user",)