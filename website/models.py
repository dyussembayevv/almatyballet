from django.utils import timezone
from django.db import models
from ckeditor.fields import RichTextField
import uuid
from django.utils.translation import gettext_lazy as _



# Карусель
class Carousel(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    subtitle = models.TextField("Описание")
    button_text = models.CharField("Текст кнопки", max_length=50)
    image = models.ImageField("Изображение", upload_to='carousel/')

    def __str__(self):
        return self.title

class Cast(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    full_name = models.CharField("Полное имя", max_length=255)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    photo = models.ImageField("Фото", upload_to="cast_photos/", null=True, blank=True)
    biography = models.TextField("Биография", blank=True)
    position = models.CharField("Должность", max_length=100, blank=True)
    theater = models.CharField("Театр / Труппа", max_length=255, blank=True)

    education = models.TextField("Образование", blank=True)
    roles = models.TextField("Основные партии / роли", blank=True)
    awards = models.TextField("Награды и звания", blank=True)
    activity_period = models.CharField("Период активности", max_length=100, blank=True)
    location = models.CharField("Город / Местоположение", max_length=100, blank=True)

    instagram = models.URLField("Instagram", max_length=255, blank=True)
    website = models.URLField("Персональный сайт", max_length=255, blank=True)
    contact_email = models.EmailField("Email для связи", blank=True)

    languages = models.CharField("Языки", max_length=255, blank=True)
    video_links = models.TextField("Видео выступлений (ссылки)", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Артист балета"
        verbose_name_plural = "Артисты балета"

    def __str__(self):
        return self.full_name

class Creative(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    full_name = models.CharField("Полное имя", max_length=255)
    age = models.IntegerField("Возраст", null=True, blank=True)
    biography = models.TextField("Биография", blank=True)
    image = models.ImageField("Фото", upload_to="creatives/", null=True, blank=True, default="defaults/blank-profile-picture-973460_1280.png")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Творческий специалист"
        verbose_name_plural = "Творческая команда"

# Событие
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Название", max_length=200)
    image = models.ImageField("Изображение", upload_to='event/', blank=True, null=True)
    date = models.DateField("Дата проведения")
    description = models.TextField("Описание")
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, blank=True, null=True)
    show_on_homepage = models.BooleanField("Показать на главной?", default=False)
    ticket_url = models.URLField("Ссылка на покупку билета", blank=True, null=True)
    slug = models.SlugField("URL-имя", unique=True, blank=True)
    start_time = models.TimeField(verbose_name="Время начала", blank=True, null=True)
    duration = models.DurationField(verbose_name="Продолжительность", blank=True, null=True)
    age_limit = models.PositiveIntegerField(verbose_name="Возрастное ограничение", blank=True, null=True)

    class Meta:
        ordering = ['date']
        verbose_name = "Постановка"
        verbose_name_plural = "Постановки"

    def __str__(self):
        return self.name

class EventCreativeRole(models.Model):
    ROLE_CHOICES = [
        ("choreographer", _("Хореограф")),
        ("director", _("Режиссёр")),
        ("composer", _("Композитор")),
        ("set_designer", _("Художник-постановщик")),
        ("costume_designer", _("Художник по костюмам")),
        ("lighting_designer", _("Художник по свету")),
        ("conductor", _("Дирижёр")),
        ("dramaturg", _("Драматург")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="creative_roles")
    creative = models.ForeignKey(Creative, on_delete=models.CASCADE, related_name="event_roles")
    role = models.CharField("Роль в постановке", max_length=50, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('event', 'creative', 'role')
        verbose_name = "Творец в постановке"
        verbose_name_plural = "Творцы в постановке"

    def __str__(self):
        return f"{self.creative.full_name} — {self.get_role_display()} в «{self.event.name}»"

class EventCastRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="cast_roles")
    cast = models.ForeignKey(Cast, on_delete=models.CASCADE, related_name="event_roles")
    role = models.CharField("Партию / Роль", max_length=100)

    class Meta:
        unique_together = ('event', 'cast', 'role')
        verbose_name = "Артист в постановке"
        verbose_name_plural = "Артисты в постановке"

    def __str__(self):
        return f"{self.cast.full_name} — {self.role} в «{self.event.name}»"


# Backstage (статья)
class Backstage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField("Заголовок", max_length=200)
    subtitle = models.CharField("Подзаголовок", default="")
    content = RichTextField("Текст")
    image = models.ImageField("Изображение", upload_to='backstage/', blank=True, null=True)
    video_url = models.URLField("Видео (ссылка)", blank=True, null=True)
    video_embed = models.CharField(max_length=2000, blank=True, null=True)
    show_on_homepage = models.BooleanField("Показать на главной?", default=False)
    created_at = models.DateTimeField("Дата создания", default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']