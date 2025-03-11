from django.contrib.auth import get_user_model
from django.db import models

from .constants import MAX_LENGTH_TITLE


User = get_user_model()


class Group(models.Model):
    """
    Модель для представления сообщества.

    Атрибуты:
        title: Название сообщества.
        slug: Уникальный идентификатор сообщества (URL friendly).
        description: Описание сообщества.
    """
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE
    )
    slug = models.SlugField(
        unique=True
    )
    description = models.TextField()

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Модель для представления публикации.

    Атрибуты:
        text: Текст публикации.
        pub_date: Дата публикации.
        author: Автор публикации (ссылка на пользователя).
        image: Изображение, прикрепленное к публикации (необязательно).
        group: Сообщество, к которому относится публикация (необязательно).
    """
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True, blank=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель для представления комментария к публикации.

    Атрибуты:
        author: Автор комментария (ссылка на пользователя).
        post: Публикация, к которой относится комментарий.
        text: Текст комментария.
        created: Дата и время создания комментария.
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('-created',)

    def __str__(self):
        return self.text[:20]


class Follow(models.Model):
    """
    Модель для представления подписки пользователя на другого пользователя.

    Атрибуты:
        user: Пользователь, который подписывается.
        following: Пользователь, на которого подписываются.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик', )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан', )

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='check_not_self_follow',
            ),
        )

    def __str__(self):
        return f"{self.user} подписан на {self.following}"
