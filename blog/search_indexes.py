from haystack import indexes
from .models import Post


# search_indexes.py file should within the app it applies to
class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # user_template=True allow us to use a data template
    # to build the document the search engine will index
    # path of template should be
    # "templates/search/indexes/<app_name>/<model_name>_text.txt
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
