from django.core.management.base import BaseCommand
import requests
import base64
from tag.models import FailedPost

url = 'https://childrenshealthcouncil.kinsta.cloud/wp-json/wp/v2/posts'

wp_user = 'ryan.stemkoski@abectech.com'
wp_password = 'Ltr1 Lw9A wNEf aNrI zKsT AnL5'

headers = {
    'Authorization': 'Basic ' + base64.b64encode(f'{wp_user}:{wp_password}'.encode()).decode(),
    'Content-Type': 'application/json'
}

class Command(BaseCommand):
  help ="tags"
  
  def handle(self, *args, **options):
    cat_slugs = [
      "parent-caregiver", 
      "parenting", 
      "parenting-preteen", 
      "parenting-school-age", 
      "parenting-teen", 
      "parenting-young-adult", 
      "parenting-young-child", 
      "parenting-young-adults", 
      "special-needs-parenting"
    ]
    
    cat_ids =[]
    
    for cat_slug in cat_slugs:
      url = f'https://childrenshealthcouncil.kinsta.cloud/wp-json/wp/v2/categories?slug={cat_slug}'
      response = requests.get(url)
    
      if response.status_code == 200:
          categories = response.json()
          
          if categories:
            cat_ids.append(categories[0]['id'])
            
          else:
            print(f"Error: Unable to fetch category for slug '{cat_slug}'")
            
      else:
          print(f"Error: Unable to fetch category for slug '{cat_slug}'")
          return None
    
    print(cat_ids)