from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import SermonForm
from .models import Sermon


def can_add_sermons(user):
    return bool(
        user.is_authenticated
        and user.is_active
        and user.is_staff
        and (user.is_superuser or user.has_perm('sermons.add_sermon'))
    )


@login_required
@login_required
def sermon_list(request):
    authorized = can_add_sermons(request.user)

    if request.method == 'POST':
        if not authorized:
            return HttpResponseForbidden('You are not authorized to add sermons.')

        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sermon added successfully.')
            return redirect('sermons')
    else:
        form = SermonForm()

    return render(request, 'Sermon.html', {
        'can_add_sermons': authorized,
        'form': form,
        'sermons': Sermon.objects.all(),
    })
