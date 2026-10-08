from django import forms

from .models import PrivateMessage


class PrivateMessageForm(forms.ModelForm):
    confidential = forms.BooleanField(required=True)

    class Meta:
        model = PrivateMessage
        fields = ['name', 'phone', 'email', 'message_type', 'message', 'confidential']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'placeholder': 'Enter your name'}),
            'phone': forms.TelInput(attrs={'id': 'phone', 'placeholder': 'Enter your phone number'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Enter your email'}),
            'message_type': forms.Select(attrs={'id': 'message_type'}),
            'message': forms.Textarea(attrs={
                'id': 'message',
                'rows': 8,
                'placeholder': 'Write your prayer request or message here...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confidential'].widget.attrs['id'] = 'confidential'
