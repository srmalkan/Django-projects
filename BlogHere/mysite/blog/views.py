from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import post,Comment
from .forms import EmailForm,CommentForm,addPostForm,updateForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.urls import reverse,reverse_lazy
from django.utils import timezone
from django.views.generic import View,ListView, DetailView, CreateView, UpdateView, DeleteView,FormView
from django.utils.decorators import method_decorator
# from django.urls import reverse
# Create your views here.

class postList(ListView):
    # model = post
    # queryset = post.objects.filter(status='published')
    context_object_name = 'posts'
    paginate_by  = 4
    template_name='blog/post/list.html'

    def get_queryset(self):
        posts = post.objects.filter(status='published')
        if 'tag_slug' in self.kwargs :
            tag_slug = self.kwargs['tag_slug']
            tag = None
            if tag_slug:
                tag = get_object_or_404(Tag, slug=tag_slug)
                posts = posts.filter(tags__in=[tag])
        return posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.all()
        context['page']="page",
        context['tag']=tag
        return context

'''
function based view
def post_list(request,tag_slug=None):
    object_list = post.objects.filter(status='published')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5) # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts':posts,'page':page,'tag':tag})
'''

class postDetail(DetailView):
    model = post
    template_name='blog/post/detail.html'
    context_object_name = "post"
    form = CommentForm()

    def get_object(self):
        return super().get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # postreq = 
        comments = self.get_object().comments.filter(active=True)
        context["comment_form"] = self.form
        context['comments']=comments
        return context
    
    def post(self,request,*args,**kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = self.get_object()
            comment.save()
            return redirect(reverse("blog:post_detail", kwargs={"pk":self.get_object().pk}))
'''
def post_detail(request,id):
    postretv = get_object_or_404(post,id=id)
    comments = postretv.comments.filter(active=True)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = postretv
            comment.save()
    comment_form = CommentForm()
    return render(request,'blog/post/detail.html',{'post':postretv,'comment_form':comment_form,'comments':comments})
'''

class postshareFormView(FormView):
    template_name = "blog/post/share.html"
    form_class = EmailForm

    def form_valid(self,form):
        postreq = get_object_or_404(post,id=self.kwargs['post_id'],status='published')
        cd = form.cleaned_data
        post_url = self.request.build_absolute_uri(postreq.get_absolute_url())
        subject = '{} is recommended to you by {}'.format(postreq.title,cd['name'])
        message = 'Read {},\n comment:\n {}'.format(post_url,cd['comments'])
        send_mail(subject,message,'pythondjango99@gmail.com',[cd['to']])
        return redirect(postreq)


def post_share(request, post_id):
    postreq = get_object_or_404(post,id=post_id,status='published')
    sent = False
    
    if request.method=='POST':
        form = EmailForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(postreq.get_absolute_url())
            subject = '{} is recommended to you by {}'.format(postreq.title,cd['name'])
            message = 'Read {},\n comment:\n {}'.format(post_url,cd['comments'])
            send_mail(subject,message,'pythondjango99@gmail.com',[cd['to']])
            sent = True

    else:
        form = EmailForm()
    return render(request,'blog/post/share.html',{'post':postreq,'form':form,'sent':sent})

@method_decorator(login_required, name='dispatch')
class postCreateView(CreateView):
    model = post
    template_name = "blog/post/addPost.html" 
    form_class = addPostForm

    def form_valid(self, form):
        print("something")
        newpost = form.save(commit=False)
        newpost.author = self.request.user
        newpost.slug = slugify(newpost.title)
        newpost.save()
        return redirect(reverse('account:dashboard'))

'''
@login_required
def addPost(request):
    if request.method == 'POST':
        form = addPostForm(request.POST)
        if form.is_valid :
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.slug = slugify(newpost.title)
            newpost.save()
            return 
    else:        
        form = addPostForm()
    return render(request,'blog/post/addPost.html',{'form':form})
'''
@method_decorator(login_required, name='dispatch')
class postUpdateView(UpdateView):
    model = post
    template_name = "blog/post/update.html"
    form_class = addPostForm

    def form_valid(self, form):
        postretv = get_object_or_404(post,pk=self.kwargs['pk'])
        cd = form.cleaned_data
        postretv.title = cd['title']
        postretv.slug = slugify(postretv.title)
        postretv.body = cd['body']
        postretv.save()
        return redirect(reverse("blog:update_post", kwargs={"pk":postretv.pk}))

'''
@login_required
def updatePost(request,pk):
    postretv = get_object_or_404(post,pk=pk)
    tags=''
    for tag in postretv.tags.all():
        tags += str(tag)+','
    if request.method == 'POST':
        form = updateForm(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
            postretv.title = cd['title']
            postretv.slug = slugify(postretv.title)
            postretv.body = cd['body']
            postretv.save()

    form = updateForm(initial={'title':postretv.title,'body':postretv.body,'tags':tags})
    return render(request,'blog/post/update.html',{'form':form,'post':postretv})
''' 
@method_decorator(login_required, name='dispatch')
class publishView(View):
    def get(self, request, *args, **kwargs):
        postretv = get_object_or_404(post,pk=kwargs['pk'])
        return render(request,'blog/post/publish.html',{'post':postretv})

    def post(self, request, *args, **kwargs):
        postretv = get_object_or_404(post,pk=kwargs['pk'])
        postretv.status = 'published'
        postretv.publish = timezone.now()
        postretv.save()
        print(postretv.status)
        return redirect(postretv)

'''
@login_required
def publishPost(request,pk):
    postretv = get_object_or_404(post,pk=pk)
    if request.method == 'POST':
        postretv.status = 'published'
        postretv.publish = timezone.now()
        postretv.save()
        print(postretv.status)
        return redirect(postretv)
    return render(request,'blog/post/publish.html',{'post':postretv})
'''
@method_decorator(login_required, name='dispatch')
class postDeleteView(DeleteView):
    model = post
    template_name = "blog/post/delete.html"
    success_url = reverse_lazy('account:dashboard')

'''
@login_required
def deletePost(request,pk):
    postretv = get_object_or_404(post,pk=pk)
    request
    if request.method == 'POST':
        postretv.delete()
        return redirect('account:dashboard')
    return render(request,'blog/post/delete.html',{'post':postretv})
'''