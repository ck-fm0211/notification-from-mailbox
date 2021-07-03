# notification-from-mailbox
notification from mailbox usin SORACOM funk

# Requirement
## Runtime
- Python3.9.5

## Library
- requests==2.25.1

## Platform
- [SORACOM LTE-M Button Plus](https://soracom.jp/store/5207/)
- [SORACOM funk](https://soracom.jp/services/funk/)
- GCP Cloud Functions
- Slack
- LINE

# Usage
## Environment
write [env.yaml](./env.yaml)
- `SLACK_TOKEN`
- `SLACK_CHANNEL`
- `LINE_ACCESS_TOKEN`

### How To Get SLACK_TOKEN
- https://www.whizz-tech.co.jp/5857/

### How To Get LINE_ACCESS_TOKEN
- https://rooter.jp/web-crawling/line-notify_with_python/

# Deploy
```Shell
FUNCTION_NAME=notify_from_mailbox
gcloud functions deploy ${FUNCTION_NAME} \
--region asia-northeast1 \
--runtime python39 \
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
SLACK_CHANNEL=xxx \
SLACK_TOKEN=xxx \
LINE_ACCESS_TOKEN=xxx \
functions_framework --target=notify_from_mailbox

# other window
curl -X POST -H 'Content-Type: application/json' \
-d '{"clickType": 3,"batteryLevel":1}}' \
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
