# youtube_short_vietnam
# YouTube Shorts Vietnam — Phân Tích Dữ Liệu

![Dashboard Preview](dashboard/dashboard_overview.png)

> **Phân tích dữ liệu end-to-end** — từ thu thập dữ liệu qua YouTube Data API, tiền xử lý & NLP bằng Python, đến trực quan hóa trên Power BI — khám phá hành vi xem, tương tác và xu hướng nội dung YouTube Shorts tại thị trường Việt Nam giai đoạn 2018–2025.

---

## 🗂️ Mục Lục

- [Tổng Quan Dự Án](#-tổng-quan-dự-án)
- [Quy Trình Dự Án](#-quy-trình-dự-án)
- [Dataset](#-dataset)
- [Công Cụ & Kỹ Thuật](#️-công-cụ--kỹ-thuật)
- [Cấu Trúc Dự Án](#-cấu-trúc-dự-án)
- [Key Insights](#-key-insights)
- [Dashboard](#-dashboard)
- [Hướng Dẫn Sử Dụng](#-hướng-dẫn-sử-dụng)
- [Kết Luận & Đề Xuất](#-kết-luận--đề-xuất)

---

## 🎯 Tổng Quan Dự Án

### Mục tiêu
Dự án này nhằm trả lời các câu hỏi kinh doanh quan trọng cho nhà sáng tạo nội dung và marketer tại Việt Nam:

- Thể loại nội dung nào có **lượt xem và tương tác cao nhất**?
- **Thời điểm nào trong tuần / tháng** phù hợp để đăng video?
- Xu hướng tăng trưởng của YouTube Shorts tại Việt Nam theo thời gian ra sao?
- Yếu tố nào (hashtag, thời lượng, chủ đề) ảnh hưởng đến **tỷ lệ tương tác** (engagement rate)?
- **Kênh nào** đang hoạt động hiệu quả nhất và chiến lược nội dung của họ là gì?

### Phạm vi
| Chỉ số | Giá trị |
|---|---|
| Số video phân tích | **2.358K** |
| Tổng lượt xem | **~10 tỷ** |
| Tổng lượt thích | **~125 triệu** |
| Tổng bình luận | **~903K** |
| Số kênh | **1.171** |
| Thời gian | **2018 – 2025** |
| Tổng số hashtag | **2.358K** |

---

## 🔄 Quy Trình Dự Án

```
[1. Thu Thập]         [2. Tiền Xử Lý]        [3. Phân Tích]        [4. Trực Quan Hóa]
YouTube Data API  →   Python / NLP       →    EDA + Insights   →    Power BI Dashboard
ThuThapData.py        YouTube_Shorts          Jupyter Notebook       2-page report
                      _Vietnam.ipynb
```

### Bước 1 — Thu Thập Dữ Liệu (`ThuThapData.py`)
Sử dụng **YouTube Data API v3** để tự động thu thập dữ liệu video:
- Tìm kiếm video Shorts theo từ khóa, lọc theo `videoDuration="short"`
- Lấy thống kê: `views`, `likes`, `comments`, `subscribers`
- Hỗ trợ phân trang (`nextPageToken`) để thu thập số lượng lớn (tối đa 200+ video/lần)
- Xuất ra file `CSV` sẵn sàng cho bước tiền xử lý

```python
# Minh họa logic thu thập
yt = build("youtube", "v3", developerKey=API_KEY)
search_resp = yt.search().list(
    part="snippet", q=QUERY, type="video",
    videoDuration="short", maxResults=50, order="viewCount"
).execute()
```

### Bước 2 — Tiền Xử Lý & NLP (`YouTube_Shorts_Vietnam.ipynb`)
Pipeline xử lý dữ liệu gồm **7 nhóm kỹ thuật chính**:

| Bước | Kỹ thuật | Mô tả |
|---|---|---|
| 2.1 | **Chuẩn hóa kiểu dữ liệu** | Parse `datetime`, convert ISO 8601 duration → seconds |
| 2.2 | **Xử lý trùng lặp** | Deduplicate theo `video_id` |
| 2.3 | **Lọc dữ liệu bất hợp lệ** | Loại giá trị âm ở `views`, `likes`, `comments`, `subscribers` |
| 2.4 | **Làm sạch văn bản** | Lowercase, strip, loại URL, emoji, ký tự đặc biệt |
| 2.5 | **NLP Pipeline** | Tokenization, Stopwords removal (NLTK), Stemming (PorterStemmer), Lemmatization |
| 2.6 | **Phát hiện ngôn ngữ** | `langdetect` → lọc lấy video tiếng Việt (`lang == 'vi'`) |
| 2.7 | **Chuẩn hóa danh mục** | Map category ID → tên tiếng Việt (15 danh mục) |

---

## 📁 Dataset

**File cuối:** `youtube_data_vietnamese2.csv`  
**Số dòng:** 2.360 records | **Số cột:** 21 features

### Mô tả các trường dữ liệu

| Cột | Mô tả | Kiểu dữ liệu |
|---|---|---|
| `video_id` | ID định danh video | string |
| `title` | Tiêu đề video gốc | string |
| `title_clean` | Tiêu đề đã làm sạch (NLP) | string |
| `title_tokens` | Danh sách token từ tiêu đề | list |
| `title_clean_text` | Tiêu đề sau stemming/lemmatization | string |
| `category` | Danh mục (tiếng Anh, YouTube ID) | string |
| `category_vi` | Danh mục (tiếng Việt, chuẩn hóa) | string |
| `views` | Tổng lượt xem | int |
| `likes` | Tổng lượt thích | int |
| `comments` | Tổng bình luận | int |
| `duration` | Thời lượng gốc (ISO 8601) | string |
| `duration_seconds` | Thời lượng (giây) | float |
| `subscribers` | Số người đăng ký kênh | int |
| `publish_date` | Ngày đăng video | datetime |
| `hashtags_clean` | Hashtag đã làm sạch | string |
| `hashtag_list` | Danh sách hashtag tách ra | list |
| `n_hashtags` | Số lượng hashtag | int |
| `lang` | Ngôn ngữ phát hiện tự động | string |
| `channel_title` | Tên kênh | string |
| `topic` | Chủ đề cụ thể | string |


---

## 🛠️ Công Cụ & Kỹ Thuật

### Tech Stack

```
Thu thập dữ liệu   →  YouTube Data API v3 + google-api-python-client
Data Wrangling     →  Python · pandas · numpy · isodate
NLP                →  NLTK · langdetect · underthesea · vaderSentiment · WordCloud
Visualization      →  matplotlib · seaborn · Power BI (DAX, custom visuals)
Môi trường         →  Google Colab · Jupyter Notebook
```

### Kỹ năng phân tích áp dụng

- **API Data Collection:** Gọi REST API có phân trang, xử lý quota, lưu CSV tự động
- **Data Cleaning & Wrangling:** Xử lý missing values, type casting, deduplication, outlier filtering
- **Text Preprocessing (NLP):** Tokenization, stopwords removal, stemming, lemmatization, language detection
- **Exploratory Data Analysis (EDA):** Thống kê mô tả, phân phối, tương quan, phát hiện outlier
- **Time Series Analysis:** Xu hướng lượt xem theo tháng từ 2018–2025
- **Engagement Rate Analysis:** Tính toán và so sánh tỷ lệ tương tác theo danh mục
- **Channel Performance Analysis:** Top kênh theo tổng views, views/video, thời lượng TB
- **Heatmap / Matrix Analysis:** Ma trận lượt xem theo ngày trong tuần × tháng
- **Word Cloud:** Từ khóa phổ biến trong tiêu đề và hashtag
- **Dashboard Design:** Power BI với DAX measures, slicers động, 2-page report

---

## 📂 Cấu Trúc Dự Án

```
youtube-shorts-vietnam-analysis/
│
├── data/
│   ├── youtube_data_vietnamese2.csv    # Dataset cuối (đã xử lý)
│   └── youtube_results.csv            # Raw data từ API (mẫu)
│
├── notebooks/
│   └── YouTube_Shorts_Vietnam.ipynb   # Tiền xử lý, NLP & EDA
│
├── scripts/
│   └── ThuThapData.py                 # Thu thập dữ liệu qua YouTube API
│
├── dashboard/
│   ├── YouTube_Shorts_Analysis.pbix   # File Power BI
│   ├── dashboard_overview.png         #  Overview
│   └── dashboard_analysis.png        #  Analysis
│
└── README.md
```

---

## 💡 Key Insights

### 1. 📈 Xu Hướng Tăng Trưởng
- Lượt xem **tăng đột biến vào Q2/2022** (đạt ~500M/tháng), trùng với giai đoạn YouTube Shorts bùng nổ toàn cầu.
- Sau 2022, lượt xem **ổn định ở mức ~100–200M/tháng**, cho thấy thị trường đã trưởng thành và cạnh tranh hơn.

### 2. 🎯 Nội Dung Chiến Lược
- **"Đời sống"** chiếm 58% tổng video — phân khúc cạnh tranh cao nhưng có audience rộng nhất.
- **"Khoa học & Công nghệ"** có **tỷ lệ tương tác cao nhất (0.03)** — cơ hội lớn cho creator dù số lượng video còn ít.
- **"Mẹo vặt & Phong cách"** và **"Giáo dục"** đạt engagement rate 0.02 — nội dung thực dụng được phản hồi tốt và bền vững.

### 3. 📅 Thời Điểm Đăng Video Tối Ưu
- **Thứ 3 tháng 4** và **Thứ 5 tháng 5** ghi nhận lượt xem cao đột biến (highlight màu đậm trên heatmap).
- **Tháng 4–5** là giai đoạn có lượt xem cao nhất trong năm.
- **Chủ nhật tháng 1–2** có lượt xem thấp nhất — nên hạn chế đăng vào giai đoạn này.

### 4. 📊 Channel Performance
- Số người đăng ký **không phải yếu tố duy nhất** quyết định lượt xem — nội dung chất lượng trong niche nhỏ vẫn đạt triệu views.
- Top 10 kênh hiệu suất cao chủ yếu thuộc mảng **thiếu nhi, giải trí gia đình** và **đời sống hài hước**.
- Có sự chênh lệch lớn giữa **tổng views** và **views trung bình/video** — thể hiện một số kênh tập trung vào số lượng, một số vào chất lượng.

### 5. ⏱️ Thời Lượng Video
- Phân tích tương quan giữa `duration_seconds` và `views/likes/comments` cho thấy **video ngắn (dưới 45 giây)** có xu hướng tương tác tốt hơn.
- Đây phù hợp với đặc tính của nền tảng Shorts — nội dung ngắn gọn, dễ xem lại.

### 6. 🏷️ Hashtag & Discoverability
- Top hashtag của các kênh lớn tập trung vào **tên kênh, tên nhân vật, và thể loại nội dung** — chiến lược xây dựng brand identity qua hashtag.
- Dataset có 2.358K hashtag duy nhất, phản ánh sự đa dạng trong chiến lược SEO của creator.

---

## 📊 Dashboard

Dashboard được xây dựng trên **Power BI** với 2 trang:

### Page 1 — Overview
| Visual | Mô tả |
|---|---|
| KPI Cards (7 thẻ) | Tổng video, subscribers, thời lượng TB, views, comments, hashtags, likes |
| Donut Chart | Phân bố video theo nhóm chủ đề (category_vi) |
| Line Chart | Xu hướng lượt xem theo tháng (2018–2025) |
| Heatmap Matrix | Tổng lượt xem theo ngày trong tuần × tháng |
| Horizontal Bar Chart | Tỷ lệ tương tác theo danh mục nội dung |

### Page 2 — Analysis
*(Trang phân tích chi tiết)*

### Bộ lọc động (Slicers)
- **Nội dung** — theo danh mục
- **Chủ đề** — theo topic
- **Năm** — theo năm đăng

---

## 🚀 Hướng Dẫn Sử Dụng

### Yêu cầu
```
Python      ≥ 3.8
Power BI Desktop (Windows, miễn phí)
Google API Key (YouTube Data API v3)
```

### Cài đặt thư viện Python
```bash
pip install pandas numpy matplotlib seaborn
pip install google-api-python-client
pip install langdetect vaderSentiment underthesea
pip install nltk isodate wordcloud
```

### Thu thập dữ liệu mới
```python
# Trong ThuThapData.py — chỉnh các thông số:
API_KEY = "your_youtube_api_key"
QUERY   = "từ khóa tìm kiếm"
TOTAL_RESULTS = 200        # Số video muốn thu thập

python scripts/ThuThapData.py
# → Xuất file youtube_results.csv
```

### Chạy notebook tiền xử lý
```bash
# Local
jupyter notebook notebooks/YouTube_Shorts_Vietnam.ipynb

# Hoặc mở trên Google Colab
# → Upload file .ipynb → Runtime > Run all
```

### Xem Dashboard Power BI
```
1. Tải Power BI Desktop tại https://powerbi.microsoft.com
2. Mở file: dashboard/YouTube_Shorts_Analysis.pbix
3. Refresh data source nếu cần
```

---

## 🔍 Kết Luận & Đề Xuất

### Dành cho Content Creator
1. **Tập trung vào niche Khoa học & Công nghệ** nếu muốn engagement cao trong thị trường ít cạnh tranh.
2. **Đăng video vào Thứ 3–Thứ 5, tháng 4–5** để tối ưu lượt xem tự nhiên.
3. **Giữ video dưới 45 giây** — tương thích tốt nhất với thuật toán Shorts.
4. **Xây dựng hashtag brand** — top kênh đều có chiến lược hashtag nhất quán theo tên kênh/nhân vật.
5. Nội dung **có giá trị** (mẹo vặt, giáo dục) tạo ra tương tác bền vững hơn nội dung thuần giải trí.

### Hướng Phát Triển Tiếp Theo
- [ ] Xây dựng model dự báo lượt xem (regression) dựa trên đặc trưng video
- [ ] Clustering nội dung theo TF-IDF + K-Means để tìm niche tiềm năng
- [ ] Mở rộng dataset để so sánh với thị trường các nước khcas(Thái Lan, Indonesia)

---

## 👤 Tác Giả

**[Nguyễn Thị Như]**  

> *Bài được thực hiện — từ thu thập dữ liệu thực qua API, xử lý NLP, đến xây dựng dashboard — nhằm thực hành end-to-end data analytics workflow.*
