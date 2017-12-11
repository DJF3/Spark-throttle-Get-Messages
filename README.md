# Cisco Spark - Getting a large number of messages.

If you want to get a large number of messages from a Cisco Spark Space, you can't 
send out a single request saying: 
> "I want 20,000 messages".

This example doesn't wait for a "`429 Too many requests`" error, it just doesn't push the API's a lot.


## Q: How _do_ you get 20,000 messages?

Requesting them in Batches. Read 400 messages, wait 5 seconds, read 400 messages, etc.


## Q: After getting the first messages, how do you know _where_ to start with your next batch?

The HTTP header returned with the first (say 400) messages has a field: `Link`.
```
Link →<https://api.ciscospark.com/v1/messages
     ?roomId=Y2lzY29zcGFyazovL3VzL1JPT00vNDNiMTRmYWYtNjQ1OC0zOTJkLWFhMzgtNDNjYjcwMDI1Zjg3
     &max=50
     &beforeMessage=Y2lzY29zcGFyazovL3VzL01FU1NBR0UvYTgwMDJlZTAtMzE5Mi0xMWU3LTg4YjEtODk4YmNmMDc0OWM0>; rel="next">
```
The field "`BeforeMessage`" has the _message ID_ of the last message retrieved. 
In subsequent API calls you tell Spark to return messages _starting_ with the `BeforeMessage` message ID.


# Requirements
- Python 3.x
- Python Requests library


# A different approach
getting messages until you hit an HTTP 429 error. When you hit a '429', the HTML header 
will have a `retry-after` field indicating how long you have to wait before you can send your next request. 
Info on dealing with HTTP error 429:  [Spark Developer Blog](https://developer.ciscospark.com/blog/blog-details-8193.html)


Enjoy.
