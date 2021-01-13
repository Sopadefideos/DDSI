# Generated by Django 3.1.5 on 2021-01-13 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BeatSharkApp', '0003_auto_20210113_0106'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavCancion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BeatSharkApp.cancion')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BeatSharkApp.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='FavArtista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artista', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BeatSharkApp.artista')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BeatSharkApp.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='FavAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BeatSharkApp.album')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BeatSharkApp.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='CancionArtista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artista', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BeatSharkApp.artista')),
                ('cancion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BeatSharkApp.cancion')),
            ],
        ),
        migrations.CreateModel(
            name='AlbumCancion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BeatSharkApp.album')),
                ('cancion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BeatSharkApp.cancion')),
            ],
        ),
    ]
