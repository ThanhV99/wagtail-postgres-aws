from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel

from django.core.exceptions import ValidationError

#catogory
from wagtail.snippets.models import register_snippet
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from django.utils.text import slugify
from django.contrib import messages

from blog.blocks import SectionBlock
from wagtail import blocks
from django.utils import timezone

# tag
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

        
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )
        
        
class BlogPage(Page):
    class Meta:
        verbose_name = "Blog Page"
        # db_tablespace = 'test_data' # postgress rds khong co tablespace

    blog_title = models.CharField(max_length=255, blank=True)
    date = models.DateField("Creation time", null=True, blank=True)
    update_time = models.DateTimeField("Update time", null=True, blank=True)
    description = models.CharField(max_length=250, default='')
    body = StreamField(
        [
            ('content', blocks.RichTextBlock(required=False)),
            ("image", SectionBlock()),
        ],
        use_json_field=True,
        blank=True,
    )
    author = models.CharField(max_length=100, default="Anonymous")
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    category = models.ForeignKey('blog.BlogCategory', blank=True, null=True, on_delete=models.SET_NULL, related_name='BlogPage_Category')
    feed_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date', read_only=True),
            FieldPanel('update_time', read_only=True),
        ], heading="Time"),
        MultiFieldPanel([
            FieldPanel('tags'),
            FieldPanel('category'), 
        ], heading="Information"),
        MultiFieldPanel([
            FieldPanel('description'),
            FieldPanel('body'),
            FieldPanel('author'),
        ], heading="Content"),
        FieldPanel("feed_image")
    ]
    
    def clean(self):
        super().clean()
        if self.category is None:
            raise ValidationError('Category is required.')
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is triggered before saving
        if not self.id:
            self.date = timezone.now()
        self.blog_title = self.title
        self.update_time = timezone.now()
        super().save(*args, **kwargs)
        

@register_snippet
class BlogCategory(models.Model):
    class Meta:
        verbose_name_plural = 'Blog Categories'
        verbose_name = "Blog Categories",
        ordering = ["name"]
        
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
        blank=True,
    )

    panels = [
        FieldPanel('name'),
        FieldPanel("slug", read_only=True),
    ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from name if it doesn't exist
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
        
    def generate_unique_slug(self):
        original_slug = slugify(self.name)
        slug = original_slug
        while BlogCategory.objects.filter(slug=slug).exclude(id=self.id).exists():
            messages.error(None, f"Slug '{slug}' is not unique. Please choose a different name.")
            raise ValueError("Non-unique slug")
        return slug