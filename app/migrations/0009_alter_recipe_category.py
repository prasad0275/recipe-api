# Generated by Django 4.1.2 on 2023-06-14 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_recipe_posted_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='recipe', to='app.recipecategory'),
        ),
    ]
