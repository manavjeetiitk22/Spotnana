from datetime import datetime
from zoneinfo import ZoneInfo

def to_utc(local_time_str, timezone):
    tz = ZoneInfo(timezone)
    local_dt = datetime.fromisoformat(local_time_str).replace(tzinfo=tz)
    return local_dt.astimezone(ZoneInfo("UTC"))

# def local_date_from_utc(utc_dt, timezone):
#     return utc_dt.astimezone(ZoneInfo(timezone)).date().isoformat()

def format_layover(td):
    minutes = int(td.total_seconds() // 60)
    h = minutes // 60
    m = minutes % 60
    return f"{h}h {m}m"