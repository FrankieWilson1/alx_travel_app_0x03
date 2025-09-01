import random
from datetime import timedelta, timezone as dt_timezone

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from faker import Faker

from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seeds the database with sample data for Listings, Bookings, and Reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_listings',
            type=int,
            default=20,
            help='Number of fake listings to create.'
        )
        parser.add_argument(
            '--num_users',
            type=int,
            default=5,
            help='Number of fake users to create (if not enough exist)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding.'
        )

    def handle(self, *args, **options):
        num_listings = options['num_listings']
        num_users = options['num_users']
        clear_data = options['clear']
        fake = Faker()

        self.stdout.write(self.style.NOTICE(f'Starting database seeding...'))

        if clear_data:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Listing.objects.all().delete()
            Booking.objects.all().delete()
            Review.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        with transaction.atomic():
            if User.objects.count() < num_users:
                self.stdout.write(
                    self.style.NOTICE(
                        f'Creating {num_users - User.objects.count()} additional users...'
                    )
                )
                for _ in range(num_users - User.objects.count()):
                    User.objects.create_user(
                        username=fake.user_name() + str(random.randint(1, 1000)),
                        email=fake.email(),
                        password='password123'
                    )
                self.stdout.write(self.style.SUCCESS('Users created.'))
            users = list(User.objects.all())

            self.stdout.write(self.style.NOTICE(f'Creating {num_listings} fake listings...'))
            listings = []
            for _ in range(num_listings):
                listing = Listing.objects.create(
                    title=fake.sentence(nb_words=6),
                    address=fake.street_address(),
                    city=fake.city(),
                    state=fake.state_abbr(),
                    zipcode=fake.postcode(),
                    description=fake.paragraph(nb_sentences=5),
                    price=random.randint(100000, 1000000),
                    bedrooms=random.randint(1, 5),
                    bathrooms=round(random.uniform(1.0, 4.0), 1),
                    garage=fake.boolean(),
                    sqft=random.randint(800, 3000),
                    lot_size=round(random.uniform(0.1, 1.5), 2),
                    photo_main=(
                        # This line was incorrect. It should be a string.
                        f'photos/{timezone.now().year}/{timezone.now().month:02d}/{timezone.now().day:02d}/main_{fake.uuid4()}.jpg'
                    ),
                    is_published=fake.boolean(),
                    # This now uses our dt_timezone alias
                    list_date=fake.date_time_between(start_date='-2y', end_date='now', tzinfo=dt_timezone.utc)
                )
                listings.append(listing)
            self.stdout.write(self.style.SUCCESS(f'{len(listings)} listings created.'))

            # Create Bookings.
            self.stdout.write(self.style.NOTICE(f'Creating bookings for listings...'))
            for listing in listings:
                if random.random() < 0.7:
                    num_bookings = random.randint(1, 3)
                    for _ in range(num_bookings):
                        user = random.choice(users)
                        start_date = fake.date_between(start_date='-1y', end_date='+6m')
                        end_date = start_date + timedelta(days=random.randint(2, 14))
                        total_price = listing.price / 30 * (end_date - start_date).days
                        Booking.objects.create(
                            listing=listing,
                            user=user,
                            start_date=start_date,
                            end_date=end_date,
                            total_price=round(total_price, 2),
                            is_confirmed=fake.boolean(),
                            # This now uses our dt_timezone alias
                            created_at=fake.date_time_between(start_date=start_date, end_date='now', tzinfo=dt_timezone.utc)
                        )
            self.stdout.write(self.style.SUCCESS(
                f'{Booking.objects.count()} bookings created.'
            ))

            # Create Reviews
            self.stdout.write(self.style.NOTICE(
                f'Creating reviews for listings...'
            ))
            for booking in Booking.objects.all():
                if random.random() < 0.8:
                    Review.objects.create(
                        listing=booking.listing,
                        user=booking.user,
                        rating=random.randint(1, 5),
                        comment=fake.paragraph(
                            nb_sentences=2,
                            variable_nb_sentences=True
                        ) if random.random() < 0.7 else "",
                        created_at=fake.date_time_between(
                            start_date=booking.end_date,
                            end_date='now', tzinfo=dt_timezone.utc
                        )
                    )
            self.stdout.write(self.style.SUCCESS(
                f'{Review.objects.count()} reviews created.'
            ))
        self.stdout.write(self.style.SUCCESS(
            'Database seeding complete!'
        ))
