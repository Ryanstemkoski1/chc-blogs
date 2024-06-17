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
  help ="tags"
  
  def handle(self, *args, **options):
    posts = FailedPost.objects.all()
    orginals = [112, 237, 254, 217, 200, 259, 345, 188, 347, 329, 130, 115, 147, 238, 201, 277, 263, 295, 270]
    newposts = []
    
    for post in posts:
      op = Post.objects.get(post_id = post.post_id)
      cats = op.categories
      cats = cats.split(',')
      
      for cat in cats:
        if int(cat) in orginals:
          newposts.append(post.post_id)
          break
        
    print(newposts)
    
      
    