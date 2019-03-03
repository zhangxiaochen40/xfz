from haystack import indexes
from .models import News


class NewsIndex(indexes.Indexable,indexes.SearchIndex):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return News
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
