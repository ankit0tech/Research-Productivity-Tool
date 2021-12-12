from django.shortcuts import render, get_object_or_404
from subjects.models import Subject, Comment
from accounts.models import UserProfile
from subjects.forms import CreateSubjectForm, CreateCommentForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.core import serializers
from django.http import HttpResponseRedirect


class CreateSubject(LoginRequiredMixin, CreateView):
    form_class= CreateSubjectForm
    model = Subject
    # success_url = reverse_lazy('subjects:details', )

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.created_at = timezone.now()
        self.object.user = self.request.user
        userprofile = UserProfile.objects.get(user=self.object.user.id)
        self.object.department = userprofile.department
        if 'document_file' in self.request.FILES:
                print('document_file is uploaded')
                self.object.document_file = self.request.FILES['document_file']
        self.object.save()
        return super().form_valid(form)

class UpdateSubject(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = CreateSubjectForm
    model = Subject
    success_url = reverse_lazy('subjects:list')

    def test_func(self):
        subject = self.get_object()
        if self.request.user == subject.user:
            return True
        return False

    # def get_pk(self):
    #     self.object = 

class DeleteSubject(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('subjects:list')

class SubjectList(ListView):
    model = Subject

# class SubjectDetail(DetailView):
#     model = Subject

def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    comments = subject.comments

    if request.method == "POST":
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.subject = subject
            user_comment.user = request.user
            user_comment.save()
            return HttpResponseRedirect(reverse('subjects:details', kwargs={'pk': subject.pk}))
    else:
        comment_form = CreateCommentForm

    return render(request, 'subjects/subject_detail.html', {'subject': subject, 'comment_form': comment_form,})


#############################
#    Views for Comment      #
#############################

class CreateComment(LoginRequiredMixin, CreateView):

    form_class = CreateCommentForm
    model = Comment

    def get_success_url(self):
        return reverse_lazy('subjects:details',kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.created_at = timezone.now()
        self.object.user = self.request.user
        self.object.subject = Subject.objects.get(pk=self.kwargs['pk'])
        self.object.save()
        return super().form_valid(form)
    


# def test_func(request):
#     comment = Comment.objects.get(pk=request.pk)
#     if request.user == comment.user:
#         return True
#     return False

# @user_passes_test(test_func)
@login_required
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    subject_pk = comment.subject.pk
    comment.delete()

    return HttpResponseRedirect(reverse_lazy('subjects:details', kwargs={'pk': subject_pk}))
