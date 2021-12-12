from django import forms
from subjects.models import Subject, Comment
from mptt.forms import TreeNodeChoiceField

class CreateSubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ('title', 'details','github_url', 'document_file')


class CreateCommentForm(forms.ModelForm):

    parent = TreeNodeChoiceField(queryset = Comment.objects.all())

    class Meta:
        model = Comment
        fields = ('text','parent',)
    
    def __init__(self, *args, **kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False
