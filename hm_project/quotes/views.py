from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from .utils import get_mongodb
from django.shortcuts import get_object_or_404
from .models import Author, Quote



def main(request, page=1):
    quotes = Quote.objects.all().select_related('author').prefetch_related('tags').order_by('created_at')
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})
    # db = get_mongodb()
    # quotes = db.quotes.find()
    # per_page = 10
    # paginator = Paginator(list(quotes), per_page)
    # quotes_on_page = paginator.page(page)
    # return  render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    quotes = author.quote_set.all()   # type: ignore
    return render(request, "quotes/author_detail.html", {"author": author, "quotes": quotes})



@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quotes:root")
    else:
        form = AuthorForm()

    return render(request, "quotes/add_author.html", {"form": form})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quotes:root")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})
