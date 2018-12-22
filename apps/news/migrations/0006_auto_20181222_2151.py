# Generated by Django 2.1.3 on 2018-12-22 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField()),
                ('img_url', models.URLField()),
                ('link_to', models.URLField()),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-priority'],
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-pub_time']},
        ),
    ]
