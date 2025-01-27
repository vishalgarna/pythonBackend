from pushbullet import PushBullet


def send_notification(title , body):
    api_key = 'o.HJz6kWyCg6seJHhL68FxEM3OVI6AgB7i'
    pb = PushBullet(api_key)
    pb.push_note(title, body)





