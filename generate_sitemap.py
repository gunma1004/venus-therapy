import os
import datetime
import urllib.parse

# 실제 사용할 도메인 주소 (Netlify 주소 또는 연결할 개인 도메인)
BASE_URL = "https://venus-therapy.netlify.app"

today = datetime.date.today().isoformat()
url_list = []

# 프로젝트 내 모든 index.html 파일 경로 수집
for root, dirs, files in os.walk("."):
    # 가상환경, 깃 폴더, 리소스 폴더 등 제외
    if any(p in root.split(os.sep) for p in [".git", ".vscode", "assets", "css", "js", "__pycache__"]):
        continue
        
    if "index.html" in files:
        rel_path = os.path.relpath(root, ".").replace("\\", "/")
        
        if rel_path == ".":
            loc = f"{BASE_URL}/"
            priority = "1.0"
            changefreq = "daily"
        else:
            # 한글 경로(동/읍/면 등)를 안전하게 URL 인코딩 처리
            encoded_path = "/".join(urllib.parse.quote(part) for part in rel_path.split("/"))
            loc = f"{BASE_URL}/{encoded_path}/"
            
            # 깊이(시도: 0.8, 구시: 0.8, 동/읍/면: 0.6)
            priority = "0.8" if rel_path.count("/") <= 1 else "0.6"
            changefreq = "weekly"
        
        url_list.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

# sitemap.xml 생성
sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(url_list)}
</urlset>"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

# robots.txt 생성
robots_content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""

with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)

print(f">> 완료! 총 {len(url_list)}개 URL이 담긴 sitemap.xml 및 robots.txt가 성공적으로 생성되었습니다.")