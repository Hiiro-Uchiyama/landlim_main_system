from django import forms
from .widgets import SuggestWidgetForeign, SuggestWidgetText
from django.urls import reverse_lazy

## Make selections about feelings.
class SearchBlogRefineForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "

    SORT_METHOD_OPTIONS = (('sort_new', '新しい順'), ('sort_old', '古い順'))
    sort_method = forms.ChoiceField(label="ソート", choices=SORT_METHOD_OPTIONS)
    sort_method.widget.attrs.update({'class': 'custom-select'})

    q = forms.CharField(label="キーワード検索", required=False,
                        widget=SuggestWidgetText(
                            attrs={'data-url': reverse_lazy('search_post:api_posts_get'),
                                   'class': 'form-control form-size',
                                   'placeholder': 'タイトル検索',
                                   'name': 'q'})
                        )
    q_tag = forms.CharField(label="タグ検索", required=False,
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_tags_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': 'タグ検索',
                                       'name': 'q_tag'})
                            )
    q_cou = forms.CharField(label="国検索", required=False,
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_cou_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': '国検索',
                                       'name': 'q_cou'})
                            )
    q_pre = forms.CharField(label="県検索", required=False,
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_pre_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': '県検索',
                                       'name': 'q_pre'})
                            )
    q_cit = forms.CharField(label="市検索", required=False,
                            widget=SuggestWidgetText(
                                attrs={'data-url': reverse_lazy('search_post:api_cit_get'),
                                       'class': 'form-control form-size',
                                       'placeholder': '市検索',
                                       'name': 'q_cit'})
                            )