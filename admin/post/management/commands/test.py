from django.core.management.base import BaseCommand
import requests
from requests.auth import HTTPBasicAuth
import base64
from bs4 import BeautifulSoup
import os
import re

from post.models import CompletedPost, Uploadfaild

# WordPress user credentials
wp_user = 'ryan.stemkoski@abectech.com'
wp_password = 'Ltr1 Lw9A wNEf aNrI zKsT AnL5'

headers = {
    'Authorization': 'Basic ' + base64.b64encode(f'{wp_user}:{wp_password}'.encode()).decode(),
    'Content-Type': 'application/json'
}


class Command(BaseCommand):
  help = "Image"
  
  def handle(self, *args, **options):
    # posts = CompletedPost.objects.all()[100:2000]
      # post = CompletedPost.objects.get(post_id=8288)
      post = CompletedPost.objects.get(post_title='Life Skills for Teens and Healthy Lifestyle Tips [web resource]')
      print(post.post_title)
    # for post in posts:
      wordpress_url = f'https://childrenshealthcouncil.kinsta.cloud/wp-json/wp/v2/posts/{post.post_id}'
      payload = {
          'content': post.post_content
      }
      
      response = requests.post(wordpress_url, headers=headers, json=payload)
      
      if response.status_code == 200:
          print('Post updated successfully.')
      else:
          print('Failed to update post.')
          Uploadfaild.objects.update_or_create(
            defaults={
                'post_id': post.post_id,
                "post_content": post.post_content
            },
            post_title=post.post_title,
            post_id=post.post_id
          )
          
    # print("completed")