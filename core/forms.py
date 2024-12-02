from django import forms

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    asunto = forms.CharField(max_length=200)
    mensaje = forms.CharField(widget=forms.Textarea)
