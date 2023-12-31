# Generated by Django 4.2.4 on 2023-09-11 07:48

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("taggit", "0005_auto_20220424_2025"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        help_text="A slug to identify posts by this category",
                        max_length=255,
                        verbose_name="slug",
                    ),
                ),
            ],
            options={
                "verbose_name": ("Blog Categories",),
                "verbose_name_plural": "Blog Categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="BlogPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("blog_title", models.CharField(blank=True, max_length=255)),
                (
                    "date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Creation time"
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Update time"
                    ),
                ),
                ("description", models.CharField(default="", max_length=250)),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            ("content", wagtail.blocks.RichTextBlock(required=False)),
                            (
                                "image",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(
                                                required=False
                                            ),
                                        ),
                                        (
                                            "caption",
                                            wagtail.blocks.CharBlock(required=False),
                                        ),
                                    ]
                                ),
                            ),
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
                ("author", models.CharField(default="Anonymous", max_length=100)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="BlogPage_Category",
                        to="blog.blogcategory",
                    ),
                ),
                (
                    "feed_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Blog Page",
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="BlogPageTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content_object",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tagged_items",
                        to="blog.blogpage",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_items",
                        to="taggit.tag",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="blogpage",
            name="tags",
            field=modelcluster.contrib.taggit.ClusterTaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="blog.BlogPageTag",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
