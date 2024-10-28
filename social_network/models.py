from django.db import models
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

class User(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    avatar = models.ImageField(upload_to='avatars', verbose_name='Аватар', blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):

        if self.avatar:
            img = Image.open(self.avatar)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)

                thumb_io = BytesIO()
                img.save(thumb_io, format='JPEG')

                self.avatar.save(self.avatar.name, ContentFile(thumb_io.getvalue()), save=False)

        super().save(*args, **kwargs)

class Message(models.Model):
    text_message = models.TextField(verbose_name='Текст сообщения')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель', related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Получатель', related_name='received_messages')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.sender} -> {self.receiver} : {self.text_message} at {self.sent_at}'


class Group(models.Model):
    description = models.TextField(verbose_name='Описание')
    name = models.CharField(max_length=20, verbose_name='Название группы')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Администратор', related_name='admin_groups')
    users = models.ManyToManyField(User, through='UserGroup', verbose_name='Пользователи', related_name='groups')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.description} - {self.admin}'

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.group} - {self.text} - {self.pub_date}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост',related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор',related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Родительский комментарий', related_name='replies', null=True, blank=True)
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.post} - {self.text} - {self.author} - {self.created_at}'
