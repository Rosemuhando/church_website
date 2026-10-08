from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import PrivateMessageForm


def contact_page(request):
    return render(request, 'Contact.html', {'form': PrivateMessageForm()})


@require_POST
def private_message(request):
    form = PrivateMessageForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your confidential message has been received.')
        return redirect(f"{reverse('contact')}#private-message")

    return render(request, 'Contact.html', {'form': form})
