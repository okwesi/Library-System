from django import forms

from request.models import SchoolRequests


class SchoolRequestForm(forms.ModelForm):
    # quantity = forms.IntegerField()

    class  Meta:
        model = SchoolRequests
        fields = ("quantity",)
    
    
    
    
    