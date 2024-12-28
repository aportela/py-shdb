from typing import Dict, List, Optional
import requests
import feedparser
from ...utils.logger import Logger

# Default user-agent string to be used in the HTTP request headers.
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0'

class RSSFeed:
    def __init__(self, url: str, timeout: int = 10) -> None:
        """
        Initializes the RSSFeed object with the URL of the RSS feed.

        :param url: The URL of the RSS feed to be fetched.
        :param timeout: Timeout duration for the HTTP request in seconds (default is 10 seconds).
        """
        self.__log = Logger()
        self.__url = url
        self.__timeout = timeout

    def get(self, url: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
        """
        Fetches the RSS feed, parses it, and returns a simplified dictionary containing
        the feed title and a list of parsed feed entries.

        :param url: The URL of the RSS feed to fetch. If None, the URL provided at initialization is used.
        :return: A dictionary containing the feed title and a list of feed items (each with link, title,
                 published date, and author).
        :raises RuntimeError: If there is an error in fetching or parsing the feed.
        :raises ValueError: If the feed does not contain valid entries.
        """
        # Use the provided URL or fall back to the default one initialized in the object
        feed_url = url or self.__url
        self.__log.info(f"Requesting RSS feed from {feed_url}")

        # Setting custom headers for the HTTP request (including the user-agent)
        headers = {
            'User-Agent': DEFAULT_USER_AGENT
        }

        try:
            # Make the HTTP request to fetch the feed
            response = requests.get(feed_url, headers=headers, timeout=self.__timeout)
            response.raise_for_status()  # Raise an exception for 4xx/5xx HTTP error codes

            # Verify that the content type of the response is actually an RSS feed (XML format)
            content_type = response.headers.get('Content-Type', None)
            if content_type is None or not (content_type.lower().startswith('application/rss+xml') or content_type.lower().startswith('text/xml')):
                raise ValueError(f"Expected RSS feed, but received {response.headers.get('Content-Type')}")

        except requests.exceptions.Timeout:
            # Log and raise an error if the request times out
            self.__log.error(f"Timeout occurred while requesting RSS feed from {feed_url}")
            raise RuntimeError("Request timed out while fetching RSS feed.")

        except requests.exceptions.RequestException as e:
            # Log and raise an error for other HTTP or request exceptions (e.g., connection errors)
            self.__log.error(f"Request error while fetching RSS feed: {str(e)}")
            raise RuntimeError(f"Error while fetching RSS feed: {str(e)}")

        # Parse the fetched RSS feed using feedparser
        parsed_feed = feedparser.parse(response.text)

        # Check if the parsed feed contains valid entries
        if hasattr(parsed_feed, 'entries') and parsed_feed.entries:
            items = []

            # Loop through each entry in the RSS feed and simplify the structure
            for entry in parsed_feed.entries:
                simplified_item = {
                    'link': entry.get('link', ''),       # Link to the full article or content
                    'title': entry.get('title', ''),     # Title of the feed item
                    'published': entry.get('published', ''),  # Publication date of the item
                    'author': entry.get('author', '')    # Author of the item (if available)
                }
                items.append(simplified_item)

            # Log the number of entries successfully parsed
            self.__log.info(f"Successfully parsed {len(items)} entries from {feed_url}")

            # Return the parsed feed title and the list of simplified items
            return {
                "title": parsed_feed.feed.title,  # Title of the RSS feed
                "items": items                    # List of simplified feed items
            }

        else:
            # Log a warning if the feed does not contain any valid entries
            self.__log.warning(f"The RSS feed from {feed_url} does not contain any valid entries.")
            raise ValueError("The RSS feed does not contain valid entries.")
