from django import forms


class CommentForm(forms.Form):
    content = forms.CharField()
    news_id = forms.IntegerField()





