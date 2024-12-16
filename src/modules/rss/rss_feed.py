import time
import feedparser
import requests
from typing import List, Dict, Any

class RSSFeed:
    """
    A class to manage an RSS feed, allowing updates, access to article details, and detection of feed changes.
    """

    def __init__(self, url: str, default_seconds_refresh_time: int = 600, max_items: int = 16):
        self._url = url
        self._default_seconds_refresh_time = default_seconds_refresh_time
        self._last_refresh_timestamp = time.time()
        self._max_items = max_items
        self._changed = False
        self._feed_title = None
        self._feed_items = []
        self._feed_hash = None

    def _regenerate_feed_entries_hash(self, feed_entries) -> str:
        """
        Generates a hash based on the unique identifiers (e.g., 'link' or 'guid') of the feed entries.

        :param feed_entries: List of feed entries (articles).
        :return: A string hash representing the feed.
        """
        feed_hash = ""
        for entry in feed_entries:
            feed_hash += entry.get("link", "")  # You could also use "guid" here, depending on the feed structure.
        return hash(feed_hash)

    def _refresh(self, force: bool = False) -> bool:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0'
        }
        response = requests.get(self._url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an error if the response is not successful

        parsed_feed = feedparser.parse(response.text)

        self._feed_title = parsed_feed.feed.title
        self._feed_items = []
        for entry in parsed_feed.entries[:self._max_items]:
            simplified_item = {
                'link': entry.get('link', ''),
                'title': entry.get('title', ''),
                'published': entry.get('published', ''),
                'author': entry.get('author', '')
            }
            self._feed_items.append(simplified_item)

        current_feed_hash = self._regenerate_feed_entries_hash(self._feed_items)

        if current_feed_hash != self._feed_hash:
            self._feed_hash = current_feed_hash
            return True
        else:
            return False

    def get(self, force: bool = False):
        # TODO: this property declared on interface/base module class
        self._changed = False
        current_time = time.time()
        if force or current_time - self._last_refresh_timestamp >= self._default_seconds_refresh_time:
            try:
                self._changed = self._refresh(force)
                self._last_refresh_timestamp = current_time

            except Exception as e:
                raise RuntimeError(f"Error while refreshing RSS feed: {str(e)}")

        return {
            "changed" : self._changed,
            "title": self._feed_title,
            "items": self._feed_items
        }
