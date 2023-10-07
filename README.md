# RssFeed

A simple AWS Lambda setup to listen for new posts to a set of RSS feeds. Each new found post in each feed is sent to a pre-defined Discord webhook.

RssFeed uses AWS's DynamoDB to store data about the last-posted link of a specific feed. This allows the script to remember where it last left off between invocations, and prevents duplciate posts being sent.

The Lambda should be triggered on a set schedule. For timely updates, a period of about 2/3 minutes is recommended. This also ensures executions remain in the free period tier.

## Deployment

### DynamoDB
A DynamoDB table called `rssfeed` must exist. The primary key is `feed`, which associates a string of the time the last published entry of each feed was created to said feed. 

### Lambda


## Environment variables

- `WEBHOOK_URL` - the webhook to post embeds to.

## Adding new feeds
To add a new feed to be listened to, simply insert a new entry into the `rss_feeds` dictionary inside `process_feeds.py`. Any feed removed from the script will have a last published date persisted in the DynamoDB table.