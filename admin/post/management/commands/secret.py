import os
import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from post.models import Post, UnCompletedPost, CompletedPost

MEDIA_URL = "https://childrenshealthcouncil.kinsta.cloud/wp-json/wp/v2/media"


class Command(BaseCommand):
    help = "DB"

    def handle(self, *args, **options):
      posts = CompletedPost.objects.all()
      # post = CompletedPost.objects.get(post_title='The Emergent Bilingual Experience')
      for post in posts:
        print(post.post_id)
        content = post.post_content
        soup = BeautifulSoup(content, 'lxml')
        img_tags = soup.find_all('img')
        sensitive_attributes = ['data-secret', 'secret', 'srcset']

        # Loop through each image tag and remove sensitive attributes
        for img in img_tags:
            for attr in sensitive_attributes:
                if attr in img.attrs:
                    del img.attrs[attr]
              
        new_content = str(soup).replace("<html>", "").replace("<body>", "").replace("</body>", "").replace("</html>", "")
        CompletedPost.objects.update_or_create(
          defaults={
              'post_id': post.post_id,
              "post_content": new_content
          },
          post_title=post.post_title,
          post_id=post.post_id
        )
      print("completed")