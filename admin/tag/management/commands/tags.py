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
    per_page = 100
    page = 1
    
    while True:
      params = {
        'per_page': per_page, 
        'page': page,
        'categories': 191
      }
      
      young_child = 553
      
      response = requests.get(url, params=params)
      
      if response.status_code == 200:
        
        posts = response.json()
        
        for index, post in enumerate(posts):
          print(index)
          print(post['title'])
          
          post_id = post['id']
          tags = post['tags']
          
          if young_child not in tags:
            tags.append(young_child)
          
          
          wordpress_url = f'https://childrenshealthcouncil.kinsta.cloud/wp-json/wp/v2/posts/{post_id}'
          payload = {
            'tags': tags
          }
          
          response = requests.post(wordpress_url, headers=headers, json=payload)
          
          if response.status_code == 200:
            print('Post updated successfully.')
          
          else:
            print('Failed to update post.')
            FailedPost.objects.update_or_create(
              defaults={
                  'post_id': post_id,
              },
              post_title=post.post_title
            )
            
        page += 1
        
      else:
        print(f"Failed to fetch custom data: {response.status_code}")
        break

    
  