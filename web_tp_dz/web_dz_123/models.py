from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Sum, Case, When, IntegerField, OuterRef
from django.db.models import Count
from django.shortcuts import get_object_or_404


class QuestionSerializer(models.Manager):
    def get_hot(self):
        return self.order_by('-rating','title')

    def get_one_question(self, pk):
        get_object_or_404(Question, id=pk)
        return self.get(id=pk)

    def get_new(self):
        return self.order_by('-created_at')
    
    def by_tag(self, tag_name):
        bytag = get_object_or_404(Tag, name=tag_name)
        questions = Question.objects.filter(tag=bytag)
        print(bytag.questions_count)
        return questions

class TagSerializer(models.Manager):
    def get_popular(self):
        return self.order_by('-questions_count')[:10]

    def increase_question_count(self,tag):
        same_tag = self.get(name=tag)
        same_tag.questions_count += 1
        same_tag.save()
        return same_tag


class AnswerSerializer(models.Manager):
    def by_question(self, pk):
        answers = Answer.objects.filter(question__id=pk)
        return answers.order_by('-rating')

class UserSerializer(models.Manager):
    def best_members(self):
        return self.order_by('-activity')[:10]
    
    def get_one_member(self, User_name):
        get_object_or_404(Profile, nickname=User_name)
        return self.get(nickname=User_name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='user_profile')
    avatar = models.ImageField(null=True, blank=True,upload_to="images/")
    nickname = models.CharField(max_length=255)
    activity = models.IntegerField(default=0)
    likes_count_answer = models.IntegerField(default=0)
    likes_count_question = models.IntegerField(default=0)

    objects = UserSerializer()

    def __str__(self):
        return self.nickname

class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    questions_count = models.IntegerField(default=0)

    objects = TagSerializer()

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)

    objects = QuestionSerializer()
    
    def __str__(self):
        return self.title

class Answer(models.Model):
    STATUS_CHOICES = [("m", "Right"), ("nm", "Not marked")]
    text = models.TextField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10,default='nm')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    objects = AnswerSerializer()

    def __str__(self):
        return self.text
 
class LikeAnswer(models.Model):
    STATUS_CHOICES = [(1, "Like"), (-1, "Dislike")] #Поднимаем ответы с лучшим соотношением лайков - дизлайков
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,default='')
    status = models.IntegerField(choices=STATUS_CHOICES)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.nickname
    
    class Meta:
        unique_together = ('user', 'answer')

class LikeQuestion(models.Model):
    STATUS_CHOICES = [("l", "Like"), ("d", "Dislike")]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,default='')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.nickname
    
    class Meta:
        unique_together = ('user', 'question')
