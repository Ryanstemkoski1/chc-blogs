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
    young_adult = 555
    
    posts = [4230, 4244, 5305, 5331, 6256, 7143]
    for post in posts:
      post_id = post
       
      wordpress_url = f'https://childrenshealthcouncil.kinsta.cloud/wp-json/wp/v2/posts/{post_id}'
      
      response = requests.get(wordpress_url)
     
      if response.status_code == 200:
        blog = response.json()
        tags = blog['tags']
        
        if young_adult not in tags:
          tags.append(young_adult)
        
        print(tags)
        # wordpress_url = f'https://childrenshealthcouncil.kinsta.cloud/wp-json/wp/v2/posts/{post_id}'
        # payload = {
        #   'tags': tags
        # }
        
        # response = requests.post(wordpress_url, headers=headers, json=payload)
        # if response.status_code == 200:
        #     print('Post updated successfully.')
        # else:
        #    print(f"Failed to update post: {post_id}")
      else:
        print(f"Failed to fetch post: {post_id}")


    
  