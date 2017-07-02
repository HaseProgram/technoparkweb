# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ask.models import Question, Answer, Profile
from random import choice, randint
from faker import Factory
import os

class Command(BaseCommand):
    help = 'Fill answers'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                action='store',
                dest='number',
                default=8,
                help='Min number of answers for a question'
        )

    def handle(self, *args, **options):
        fake = Factory.create()

        number = int(options['number'])
        min_number = 0
        max_number = number

        users = Profile.objects.all()
        questions = Question.objects.all()

        for q in questions:
            for i in range(0, randint(min_number, max_number)):
                text = fake.paragraph(nb_sentences=randint(2, 10), variable_nb_sentences=True)
                owner = choice(users)
                title = fake.sentence(nb_words=randint(4, 6), variable_nb_words=True)[:40]
                ans = Answer.objects.create(owner=owner, question=q, text=text)
                self.stdout.write('[%d] ans[%d]' % (q.id, ans.id))
