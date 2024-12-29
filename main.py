import os
from datetime import datetime, timedelta, timezone

import requests
from flask import Response


def notify_from_mailbox(request):
    JST = timezone(timedelta(hours=+9), "JST")
    dt_now = datetime.now(JST)

    if request.method != "POST":
        print(f"This is not post request: {request.method}")
        return Response(response=f"This is not post request: {request.method}", status=400)

    request_dict = request.get_json()

    # バッテリー情報を取得する
    if request_dict["batteryLevel"] >= 0.5:
        battery_notification = "バッテリー残量は充分です"
    else:
        battery_notification = "そろそろバッテリーが切れます"

    notify_message = (
        "ポストに投函がありました。\n"
        + f"投函時刻：{dt_now.strftime('%Y年%m月%d日 %H:%M:%S')}\n"
        + f"{battery_notification}\n"
        + f"<debug> clickType: {request_dict['clickType']}"
    )

    # LINEへ通知
    headers = {
        "Authorization": f"Bearer {os.environ['LINE_ACCESS_TOKEN']}",
    }

    files = {
        "message": (None, notify_message),
    }

    line_res = requests.post("https://notify-api.line.me/api/notify", headers=headers, files=files)

    return {"line": line_res.json()}
