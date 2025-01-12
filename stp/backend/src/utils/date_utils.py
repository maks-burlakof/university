from datetime import datetime


def get_str_time(self):
    days = (datetime.now().astimezone() - self.created).days
    if days == 0:
        seconds = (datetime.now().astimezone() - self.created).seconds
        if 0 <= seconds < 5:
            return "только что"
        if seconds < 60:
            return f"{seconds} сек."
        elif 0 < seconds // 60 < 60:
            return f"{seconds // 60} мин."
        else:
            return f"{seconds // 60 // 60} ч."
    elif days == 1:
        return "Вчера"
    elif days == 2:
        return "Позавчера"
    else:
        return f"{days} дн."
