from django import forms


class MessageForm(forms.Form):
    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea)









