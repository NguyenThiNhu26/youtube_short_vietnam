from googleapiclient.discovery import build
import pandas as pd

API_KEY = "AIzaSyBHm2n2JfFVmDLgv1vGyOcOOZPhIeUR62U"   # Thay bằng key của bạn
QUERY = "study shorts"
TOTAL_RESULTS = 200    # Bạn muốn bao nhiêu video
CSV_PATH = "youtube_results.csv"

yt = build("youtube", "v3", developerKey=API_KEY)

all_rows = []
next_page_token = None
collected = 0

while collected < TOTAL_RESULTS:
    # số video mỗi lần gọi (tối đa 50)
    results_to_get = min(50, TOTAL_RESULTS - collected)

    search_resp = yt.search().list(
        part="snippet",
        q=QUERY,
        type="video",
        videoDuration="short",
        maxResults=results_to_get,
        order="viewCount",
        pageToken=next_page_token
    ).execute()

    items = search_resp.get("items", [])
    video_ids = [it["id"]["videoId"] for it in items]
    
    videos_resp = yt.videos().list(
        part="statistics,snippet",
        id=",".join(video_ids)
    ).execute()

    for it in videos_resp.get("items", []):
        snip = it.get("snippet", {})
        stats = it.get("statistics", {})
        all_rows.append({
            "video_id": it["id"],
            "title": snip.get("title"),
            "channel": snip.get("channelTitle"),
            "published_at": snip.get("publishedAt"),
            "views": stats.get("viewCount"),
            "likes": stats.get("likeCount"),
            "comments": stats.get("commentCount")
        })

    collected += len(items)
    next_page_token = search_resp.get("nextPageToken")
    if not next_page_token:
        break   # hết kết quả

# Lưu CSV
df = pd.DataFrame(all_rows)
df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
print(f"Đã lưu {len(df)} video vào {CSV_PATH}")
