from django import forms


class OrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=25)
    comment = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'placeholder': 'Add comment'}))

