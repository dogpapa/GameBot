from django import forms
from .models import UploadFileModel
class UploadFileForm(forms.ModelForm):
    class Meta:
        
        model = UploadFileModel
        fields = ('upload_file',)
        # name = forms.CharField(max_length = 15)
        # files = forms.FileField()
        #files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

# class DocumentForm(forms.Form):
#     docfile = forms.FileField(
#         label='Select a file',
#         help_text='max. 42 megabytes'
#     )
# # class PhotoForm(forms.ModelForm):
#     class Meta:
#         model = Photo
#         field = ('file',)
