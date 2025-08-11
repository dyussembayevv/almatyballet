from django.contrib import admin
from .models import Carousel, Event, Backstage, EventCastRole, EventCreativeRole, Cast, Creative


# --- Inline для Cast в Event ---
class EventCastRoleInline(admin.TabularInline):
    model = EventCastRole
    extra = 1
    autocomplete_fields = ['cast']


# --- Inline для Creative в Event ---
class EventCreativeRoleInline(admin.TabularInline):
    model = EventCreativeRole
    extra = 1
    autocomplete_fields = ['creative']

# --- Event с двумя inlines ---
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "show_on_homepage")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [EventCastRoleInline, EventCreativeRoleInline]

    def save_model(self, request, obj, form, change):
        if obj.show_on_homepage:
            current_home_events = Event.objects.filter(show_on_homepage=True).exclude(pk=obj.pk)
            if current_home_events.count() >= 3:
                from django.core.exceptions import ValidationError
                raise ValidationError("Можно выбрать не более 3 событий для главной страницы.")
        super().save_model(request, obj, form, change)


# --- Cast Admin ---
@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ("full_name", "birth_date", "position", "theater")
    search_fields = ("full_name", "position", "theater")
    list_filter = ("position",)


# --- Creative Admin ---
@admin.register(Creative)
class CreativeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "age")
    search_fields = ("full_name",)


# --- Можно зарегистрировать отдельно EventCastRole и EventCreativeRole (по желанию) ---
@admin.register(EventCastRole)
class EventCastRoleAdmin(admin.ModelAdmin):
    list_display = ("event", "cast", "role")
    search_fields = ("cast__full_name", "role")


@admin.register(EventCreativeRole)
class EventCreativeRoleAdmin(admin.ModelAdmin):
    list_display = ("event", "creative", "role")
    search_fields = ("creative__full_name", "role")

# Carousel
@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'button_text')

# Backstage
@admin.register(Backstage)
class BackstageAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_on_homepage')
    list_editable = ('show_on_homepage',)

    def save_model(self, request, obj, form, change):
        if obj.show_on_homepage:
            current_home_backstages = Backstage.objects.filter(show_on_homepage=True).exclude(pk=obj.pk)
            if current_home_backstages.count() >= 4:
                from django.core.exceptions import ValidationError
                raise ValidationError("Можно выбрать не более 4 backstage материалов для главной страницы.")
        super().save_model(request, obj, form, change)
