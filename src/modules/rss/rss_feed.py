import time
import os
import pickle
from typing import Dict, List
import hashlib
import requests
import feedparser
import logging
from ..module_cache import ModuleCache

class RSSFeed:
    def __init__(self, url, max_items=5, default_seconds_refresh_time=3600, cache_path: str = None):
        """
        Initializes the RSSFeed object with the URL of the RSS feed and other configurations.

        :param url: The URL of the RSS feed.
        :param max_items: The maximum number of items to retrieve from the feed (default is 5).
        :param default_seconds_refresh_time: The time in seconds between feed refreshes (default is 3600 seconds = 1 hour).
        """
        self._url = url
        self._max_items = max_items
        self._default_seconds_refresh_time = default_seconds_refresh_time
        self._last_refresh_timestamp = 0
        if cache_path != None:
            self._cache = ModuleCache(cache_path = f"{cache_path}/rss/{hashlib.sha256(self._url.encode('utf-8')).hexdigest()}.rss",  expire_seconds = default_seconds_refresh_time, purge_expired = True)
        else:
            self._cache = None
        self._feed_title = ''
        self._feed_items = []
        self._feed_hash = ''
        logging.basicConfig(level=logging.INFO)

    def _regenerate_feed_entries_hash(self, feed_entries) -> str:
        """
        Generates a consistent hash based on the unique identifiers (e.g., 'link' or 'guid') of the feed entries.

        :param feed_entries: A list of feed entry dictionaries to hash.
        :return: A SHA-256 hash string representing the feed entries.
        """
        feed_hash = hashlib.sha256()  # Create a new hash object
        for entry in feed_entries:
            feed_hash.update(entry.get("link", "").encode('utf-8'))  # Update the hash with the entry's link
        return feed_hash.hexdigest()  # Return the hex digest of the hash

    def _refresh(self, force: bool = False) -> bool:
        """
        Refreshes the RSS feed by fetching it from the provided URL and parsing the entries.

        :param force: Whether to force refresh the feed (ignoring the refresh time).
        :return: True if the feed was updated, False if the feed is unchanged.
        """

        parsed_feed = None
        if self._cache != None:
            parsed_feed = self._cache.load()

        if parsed_feed == None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0'
            }

            try:
                response = requests.get(self._url, headers=headers, timeout=10)  # Fetch the feed with a timeout
                response.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
            except requests.exceptions.RequestException as e:
                raise RuntimeError(f"Error while fetching RSS feed: {str(e)}")

            parsed_feed = feedparser.parse(response.text)

            if self._cache != None:
                self._cache.save(parsed_feed)

        self._feed_title = parsed_feed.feed.title  # Store the feed title
        self._feed_items = []  # Reset the feed items

        # Ensure that 'entries' contains valid data
        if hasattr(parsed_feed, 'entries') and parsed_feed.entries:
            for entry in parsed_feed.entries[:self._max_items]:
                # Simplify each entry and append it to the feed items
                simplified_item = {
                    'link': entry.get('link', ''),
                    'title': entry.get('title', ''),
                    'published': entry.get('published', ''),
                    'author': entry.get('author', '')
                }
                self._feed_items.append(simplified_item)
        else:
            raise ValueError("The RSS feed does not contain valid entries.")

        # Generate a hash for the current feed items
        current_feed_hash = self._regenerate_feed_entries_hash(self._feed_items)

        # Compare the new hash with the previous hash to check if the feed content has changed
        if current_feed_hash != self._feed_hash:
            self._feed_hash = current_feed_hash  # Update the feed hash if it's different
            return True  # Return True to indicate the feed has changed
        else:
            return False  # Return False to indicate no change in the feed

    def get(self, force: bool = False) -> Dict[str, List[Dict[str, str]]]:
        """
        Returns the latest RSS feed data. If the feed hasn't been refreshed recently, it will refresh the feed.

        :param force: Whether to force refresh the feed even if the refresh time hasn't passed.
        :return: A dictionary containing the feed status, title, and items.
        """

        changed = False
        current_time = time.time()  # Get the current time in seconds since the epoch
        if force or current_time - self._last_refresh_timestamp >= self._default_seconds_refresh_time:
            try:
                changed = self._refresh(force)  # Refresh the feed and check if it changed
                self._last_refresh_timestamp = current_time  # Update the timestamp of the last refresh
            except Exception as e:
                raise RuntimeError(f"Error while refreshing RSS feed: {str(e)}")

        # Return the feed status and content
        return {
            "changed": changed,
            "title": self._feed_title,
            "items": self._feed_items
        }
