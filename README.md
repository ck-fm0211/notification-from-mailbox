# notification-from-mailbox
notification from mailbox usin SORACOM funk

# Requirement
## Runtime
- Python3.12.8

## Library
- requests==2.25.1

## Platform
- [SORACOM LTE-M Button Plus](https://soracom.jp/store/5207/)
- [SORACOM funk](https://soracom.jp/services/funk/)
- Google Cloud Cloud Run Functions
- LINE Messaging API

# Usage
## Environment
write [env.yaml](./env.yaml)
- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_GROUP_ID`

### How To Get SLACK_TOKEN
- https://www.whizz-tech.co.jp/5857/

### How To Get LINE_ACCESS_TOKEN
- https://rooter.jp/web-crawling/line-notify_with_python/

# Deploy
```Shell
FUNCTION_NAME=notify_from_mailbox
gcloud functions deploy ${FUNCTION_NAME} \
--region asia-northeast1 \
--runtime python312 \
--trigger-http \
--allow-unauthenticated \
--env-vars-file=env.yaml \
--memory 128MiB
```

# Test
using [functions_framework](https://cloud.google.com/functions/docs/running/function-frameworks?hl=ja)
```Shell
# install
pip install functions_framework

# execute
LINE_CHANNEL_ACCESS_TOKEN=xxx \
LINE_GROUP_ID=xxx \
functions_framework --target=notify_from_mailbox

# other window
curl -X POST -H 'Content-Type: application/json' \
-d '{"clickType": 3,"batteryLevel":1}' \
"http://localhost:8080"
```

# SORACOM Func Data Format
https://users.soracom.io/ja-jp/docs/funk/format/
```json
{
    "method": "POST",
    "body":  {
        "clickType": 1,
        "clickTypeName": "SINGLE",
        "batteryLevel": 1,
        "binaryParserEnabled": true},
    "headers": {
        "user-agent": "SORACOM Funk",
        "content-type": "application/json",
        "x-soracom-token": "JWT Token"
    }
}
```

## ClickType
https://users.soracom.io/ja-jp/guides/iot-devices/lte-m-button-enterprise/device-setting/#%E3%83%A1%E3%83%BC%E3%83%AB%E9%80%81%E4%BF%A1%E3%81%AE%E8%A8%AD%E5%AE%9A
- 1: Single Click
- 2: Double Click
- 3: Long Click

## batteryLevel
https://users.soracom.io/ja-jp/guides/iot-devices/lte-m-button-enterprise/device-setting/#%E3%83%A1%E3%83%BC%E3%83%AB%E9%80%81%E4%BF%A1%E3%81%AE%E8%A8%AD%E5%AE%9A
- 0.25
- 0.5
- 0.75
- 1.0

# LINE Messaging API
## Getting User ID (or Group ID)

- Deploy the following JavaScript code as a web application using Google Apps Script, and register it as a webhook in the LINE Developers console.
- Send a message from LINE and identify the User ID or Group ID included in the response.

```javascript
// LINE Messaging API Channel Access Token
var ACCESS_TOKEN = 'xxx';

function doPost(e) {
  console.log(e)
  var event = JSON.parse(e.postData.contents).events[0];

  var replyToken = event.replyToken;

  var type = event.source.type;

  if (type == 'user') {
    var id = event.source.userId;
  } else if (type == 'group') {
    var id = event.source.groupId;
  } else if (type == 'room') {
    var id = event.source.roomId;
  }

  var url = 'https://api.line.me/v2/bot/message/reply';

  var payload = {
    'replyToken': replyToken,
    'messages': [
      {
        'type': 'text',
        'text': type + '_id = '+ id
      }
    ]
  };

  var options = {
    'method': 'post',
    'headers': {
      'Content-Type': 'application/json; charset=UTF-8',
      'Authorization': 'Bearer ' + ACCESS_TOKEN,
    },
    'payload' : JSON.stringify(payload)
  };

  UrlFetchApp.fetch(url, options)
}

```
