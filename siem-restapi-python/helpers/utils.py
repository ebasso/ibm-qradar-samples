def get_date_string(timestamp_ms):
    from datetime import datetime
    if timestamp_ms == 0:
        return ""

    timestamp_s = timestamp_ms / 1000
    dt = datetime.fromtimestamp(timestamp_s) 
    return dt.strftime("%d/%m/%Y")
