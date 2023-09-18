from __future__ import unicode_literals
import graphene
from graphene_django import DjangoObjectType
from blog.models import BlogPage, BlogCategory
from graphene import Argument
from django.db.models import F

from blog.blocks import SectionBlock
from wagtail import blocks
from wagtail.images.models import Image

# --------- section block ------- #
class SectionBlockType(graphene.ObjectType):
    image = graphene.String()
    caption = graphene.String()
    
class RichTextBlockType(graphene.ObjectType):
    content = graphene.String()
    
class BlockUnion(graphene.Union):
    class Meta:
        types = (SectionBlockType, RichTextBlockType)
# ------------------------------------
# ------------ tags ------------------
class TagsBlockType(graphene.ObjectType):
    tag = graphene.String()
# ------------------------------------

# ---------- category ----------------
class CategoryType(DjangoObjectType):
    blog = graphene.List(lambda: BlogNode)
    class Meta:
        model = BlogCategory
        fields = ['name', 'slug'] # truong categories link voi blog mac dinh dc sinh ra
    def resolve_blog(self, info):
        return self.BlogPage_Category.all() # ten related_name

# ------------------------------------

class BlogNode(DjangoObjectType):
    body = graphene.List(BlockUnion)
    feed_image = graphene.String()
    category = graphene.List(CategoryType)
    update_time = graphene.String()
    
    class Meta:
        model = BlogPage
        only_fields = ['title', 'update_time', 'description', 'author', 'slug']
    
    def resolve_body(self, info):
        body_data = []
        for block in self.body:
            # ininstance kiem tra doi tuong la 1 mot instance hay mot class con
            if isinstance(block.block, blocks.RichTextBlock):
                body_data.append(RichTextBlockType(content=block.value))
            elif isinstance(block.block, SectionBlock):
                section_block = block.value
                body_data.append(SectionBlockType(image=section_block.get('image').file.url, caption=section_block.get('caption')))
        return body_data   
     
    def resolve_feed_image(self, info):
        return self.feed_image.file.url if self.feed_image else None
    
    def resolve_category(self, info):
        return self.categories.all() 
    
    def resolve_update_time(self, info):
        return self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
    
class Query(graphene.ObjectType):
    allBlog = graphene.List(BlogNode, order_by=Argument(graphene.String, default_value='update_time'))
    blog = graphene.Field(BlogNode, slug=graphene.String())
    
    allCategories = graphene.List(CategoryType)
    blogsByCategory = graphene.List(BlogNode, slug=graphene.String(), num_blogs=graphene.Int())

    # @graphene.resolve_only_args
    def resolve_allBlog(self, info, order_by):
        # Define the default field to sort by
        if order_by == 'update_time':
            order_field = F('update_time')
        else:
            order_field = F('update_time')  # You can set a default ordering field here

        return BlogPage.objects.live().order_by(order_field).reverse()
    
    def resolve_blog(self, info, slug):
        try:
            return BlogPage.objects.live().get(slug=slug)
        except BlogPage.DoesNotExist:
            return None
        
    def resolve_allCategories(self, info):
        return BlogCategory.objects.all()
    
    def resolve_blogsByCategory(self, info, slug, num_blogs):
        try:
            category = BlogCategory.objects.get(slug=slug)
            order_field = F('update_time')
            if num_blogs == -1:
                return category.BlogPage_Category.live().order_by(order_field).reverse()
            else:
                return category.BlogPage_Category.live().order_by(order_field).reverse()[:num_blogs]  # Retrieve live blog pages associated with the category
        except BlogCategory.DoesNotExist:
            return []

schema = graphene.Schema(query=Query)