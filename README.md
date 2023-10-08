# RssFeed

A simple AWS Lambda setup to listen for new posts from a set of RSS feeds. Each new  post in each feed is sent to a pre-defined Discord webhook. This project uses a SAM template to configure an AWS Lambda function. To store the date of the article it last posted from each configured feed, the template includes a DynamoDB database. The default configuration uses a CloudWatch Events (EventBridge) timer trigger to call the function every three minutes.

## Deployment

Using SAM, simply run:

- `sam build`
- `sam deploy --parameter-overrides ParameterKey=WebhookUrl,ParameterValue=<your webhook URL>` 

## Environment variables

- `WEBHOOK_URL` - the webhook to post embeds to.

## Adding new feeds
To add a new feed to be listened to, simply insert a new entry into the `rss_feeds` dictionary inside `process_feeds.py`. Any feed removed from the script will have a last published date persisted in the DynamoDB table.
