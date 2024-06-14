from django.shortcuts import render, redirect
from .forms import ProfilePictureForm
from .models import ProfilePicture
from .tasks import enhance_profile_picture

def upload_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            profile_picture = form.save()
            enhance_profile_picture.delay(profile_picture.id)
            return redirect('result', profile_picture.id)
    else:
        form = ProfilePictureForm()
    return render(request, 'upload.html', {'form': form})

def result(request, picture_id):
    picture = ProfilePicture.objects.get(id=picture_id)
    return render(request, 'result.html', {'picture': picture})