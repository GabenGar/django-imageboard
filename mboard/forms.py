from django import forms
from django.core.exceptions import ValidationError
from mboard.models import Post, Thread


class PostForm(forms.ModelForm):
    text = forms.CharField(required=True, error_messages={'required': 'Введите текст сообщения'},
                           max_length=4000, min_length=1, widget=forms.Textarea(attrs={'accept': 'image'}))
    poster = forms.CharField(required=False, empty_value='Анон', widget=forms.TextInput(attrs={'placeholder': 'Анон'}))
    threadnum = forms.IntegerField(required=False)
    image = forms.ImageField(required=False)

    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            if image.size > 1 * 1024 * 1024:
                raise ValidationError('> 1 МБ')
            return image

    class Meta:
        model = Post
        fields = ['poster', 'text', 'threadnum', 'image']


class ThreadPostForm(PostForm):
    image = forms.ImageField(required=True)

    class Meta:
        model = Thread
        fields = ['text', 'title', 'threadnum', 'image']
