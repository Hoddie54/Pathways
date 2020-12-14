from django.db import models
from pathway.models import DisplayStage


class Article(models.Model):
    title = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.title


class DisplayStageArticleConnector(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE
    )

    display_stage = models.ForeignKey(
        'pathway.DisplayStage',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.article) + ": " + str(self.display_stage)


class ArticleSection(models.Model):

    title = models.CharField(max_length=150)
    description = models.TextField(verbose_name="Add an optional description. The user never sees this", null=True, blank=True)
    order = models.IntegerField(default=1000)
    article = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return str(self.article.title) + ": " + self.title + ". " + self.description

    class Meta:
        ordering = ['order']


class ArticleComponent(models.Model):

    title = models.CharField(max_length=150)
    order = models.IntegerField(default=1000)
    article_section = models.ForeignKey(
        ArticleSection,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return str(self.article_section) + ": " + self.title

    class Meta:
        abstract = True
        ordering = ['order']


class ArticleComponentText(ArticleComponent):
    content = models.TextField()


class ArticleComponentImage(ArticleComponent):
    content = models.ImageField(upload_to='article_image/')


class ArticleComponentTable(ArticleComponent):
    pass


class ArticleComponentTableRow(models.Model):
    table = models.ForeignKey(
        ArticleComponentTable,
        on_delete=models.CASCADE
    )
    order = models.IntegerField(default=1000)

    def __str__(self):
        return str(self.table) + ": Row " + self.order

    class Meta:
        ordering = ['order']


class ArticleComponentTableRowEntry(models.Model):
    row = models.ForeignKey(
        ArticleComponentTableRow,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    order = models.IntegerField(default=1000)

    def __str__(self):
        return str(self.row) + ": Entry " + self.order

    class Meta:
        ordering = ['order']