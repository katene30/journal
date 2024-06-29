from wagtail.core import hooks
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdmin
from .models import JournalEntry

class JournalEntryAdmin(ModelAdmin):
    model = JournalEntry
    menu_label = "Journal Entries"
    menu_icon = "edit"
    # list_display = ('user', 'date', 'mood', 'overall_day_rating')
    search_fields = ('user__username', 'date', 'log')
    list_filter = ('date', 'user')

    def get_edit_handler(self):
        return [
            FieldPanel('user'),
            FieldPanel('date'),
            FieldPanel('log'),
            FieldPanel('mood'),
            FieldPanel('depression_level'),
            FieldPanel('anxiety_level'),
            FieldPanel('stress_level'),
            FieldPanel('sleep_hours'),
            FieldPanel('sleep_quality'),
            FieldPanel('energy_level'),
            FieldPanel('social_interactions_quality'),
            FieldPanel('productivity_level'),
            FieldPanel('diet_quality'),
            FieldPanel('alcohol_caffeine_consumption'),
            FieldPanel('self_care_effectiveness'),
            FieldPanel('significant_events'),
            FieldPanel('overall_day_rating'),
        ]

modeladmin_register(JournalEntryAdmin)
