from django.core.management.base import BaseCommand

class Commands(BaseCommand):
  help ="tags"
  
  def handle(self, *args, **options):
    print(f"test")  
  