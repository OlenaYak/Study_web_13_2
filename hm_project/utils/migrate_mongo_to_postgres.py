import django
import os
import sys

from bson import ObjectId

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hm_project.settings')
django.setup()

from quotes.models import Author, Quote, Tag
from quotes.utils import get_mongodb


def migrate():
    db = get_mongodb()

    
    authors_collection = db.authors
    mongo_authors = {}

    for author_data in authors_collection.find():
        author, created = Author.objects.get_or_create(
            fullname=author_data.get('fullname'),
            defaults={
                'born_date': author_data.get('born_date'),
                'born_location': author_data.get('born_location'),
                'description': author_data.get('description', ''),
            }
        )
        if created:
            print(f"[✔] Created author: {author.fullname}")

        
        mongo_authors[str(author_data['_id'])] = author

    
    tags_collection = db.tags
    for tag_data in tags_collection.find():
        tag_name = tag_data.get('name')
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            print(f"[✔] Created tag: {tag.name}")

    
    quotes_collection = db.quotes
    for quote_data in quotes_collection.find():
        author_id = quote_data.get('author')  # це ObjectId
        author = mongo_authors.get(str(author_id))  

        if not author:
            print(f"[!] Автор з ID {author_id} не знайдений, пропускаю цитату.")
            continue

        quote_text = quote_data.get('quote')
        quote = Quote.objects.create(quote=quote_text, author=author)

        tags_names = quote_data.get('tags', [])
        for tag_name in tags_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)

        quote.save()
        print(f"[✔] Created quote: {quote_text[:50]}...")

if __name__ == '__main__':
    migrate()

