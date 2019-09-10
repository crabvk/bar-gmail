# Privacy Policy

## Introduction

This privacy policy will help you understand what information we collect with Polybar Gmail, how Polybar Gmail uses it, and what information you share.  
"We" here means I, the developer of Polybar Gmail, and all its [collaborators](https://github.com/vyachkonovalov/polybar-gmail/graphs/contributors).

## Information we receive and collect

### Google Customer Data

As result of authenticating a Google Account with Polybar Gmail, we store and utilize Google Application Credentials and expiration values. We use this credentials to retrieve email data via the Google Gmail API.

### Google OAuth Scopes

When authenticating a Google Account with Polybar Gmail, we request the use of https://www.googleapis.com/auth/gmail.labels OAuth scope. This scope is needed in order to read the count of unread Inbox messages on your Gmail account. The reading of this information is done via [the official Python client library](https://github.com/googleapis/google-api-python-client).

## How we use your information

We get the count of unread messages in your Inbox, which intended to display in a [Polybar](https://github.com/polybar/polybar) bar. Eventually, this count is stored on your computer in temporary memory (RAM) for about 10 seconds, except for the case when internet connection is lost then this time can be exceeded.

## Sharing and Disclosure

We don't share your information with anyone except you.
