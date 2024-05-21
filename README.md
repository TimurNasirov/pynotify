First of all, create your api key on nta123.duckdns.org/pynotify/key?app=your_app_name (POST)

Then, create user which you want to send notifications on nta123.duckdns.org/pynotify/user?key=your_api_key&userid=user_telegram_id (POST)

Finally, send notification on nta123.duckdns.org/pynotify/notify?key=your_api_key&user=user_id(not telergram)&message=notification_content (POST)
