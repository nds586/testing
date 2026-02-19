from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('services', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'scheduledTime',
                    models.DateTimeField(),
                ),
                ('serviceAddress', models.TextField()),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('PENDING', 'Pending'),
                            ('ACCEPTED', 'Accepted'),
                            ('STARTED', 'Started'),
                            ('COMPLETED', 'Completed'),
                            ('CANCELLED', 'Cancelled'),
                        ],
                        default='PENDING',
                        max_length=20,
                    ),
                ),
                (
                    'category',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='bookings',
                        to='services.servicecategory',
                    ),
                ),
                (
                    'customer',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='bookings',
                        to='users.customer',
                    ),
                ),
                (
                    'service_provider',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='bookings',
                        to='users.serviceprovider',
                    ),
                ),
            ],
            options={'ordering': ('-scheduledTime',)},
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('comment', models.TextField()),
                (
                    'booking',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='review',
                        to='bookings.booking',
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(
                check=models.Q(('rating__gte', 1), ('rating__lte', 5)),
                name='review_rating_between_1_and_5',
            ),
        ),
    ]
