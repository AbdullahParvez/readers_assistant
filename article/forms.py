'''Form for article app'''
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = [
            'title',
            'content',
        ]

    title = forms.CharField(widget=forms.TextInput())
    content = forms.Textarea()


# def __init__(self, *args, **kwargs):
#     super.__init__(*args, **kwargs)
#     self.helper = FormHelper()
#     self.helper.layout = Layout(
#         Row(
#             Column('title', css_class='form-group col-md-10 mb-0'),
#             css_class='form-row'
#         ),
#         Row(
#             Column('content', css_class='form-group col-md-10 mb-0'),
#             css_class='form-row'
#         ),
#     )
#     self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
#     self.helper.form_method = 'POST'
