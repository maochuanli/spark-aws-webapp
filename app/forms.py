from django import forms


class UploadFileForm(forms.Form):
    # uploadFile = forms.CharField(max_length=50)
    uploadFile = forms.FileField()