from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('icon', models.ImageField(upload_to='service-category-icons/')),
                ('basePrice', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={'ordering': ('name',)},
        ),
    ]
