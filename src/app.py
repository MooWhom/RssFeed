import boto3
import feedparser
import requests
import os
from dotenv import load_dotenv

from datetime import datetime, timezone

load_dotenv()

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

rss_feeds = {
    "MacRumors": {
        "rss_link": "http://feeds.macrumors.com/MacRumors-All"
    },
}

# Use ssm to store last-posted data.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('rssfeeds')

def generate_ai_summary(link: str):
    pass

def generate_discord_embed(link: str):
    embed = {
        "content": link
    }
    
    return embed

def send_discord_message(feed_name: str, embed): 
    if (feed_name not in rss_feeds):
        return None

    response = requests.post(
        WEBHOOK_URL, embed
    )

    # Only successful sends return a 'true' status.
    return (response.status_code == 204)

def process_feeds():
    for feed_name, feed_data in rss_feeds.items():
        last_pub_date = retrieve_datetime_for_parameter(feed_name)
        # If this feed has not been seen before, only send posts created after this invocation. 
        if (not last_pub_date):
            set_datetime_for_parameter(feed_name, datetime.now(timezone.utc))
            break

        rss_link = feed_data["rss_link"]
        rss_feed = feedparser.parse(rss_link)

        new_entries = list(filter(
            lambda entry: convert_pub_string_to_datetime(entry.published) > last_pub_date, 
            rss_feed.entries
        ))

        # Reverse so that the newest post is sent last.
        new_entries.reverse()
        
        for entry in new_entries:
            embed = generate_discord_embed(entry.link)
            did_send = send_discord_message(feed_name, embed)

            # Failure to send may indicate a rate limit. We can attempt the next time the script runs, 
            # so we'll return entirely to avoid further rate limiting.
            if (not did_send):
                return

            entry_published_date = convert_pub_string_to_datetime(entry.published)

            # Entries here always exceed 'last_pub_date' as well as the previous entry,
            # but we'll be safe and check anyway.
            if (entry_published_date > last_pub_date):
                # Since it was successfully posted to the webhook, update 'last_pub_date'
                # to stop this from being posted again.
                set_datetime_for_parameter(feed_name, entry_published_date)

# -- MARK: Helper functions
def convert_pub_string_to_datetime(date: str):
    return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc)

def set_datetime_for_parameter(feed_name: str, date: datetime):
    # Failure here could result in duplicate posts.
    table.put_item(
        Item = {
            'feed': feed_name,
            'datetimeValue': date.isoformat()
        }
    )

def retrieve_datetime_for_parameter(feed_name: str) -> datetime | None:
    response = table.get_item(
        Key = {
            'feed': feed_name
        }
    )

    datetimeValue = response.get('Item', {}).get('datetimeValue', None)
    if (datetimeValue):
        return datetime.fromisoformat(datetimeValue)
    else:
        return None

def lambda_handler(event, context):
    process_feeds()
    return {
        'statusCode': 200
    }

if __name__ == "__main__":
    process_feeds()