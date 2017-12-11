# coding=utf-8
import json
import requests
import time

# Your Spark Developer token
myToken = "__YOUR_TOKEN_HERE__"

# Your Spark Space ID
myRoom = "__YOUR_SPACE_ID_HERE__"

# maxMessagesPerRun=400 and maxRuns=10 ---> will retrieve a maximum of 10*400 = 4,000 messages
# Do not set maxMessagesPerRun > 500
maxMessagesPerRun = 400     # number of messages retrieved per batch
maxRuns = 10                # the number of runs
maxWaitTime = 5             # Number of seconds before starting the next batch


def get_messages(sparktoken, sparkspaceid):
    headers = {'Authorization': 'Bearer ' + sparktoken, 'content-type': 'application/json; charset=utf-8'}
    payload = {'roomId': sparkspaceid, 'max': maxMessagesPerRun}
    JSONdata = list()   # all message (dictionaries) are stored in a list:
    currentRun = 0
    while currentRun < maxRuns:  # for each batch of messages to be retrieved:
        currentRun += 1
        try:    # Get Spark messages (with 'max' set to the variable 'maxMessagesPerRun' (per batch))
            result = requests.get('https://api.ciscospark.com/v1/messages', headers=headers, params=payload)
        except requests.exceptions.RequestException as e:
            print(" **  WARNING: An error occurred " + e)
            break
        try:
            # Add new messages to the JSON list:
            JSONdata.extend(json.loads(result.text)['items'])

            # Get the oldest message ID of this run. This is where we start our next run.
            myBeforeMessage = result.headers.get('Link').split("beforeMessage=")[1].split(">")[0]

            # Change the Spark GET request message to include the (updated) last message ID:
            payload = {'roomId': sparkspaceid, 'max': maxMessagesPerRun, 'beforeMessage': myBeforeMessage}

            # Print the progress:
            print(" run: " + str(currentRun) + " --- total number of retrieved messages: " + str(len(JSONdata)))

            # Wait x number of seconds before retrieving more messages
            print("             ... waiting " + str(maxWaitTime) + " seconds before next API call ... \n")
            time.sleep(maxWaitTime)
        except:
            break
    return JSONdata


print("\n\n -------------------- START ----------------------------\n ")

SparkMessages = get_messages(myToken, myRoom)

print("\n number of messages retrieved: " + str(len(SparkMessages)))

print("\n\n -------------------- finished ----------------------------\n\n ")

# If you want "proof" of messages retrieved, remove the exit() command below to
#   print the email addresses + date/time of every message.
exit()

for msg in SparkMessages:
    try:
        if 'personEmail' in msg:  # double checking if the 'personEmail' field exists
            print("  message from > " + str(msg['personEmail']) + "  -- created: " + msg['created'])
    except:
        print(" **ERROR** printing messages")

print("\n -------------------- finished ----------------------------\n\n ")
