from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.models import Site
from .models import JournalEntry, JournalEntryPage

@receiver(post_save, sender=JournalEntry)
def create_journal_entry_page(sender, instance, created, **kwargs):
    print(f"Signal triggered for JournalEntry {instance.pk}")
    if created:
        # Create a JournalEntryPage linked to this JournalEntry
        homepage = Site.objects.first().root_page
        entry_page = JournalEntryPage(
            title=f"Entry for {instance.date}",
            slug=f"entry-{instance.pk}",
            journal_entry=instance,
            live=True,
            path=f"{homepage.path}{instance.pk}/",
            depth=homepage.depth + 1,
            numchild=0
        )
        homepage.add_child(instance=entry_page)
        entry_page.save()
        instance.entry_url = entry_page.url
        instance.save()
