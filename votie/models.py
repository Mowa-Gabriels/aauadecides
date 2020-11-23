from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):

    '''This model spells out the authorization requirements'''
    
    FACULTY = [
        ('Faculty of science', 'Faculty of science'),
        ('Faculty of education', 'Faculty of education'),
        ('Faculty of law', 'Faculty of law'),
        ('Faculty of agric', 'Faculty of agric'),
        ('Faculty of arts', 'Faculty of arts'),
    ]

    matric_no = models.CharField(_('Matric Number'), max_length=30, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    faculty = models.CharField(max_length=30, null=True, choices=FACULTY)
    Department = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_voter = models.BooleanField(_('voter'), default=True)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_staff = models.BooleanField(_('staff'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'matric_no'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)



class Poll(models.Model):
    text = models.CharField(max_length=202, blank=True)

    def __str__(self):
        return self.text

    def user_can_vote(self, user):
        """Returns false if user has already voted, if otherwise it returns true
        basically it checks if the user queryset is empty"""
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    choice_image = models.ImageField(default='default-avatar.png', upload_to='choice_image/', null=True, blank=True)

    def __str__(self):
        return  "{} - {}".format(self.poll.text[:25], self.choice_text[:25])

    @property
    def num_votes(self):
        return self.vote_set.count()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.matric_no


class Position(models.Model):
    text = models.CharField(_('description'), max_length=300, blank=True)

    def __str__(self):
        return self.text

class Candidate(models.Model):

    FACULTY = [
        ('Faculty of science', 'Faculty of science'),
        ('Faculty of education', 'Faculty of education'),
        ('Faculty of law', 'Faculty of law'),
        ('Faculty of agric', 'Faculty of agric'),
        ('Faculty of arts', 'Faculty of arts'),
    ]

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    faculty = models.CharField(max_length=30, null=True, choices=FACULTY)
    Department = models.CharField(max_length=30, null=True)
    image = models.ImageField(default='default-avatar.png', upload_to='user/', null=True, blank=True)
    description = models.CharField(max_length=255)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return  "{} - {}".format(self.position.text[:25], self.first_name[:25])

class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=True)

    def __str__(self):
        return self.user.matric_no