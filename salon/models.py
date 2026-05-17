from django.db import models


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('hair', 'Волосы'),
        ('nails', 'Ногти'),
        ('brows', 'Брови и ресницы'),
        ('makeup', 'Макияж'),
        ('skin', 'Уход за лицом'),
        ('other', 'Другое'),
    ]
    name = models.CharField(max_length=200, verbose_name='Услуга')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name='Категория')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=0, verbose_name='Цена (сом)')
    duration = models.IntegerField(default=60, verbose_name='Длительность (мин)')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order', 'category', 'name']
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f"{self.name} — {self.price} сом"


class Master(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    specialty = models.CharField(max_length=200, verbose_name='Специализация')
    photo = models.ImageField(upload_to='masters/', blank=True, null=True, verbose_name='Фото')
    bio = models.TextField(blank=True, verbose_name='О мастере')
    experience_years = models.IntegerField(default=1, verbose_name='Опыт (лет)')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return self.name


class GalleryPhoto(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='Название')
    image = models.ImageField(upload_to='gallery/', blank=True, null=True, verbose_name='Фото')
    category = models.CharField(max_length=20, choices=Service.CATEGORY_CHOICES, default='other', verbose_name='Категория')
    master = models.ForeignKey(Master, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Мастер')
    video_url = models.URLField(blank=True, default='', verbose_name='Ссылка (Instagram/TikTok/YouTube)')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name='Показывать')

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Фото галереи'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return self.title or f"Фото #{self.pk}"


class Review(models.Model):
    client_name = models.CharField(max_length=200, verbose_name='Имя клиента')
    rating = models.IntegerField(default=5, verbose_name='Оценка (1-5)')
    text = models.TextField(verbose_name='Отзыв')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Услуга')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"{self.client_name} — {'★' * self.rating}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    client_name = models.CharField(max_length=200, verbose_name='Имя клиента')
    client_phone = models.CharField(max_length=20, verbose_name='Телефон')
    client_email = models.EmailField(blank=True, verbose_name='Email')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, verbose_name='Услуга')
    master = models.ForeignKey(Master, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Мастер')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    payment_method = models.CharField(
        max_length=20,
        choices=[('cash', 'Наличные'), ('card', 'Карта онлайн')],
        default='cash',
        verbose_name='Способ оплаты'
    )
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f"{self.client_name} — {self.date} {self.time}"
