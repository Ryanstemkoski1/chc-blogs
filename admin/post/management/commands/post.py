import os
import os

import requests
from django.core.management.base import BaseCommand
from requests.auth import HTTPBasicAuth

from post.models import Post

FILEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

url = 'https://childrenshealthcouncil.kinsta.cloud/wp-json/wp/v2/posts'
auth = HTTPBasicAuth('ryan.stemkoski@abectech.com', '5Xh2BoSeqQfUi^(z')


class Command(BaseCommand):
    help = 'API'

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

                    Post.objects.update_or_create(
                        defaults={
                            'post_id': post['id'],
                            'post_title': post['title']['rendered'],
                            'post_content': post['content']['rendered'],
                        },
                        post_id=post['id'],
                        post_title=post['title']['rendered'],
                        post_content=post['content']['rendered'],
                    )

                page += 1
            else:
                print(f"Failed to fetch custom data: {response.status_code}")
                break
