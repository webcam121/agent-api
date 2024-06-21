# Generated by Django 3.1.6 on 2024-05-10 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterLimitSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('achievement_character_limit', models.IntegerField(blank=True, null=True)),
                ('unusual_character_limit', models.IntegerField(blank=True, null=True)),
                ('noend_character_limit', models.IntegerField(blank=True, null=True)),
                ('verylong_character_limit', models.IntegerField(blank=True, null=True)),
                ('controversial_character_limit', models.IntegerField(blank=True, null=True)),
                ('nontraditional_character_limit', models.IntegerField(blank=True, null=True)),
                ('funny_character_limit', models.IntegerField(blank=True, null=True)),
                ('opinion_character_limit', models.IntegerField(blank=True, null=True)),
                ('someonenew_character_limit', models.IntegerField(blank=True, null=True)),
                ('default_character_limit', models.IntegerField(blank=True, null=True)),
                ('min_character', models.IntegerField(blank=True, null=True)),
                ('max_character', models.IntegerField(blank=True, null=True)),
                ('number_q_topic_limit', models.IntegerField(blank=True, null=True)),
                ('total_number_topics_limit', models.IntegerField(blank=True, null=True)),
                ('number_messages_cutoff', models.IntegerField(blank=True, null=True)),
                ('num_postfix_cutoff', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(choices=[('trial', 'Trial'), ('default', 'Default'), ('notrivia', 'No Trivia')], default='default', max_length=255)),
            ],
            options={
                'verbose_name': 'Character Limit Setting',
                'verbose_name_plural': 'Character Limit Settings',
            },
        ),
        migrations.CreateModel(
            name='PersonalQuestionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(default='', max_length=255)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Personal Question Category',
                'verbose_name_plural': 'Personal Question Categories',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='SystemQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.TextField()),
                ('rank', models.FloatField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_system_questions', to='questions.personalquestioncategory')),
            ],
            options={
                'verbose_name': 'System Question',
                'verbose_name_plural': 'System Questions',
            },
        ),
        migrations.CreateModel(
            name='PersonalQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.TextField()),
                ('covered', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_questions', to='questions.personalquestioncategory')),
                ('gift_giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='accounts.giftgiver')),
                ('gift_receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver_questions', to='accounts.giftreceiver')),
                ('pre_receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_receiver_questions', to='accounts.prereceiver')),
            ],
            options={
                'verbose_name': 'Personal Question',
                'verbose_name_plural': 'Personal Questions',
            },
        ),
    ]