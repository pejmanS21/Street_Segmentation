from django.shortcuts import render
from django.http import HttpResponse
from .forms import PostForm
from .models import Post
import glob
import os
from .inc.utility.func import get_pred


# Create your views here.
def ImageView(request):
    if request.method == 'POST':
        post_form = PostForm(data=request.POST, files=request.FILES)

        if post_form.is_valid():
            post_form.save()
            path = os.path.join('./media/images/', str(request.FILES['image']))
            get_pred(path)

    else:
        post_form = PostForm()
    
    return render(request, 'upload.html', {'post_form': post_form})


def Display(request):
    if request.method == 'GET':
        # image = Post.objects.all()
        list_of_files = glob.glob('./media/images/*')
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file = '../.' + latest_file  # for html visualization    '../../media/images/path/to/image'
        
        return render(request, 'display.html', {'image': latest_file})
