from django.db import models
class AbstractPost(models.Model):
    post_id = models.IntegerField(primary_key=True, null=False)
    post_title = models.CharField(max_length=10000, null=False)
    post_content = models.TextField(null=True)
    tags = models.TextField(null=True)
    categories = models.TextField(null=True)
    def __str__(self):
        return self.post_title

    class Meta:
        abstract = True


class Post(AbstractPost):
    pass

class FailedPost(AbstractPost):
    pass