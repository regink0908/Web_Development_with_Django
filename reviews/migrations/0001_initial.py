# Generated by Django 5.0.6 on 2024-06-10 12:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Название книги', max_length=70)),
                ('publication_date', models.DateField(verbose_name='Дата издательства')),
                ('isbn', models.CharField(max_length=20, verbose_name='ISBN-номер книги')),
            ],
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_names', models.CharField(help_text='Имя/имена участника/ов.', max_length=50)),
                ('last_names', models.CharField(help_text='Фамилия/фамилии участника/ов', max_length=50)),
                ('email', models.EmailField(help_text='Контактный адрес электронной почты участника', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название издательства', max_length=50)),
                ('website', models.URLField(help_text='Веб-сайт издателя')),
                ('email', models.EmailField(help_text='Адрес электронной почты Издателя', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='BookContributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('AUTHOR', 'Author'), ('CO_AUTHOR', 'Co-Author'), ('EDITOR', 'Editor')], max_length=20, verbose_name='Роль, которую сыграл этот автор в создании книги')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.book')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.contributor')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='contributors',
            field=models.ManyToManyField(through='reviews.BookContributor', to='reviews.contributor'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.publisher'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(help_text='Текст рецензии')),
                ('rating', models.IntegerField(help_text='Оценка, данная рецензентом')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='Дата и время создания обзора')),
                ('date_edited', models.DateTimeField(help_text='Дата и время последнего изменения обзора', null=True)),
                ('book', models.ForeignKey(help_text='Книга, для которой предназначен этот обзор', on_delete=django.db.models.deletion.CASCADE, to='reviews.book')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
