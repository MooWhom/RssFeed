# RssFeed

A simple AWS Lambda setup to listen for new posts to a set of RSS feeds. Each new found post in each feed is sent to a pre-defined Discord webhook. This project uses a SAM template to configure an AWS Lambda function that stores the date of the article it last posted from each configured feed in a DynamoDB database. The default configuration uses a CloudWatch Events (EventBridge) timer trigger set to three minutes to call the function every three minutes.

## Deployment

Using SAM, simply run:

- `sam build`
- `sam deploy` 


## Environment variables

- `WEBHOOK_URL` - the webhook to post embeds to.

## Adding new feeds
To add a new feed to be listened to, simply insert a new entry into the `rss_feeds` dictionary inside `process_feeds.py`. Any feed removed from the script will have a last published date persisted in the DynamoDB table.