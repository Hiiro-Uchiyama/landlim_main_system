from django import forms
from post.models import Post
from .widgets import SuggestWidgetForeign, SuggestWidgetText
from django.urls import reverse_lazy

## How can browser default suggestions be turned off?
class SearchPostKeywordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "

    q = forms.CharField(label="キーワード検索",
                        widget=SuggestWidgetText(
                            attrs={'data-url': reverse_lazy('search_post:api_posts_get'),
                                   'class': 'form-control form-size',
                                   'placeholder':'タイトル検索',
                                   'name': 'q'})
                        )

class SearchPostOptionForm(forms.Form):
    SORT_METHOD_OPTIONS = (('sort_new', '新しい順'), ('sort_old', '古い順'))
    sort_method = forms.ChoiceField(label="ソート", choices=SORT_METHOD_OPTIONS)

class SearchPostTagForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
    q_tag = forms.CharField(label="タグ検索",
                            widget=SuggestWidgetText(
                            attrs={'data-url': reverse_lazy('search_post:api_tags_get'),
                                   'class': 'form-control form-size',
                                   'placeholder': 'タグ検索',
                                   'name': 'q_tag'})
                            )

class SearchPostCouForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "

    q_cou = forms.CharField(label="国検索",
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_cou_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': '国検索',
                                       'name': 'q_cou'})
                            )

class SearchPostPreForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "

    q_pre = forms.CharField(label="県検索",
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_pre_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': '県検索',
                                       'name': 'q_pre'})
                            )

class SearchPostCitForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "

    q_cit = forms.CharField(label="市検索",
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_cit_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': '市検索',
                                       'name': 'q_cit'})
                            )

## Make selections about feelings.
class SearchPostEmoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "

    q_emo = forms.CharField(label="感情検索",
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_emo_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': '感情検索',
                                       'name': 'q_emo'})
                            )

## Make selections about feelings.
class SearchPostRefineForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "

    SORT_METHOD_OPTIONS = (('sort_new', '新しい順'), ('sort_old', '古い順'))
    sort_method = forms.ChoiceField(label="ソート", choices=SORT_METHOD_OPTIONS)
    sort_method.widget.attrs.update({'class': 'custom-select'})
    q = forms.CharField(label="キーワード", required=False,
                        widget=SuggestWidgetText(
                            attrs={'data-url': reverse_lazy('search_post:api_posts_get'),
                                   'class': 'form-control form-size',
                                   'placeholder': 'タイトル検索',
                                   'name': 'q'})
                        )
    q_tag = forms.CharField(label="タグ",required=False,
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_tags_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': 'タグ検索',
                                       'name': 'q_tag'})
                            )
    ## This is an early and error-prone area.
    country_choices = [(posts[0], posts[0]) for posts in list(Post.objects.distinct().values_list('country'))]
    q_cou = forms.ChoiceField(label="国", choices=country_choices)
    q_cou.widget.attrs.update({'class': 'custom-select'})
    q_pre = forms.CharField(label="県", required=False,
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_pre_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': '県検索',
                                       'name': 'q_pre'})
                            )
    q_cit = forms.CharField(label="市", required=False,
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_cit_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': '市検索',
                                       'name': 'q_cit'})
                            )
    ## This is an early and error-prone area.
    emotion_choices = [(posts[0], posts[0]) for posts in list(Post.objects.distinct().values_list('emotion'))]
    q_emo = forms.ChoiceField(label="感情", choices=emotion_choices)
    q_emo.widget.attrs.update({'class': 'custom-select'})
