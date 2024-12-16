import time
import feedparser
import requests
from typing import List, Dict, Any

class RSSFeed:
    """
    A class to manage an RSS feed, allowing updates, access to article details, and detection of feed changes.
    """

    def __init__(self, url: str, default_seconds_refresh_time: int = 600, max_items: int = 16):
        """
        Initializes the RSSFeed object.

        :param url: The URL of the RSS feed.
        :param default_seconds_refresh_time: Time in seconds between automatic refreshes.
        :param max_items: Maximum number of items to return per refresh.
        """
        self._url = url
        self._default_refresh_time = default_seconds_refresh_time
        self._max_items = max_items
        self._last_refresh_timestamp = time.time()
        self._feed_entries = []
        self._last_feed_hash = None

    @property
    def url(self) -> str:
        return self._url

    @property
    def default_refresh_time(self) -> int:
        return self._default_refresh_time

    @property
    def max_items(self) -> int:
        return self._max_items

    @property
    def last_refresh_timestamp(self) -> float:
        return self._last_refresh_timestamp

    def _generate_feed_hash(self, feed_entries) -> str:
        """
        Generates a hash based on the unique identifiers (e.g., 'link' or 'guid') of the feed entries.

        :param feed_entries: List of feed entries (articles).
        :return: A string hash representing the feed.
        """
        feed_hash = ""
        for entry in feed_entries:
            feed_hash += entry.get("link", "")  # You could also use "guid" here, depending on the feed structure.
        return hash(feed_hash)  # Generate a simple hash of the links

    def refresh(self, force: bool = False) -> Dict[str, Any]:
        """
        Refreshes the RSS feed. If it's not necessary to refresh, returns the stored titles and metadata.

        :param force: If True, forces the feed to refresh regardless of time passed.
        :return: A dictionary with 'error' (boolean), 'changed' (boolean) and 'articles' (list of article details).
        """
        current_time = time.time()
        result = {
            "error": False,    # Default is no errors
            "changed": False,  # Default is no change
            "articles": []     # Empty list of articles initially
        }

        if force or current_time - self._last_refresh_timestamp >= self._default_refresh_time:
            try:
                # Using requests to fetch the RSS feed
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0'
                }
                response = requests.get(self._url, headers=headers, timeout=10)
                response.raise_for_status()  # Raises an error if the response is not successful

                # Parse the feed with feedparser
                feed = feedparser.parse(response.text)
                self._last_refresh_timestamp = current_time

                # Prepare the list of articles
                self._feed_entries = feed.entries[:self._max_items]

                # Compare the current feed hash with the last one
                current_feed_hash = self._generate_feed_hash(self._feed_entries)

                # If the feed has changed, update the entries and hash
                result["changed"] = current_feed_hash != self._last_feed_hash
                self._last_feed_hash = current_feed_hash

            except requests.exceptions.RequestException as e:
                result["error"] = True
                print(f"Error fetching RSS feed: {e}")
                result["error_message"] = str(e)
            except Exception as e:
                result["error"] = True
                print(f"Unexpected error: {e}")
                result["error_message"] = str(e)
        # Prepare the list of articles with the requested details
        result["articles"] = [
            {
                "link": entry.get("link", ""),
                "title": entry.get("title", ""),
                "published": entry.get("published", ""),
                "author": entry.get("author", "")
            }
            for entry in self._feed_entries
        ]
        return result
