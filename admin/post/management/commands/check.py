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
        # posts = Post.objects.all()
        posts = Post.objects.all().filter(post_content__isnull=False)[1300: 1950]
        for post in posts:
            print(post.post_title)
            content = post.post_content
            soup = BeautifulSoup(content, 'lxml')
            img_tags = soup.find_all('img')
            failed = False
            for img in img_tags:
                if 'src' in img.attrs:
                    url = img['src']
                    if "childrenshealthcouncil.kinsta.cloud" not in url:
                        url = f'https://childrenshealthcouncil.kinsta.cloud{url}'
                    invalid_image = False
                    try:
                        response = requests.head(url, timeout=1)
                        if response.status_code != 200:
                            invalid_image = True
                    except requests.exceptions.RequestException:
                        invalid_image = True

                    if invalid_image:
                        new_img_url = self.get_valid_image_url(url, post.post_id)
                        if new_img_url is None:
                            failed = True
                            break
                        img['src'] = new_img_url

            if failed:
              UnCompletedPost.objects.update_or_create(
                  defaults={
                      'post_id': post.post_id,
                      "post_content": content
                  },
                  post_title=post.post_title,
                  post_id=post.post_id
              )
            else:
              new_content = str(soup).replace("<html>", "").replace("<body>", "").replace("</body>", "").replace("</html>", "")
              CompletedPost.objects.update_or_create(
                  defaults={
                      'post_id': post.post_id,
                      "post_content": new_content
                  },
                  post_title=post.post_title,
                  post_id=post.post_id
              )

    def get_valid_image_url(self, url, post_id):
        image_name = url.split('/')[-1]
        name, _ext = os.path.splitext(image_name)
        clean_name = re.sub(r'-\d+x\d+$', '', name)
        url = None
        response = requests.get(MEDIA_URL, params={'search': clean_name})
        if response.ok:
            medias = response.json()
            post_medias = [m for m in medias if m['post'] == post_id]
            if len(post_medias) > 0:
                url = post_medias[0]['source_url']
            elif len(medias) > 0:
                url = medias[0]['source_url']
            else:
                url = None
        if url is not None:
            print(f"[Post: {post_id}], Found url: {url} for image: {name}, clean name: {clean_name}")
        else:
            print(f"[Post: {post_id}], Failed to find url for image: {name}, clean name: {clean_name}")
        return url
