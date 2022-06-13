from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, reverse
from mboard.models import Thread
from .forms import PostForm, ThreadPostForm
from PIL import Image
from io import BytesIO


def list_threads(request):
    if request.method == 'POST' and 'threadnum' in request.POST:  # a reply to an existing thread
        return get_thread(request, request.POST.get('threadnum'))  # 'threadnum' gets set with JS
    if request.method == 'POST':  # otherwise create a new thread
        form = ThreadPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_thread = form.save(commit=False)
            if form.cleaned_data['image']:
                new_thread.thumbnail = make_thumbnail(form.cleaned_data['image'])
            new_thread.save()
            return redirect(reverse(get_thread, kwargs={'thread_id': new_thread.id}))
    return display_threads_list(request)  # on GET request and also when 'form' IS NOT valid


def display_threads_list(request):
    if request.POST:  # was POST but form wasn't valid (keep the form content and display errors)
        form = ThreadPostForm(data=request.POST, files=request.FILES)
    else:  # GET goes here
        form = ThreadPostForm
    threads = Thread.objects.order_by('-post__date')  # threads with new posts first TODO
    threads_dict = {}
    posts_ids = []
    for thread in threads:
        posts_ids.append(thread.pk)
        for post in thread.post_set.all(): posts_ids.append(post.pk)  # list of all posts' ids in the thread
        posts_count = thread.post_set.all().count()
        if posts_count > 4:
            posts_to_display = thread.post_set.all()[posts_count - 4:]
        else:
            posts_to_display = thread.post_set.all()[0:]
        threads_dict[thread] = posts_to_display  # output only the last 0-4 posts of every thread
    context = {'threads': threads_dict, 'form': form, 'posts_ids': posts_ids}
    return render(request, 'list_threads.html', context)


def get_thread(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    posts_ids = [thread.pk]  # list of all posts' ids (+OP post.id) in the thread,
    for post in thread.post_set.all(): posts_ids.append(post.pk)  # for use in the template tag
    gotobottom = False
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            if form.cleaned_data['image']:
                new_post.thumbnail = make_thumbnail(form.files['image'])
            new_post.thread_id = thread_id
            new_post.save()
            return redirect(reverse(get_thread, kwargs={'thread_id': thread_id}) + f'#id{new_post.id}')
        else:
            gotobottom = True
    else:
        form = PostForm
    return render(request, 'thread.html',
                  context={'thread': thread, 'form': form, 'posts_ids': posts_ids, 'gotobottom': gotobottom})


def make_thumbnail(inmemory_image):
    image = Image.open(inmemory_image)
    # image.thumbnail(size=(150, 200))
    image.thumbnail(size=(200, 220))
    output = BytesIO()
    image.save(output, quality=85, format=image.format)
    thumb = InMemoryUploadedFile(output, 'ImageField', 'thumb_' + inmemory_image.name, 'image/jpeg', None, None)
    return thumb


def testview(request):
    return render(request=request, template_name='test.html')
