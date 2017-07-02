# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from ask.models import Question, LikeToQuestion, Answer, LikeToAnswer, Profile

from random import choice, randint

class Command(BaseCommand):
    help = 'Fill likes'

    def add_arguments(self, parser):
        parser.add_argument('--number-answers',
                action='store',
                dest='number_answers',
                default=5,
                help='Number of likes for an answer'
        )
        parser.add_argument('--number-questions',
                action='store',
                dest='number_questions',
                default=5,
                help='Number of likes for a question'
        )

    def handle(self, *args, **options):
        number_answers = int(options['number_answers'])
        number_questions = int(options['number_questions'])

        users = Profile.objects.all()
        questions = Question.objects.all()
        self.stdout.write(str(number_questions) + " " + str(questions.count()))
        for q in questions:
            print(q)
            self.stdout.write('question [%d]' % q.id)
            for i in range(0, number_questions):
                LikeToQuestion.objects.add_or_update(
                        owner=choice(users),
                        question=q,
                        value=choice([-1, 1])
                        )

        answers = Answer.objects.all()

        for ans in answers:
            self.stdout.write('answer [%d]' % ans.id)
            for i in range(0, number_answers):
                LikeToAnswer.objects.add_or_update(
                        owner=choice(users),
                        answer=ans,
                        value=choice([-1, 1])
)
