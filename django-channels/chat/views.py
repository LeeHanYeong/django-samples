from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from members.models import User


@login_required
def index(request):
    users = User.objects.exclude(id=request.user.id)
    context = {
        'users': users,
    }
    return render(request, 'chat/index.html', context)


@login_required
def room(request, to_user_id):
    history = request.user.get_history(to_user_id)
    context = {
        'history': history,
        'to_user_id': to_user_id,
    }
    return render(request, 'chat/room.html', context)
