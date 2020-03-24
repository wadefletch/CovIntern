from django.core.management.base import BaseCommand
from faker import Faker
import random
from jobs.models import Company, Job, Category
import sys
import time
fake = Faker()


class Command(BaseCommand):
    help = 'Adds a bunch of fake data'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        start_time = time.time()
        r = 0
        for i in range(options['count']):
            name = fake.company()
            c = Company(
                name=name,
                location=f'{fake.city()}, {fake.state_abbr()}',
                url=name.lower().replace(' ', '-')+'.com',
                logo=Company.objects.get(pk=1).logo
            )
            c.save()
            r += 1

            j = Job(
                title=fake.job()+' Intern',
                company=c,
                hours_per_week=fake.pyint(min_value=10, max_value=40, step=5),
                application_link='scoretwo.com',
                category=random.choice(Category.objects.all()),
                description=fake.text(max_nb_chars=1500, ext_word_list=None),
                qualifications=fake.text(max_nb_chars=1500, ext_word_list=None),
            )
            j.save()
            r += 1

            sys.stdout.write(f"\rCreating Company/Job {i} of {options['count']}")
            sys.stdout.flush()

        end_time = time.time()
        print(f'\rDone. Created {r} records in {round(end_time-start_time, 2)} seconds.')

