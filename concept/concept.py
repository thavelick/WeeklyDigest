import datetime
import feedparser
import requests
from dateutil.parser import parse
from readability import Document

def rss_to_items(feed_urls, since):

    for url in feed_urls:
        feed = feedparser.parse(url)

    if not feed.get('items'):
        return

    items = []
    for item in feed['items']:
        items.append(item)

    return sorted(items,key=lambda x: parse(x.published))

def rss_to_article_urls(feed_urls, since):
    return [item.link for item in rss_to_items(feed_urls, since)]


def rss_to_html(feed_urls, since):
    html = ""
    for url in rss_to_article_urls(feed_urls):
        response = requests.get(url)
        doc = Document(response.text)

        html += "<h1>" + doc.title() + "</h1>"
        html += doc.summary(html_partial=True)

    return html

week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
html = rss_to_html(["https://feeds.feedburner.com/mrmoneymustache.xml"], week_ago)
print(html)
