from django import forms
from .models import Post, PostImage, Comment, UserChoiceEmotionForPost, VideoPost
from django.core.files.uploadedfile import UploadedFile
from .validator import FileSizeValidator

## I wish I could narrow it down by distance from me.
## It should be possible to refer to it from other submission forms and so on.
class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'tags', 'web_link', 'twitter_link', 'instagram_link',
                  'access_level', 'pin_x', 'pin_y', 'provisional', 'emotion')
        ## Pulchick's Emotions
        label = ['Emotional']
        CHOICE = [
            ('1', '喜び'),
            ('2', '信頼'),
            ('3', '恐れ'),
            ('4', '驚き'),
            ('5', '悲しみ'),
            ('6', '嫌悪'),
            ('7', '怒り'),
            ('8', '期待'),
            ('9', '平穏'),
            ('10', '容認'),
            ('11', '不安'),
            ('12', '放心'),
            ('13', '哀愁'),
            ('14', 'うんざり'),
            ('15', '苛立ち'),
            ('16', '関心')]
        emotion = forms.ChoiceField(
            label=label[0],
            required=True,
            disabled=False,
            initial=['1'],
            choices=CHOICE,
            widget=forms.Select(attrs={
                'id': 'emotion',}))
        ## access level
        label = ['Access_Level']
        CHOICE = [
            ('1', 'public'),
            ('2', 'private'),
            ('3', 'friend')]
        emotion = forms.ChoiceField(
            label=label[0],
            required=True,
            disabled=False,
            initial=['1'],
            choices=CHOICE,
            widget=forms.Select(attrs={
                'id': 'access_level',}))
        ## access level
        label = ['Provisional']
        CHOICE = [
            ('1', 'No'),
            ('2', 'Yes')]
        emotion = forms.ChoiceField(
            label=label[0],
            required=True,
            disabled=False,
            initial=['1'],
            choices=CHOICE,
            widget=forms.Select(attrs={
                'id': 'provisional',}))

    def __init__(self, *args, **kwargs):
        super(PostAddForm, self).__init__(*args, **kwargs)

class SaveLocationAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'access_level', 'pin_x', 'pin_y', 'provisional')
        label = ['Emotional']
        CHOICE = [
            ('1', '喜び'),
            ('2', '信頼'),
            ('3', '恐れ'),
            ('4', '驚き'),
            ('5', '悲しみ'),
            ('6', '嫌悪'),
            ('7', '怒り'),
            ('8', '期待'),
            ('9', '平穏'),
            ('10', '容認'),
            ('11', '不安'),
            ('12', '放心'),
            ('13', '哀愁'),
            ('14', 'うんざり'),
            ('15', '苛立ち'),
            ('16', '関心')]
        emotion = forms.ChoiceField(
            label=label[0],
            required=True,
            disabled=False,
            initial=['1'],
            choices=CHOICE,
            widget=forms.Select(attrs={
                'id': 'emotion',}))
        ## access level
        label = ['Access_Level']
        CHOICE = [
            ('1', 'public'),
            ('2', 'private'),
            ('3', 'friend')]
        emotion = forms.ChoiceField(
            label=label[0],
            required=True,
            disabled=False,
            initial=['2'],
            choices=CHOICE,
            widget=forms.Select(attrs={
                'id': 'access_level', }))
        ## access level
        label = ['Provisional']
        CHOICE = [
            ('1', 'No'),
            ('2', 'Yes')]
        emotion = forms.ChoiceField(
            label=label[0],
            required=True,
            disabled=False,
            initial=['2'],
            choices=CHOICE,
            widget=forms.Select(attrs={
                'id': 'provisional', }))
    def __init__(self, *args, **kwargs):
        super(SaveLocationAddForm, self).__init__(*args, **kwargs)

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)
        validators = [FileSizeValidator(val=1, byte_type="gb")]

    def __init__(self, i, *args, **kwargs):
        super(PostImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()
        self.fields['image'].widget.attrs = {'name':'image'+str(i), 'style':'display:none;', 'id':'file_'+str(i) , 'onchange': 'fileget(this,\''+str(i)+'\');',}

    @property
    def thumbnail_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.thumbnail['600x600'].url

## Do you need more information about the comments?
## I think you're being a bit shallow.
## Is this also made with Ajax, in a manner of speaking?
class CommentAddForm(forms.ModelForm):
   class Meta:
        model = Comment
        fields = ('comment_text',)

class VideoAddForm(forms.ModelForm):
    class Meta:
        model = VideoPost
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VideoAddForm, self).__init__(*args, **kwargs)

class AddEmotionForm(forms.ModelForm):
    class Meta:
        model = UserChoiceEmotionForPost
        fields = ('def_emotion', 'def_emotion_color')