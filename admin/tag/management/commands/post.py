from django.core.management.base import BaseCommand
import requests
import base64
from tag.models import FailedPost, Post

url = 'https://childrenshealthcouncil.kinsta.cloud/wp-json/wp/v2/posts'

wp_user = 'ryan.stemkoski@abectech.com'
wp_password = 'Ltr1 Lw9A wNEf aNrI zKsT AnL5'

headers = {
    'Authorization': 'Basic ' + base64.b64encode(f'{wp_user}:{wp_password}'.encode()).decode(),
    'Content-Type': 'application/json'
}

class Command(BaseCommand):
  help ="posts"
  
  def handle(self, *args, **options):
    per_page = 100
    page = 1
    
    while True:
      params = {'per_page': per_page, 'page': page}
      response = requests.get(url, params=params)

      if response.status_code == 200:

          posts = response.json()
          if not posts:
              break

          for post in posts:
              print(f"Title: {post['title']['rendered']}")
              
              tags = ','.join(str(tag) for tag in post['tags'])
              categories = ','.join(str(category) for category in post['categories'])
                
              Post.objects.update_or_create(
                  defaults={
                      'post_id': post['id'],
                      'post_title': post['title']['rendered'],
                      'post_content': post['content']['rendered'],
                  },
                  post_id=post['id'],
                  post_title=post['title']['rendered'],
                  post_content=post['content']['rendered'],
                  tags=tags,
                  categories=categories,
              )

          page += 1
      else:
          print(f"Failed to fetch custom data: {response.status_code}")
          break


    
  