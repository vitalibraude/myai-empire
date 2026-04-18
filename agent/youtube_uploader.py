"""
YouTube Uploader — uploads videos to YouTube using the YouTube Data API v3.
Requires OAuth2 credentials from Google Cloud Console.

Setup:
1. Go to console.cloud.google.com
2. Create project → Enable YouTube Data API v3
3. Create OAuth2 credentials (Desktop App)
4. Download client_secrets.json to project root
5. Run this script — it will open browser for auth
"""
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS_PATH = os.path.join(BASE_DIR, 'client_secrets.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'data', 'youtube_token.json')
UPLOAD_LOG = os.path.join(BASE_DIR, 'data', 'youtube_uploads.json')

SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
           'https://www.googleapis.com/auth/youtube']


def _get_authenticated_service():
    """Get authenticated YouTube service."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(SECRETS_PATH):
                print("[YOUTUBE] ERROR: client_secrets.json not found!")
                print("[YOUTUBE] Setup instructions:")
                print("  1. Go to console.cloud.google.com")
                print("  2. Create project → Enable YouTube Data API v3")
                print("  3. Create OAuth2 Desktop credentials")
                print("  4. Download client_secrets.json to project root")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(SECRETS_PATH, SCOPES)
            creds = flow.run_local_server(port=8090)
        
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'w') as f:
            f.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)


def upload_video(video_path, title, description, tags=None, category="28",
                 privacy="public", thumbnail_path=None):
    """
    Upload a video to YouTube.
    category 28 = Science & Technology, 22 = People & Blogs
    """
    from googleapiclient.http import MediaFileUpload

    youtube = _get_authenticated_service()
    if not youtube:
        return None

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags or ['AI', 'automation', 'business', 'myAI'],
            'categoryId': category,
            'defaultLanguage': 'en',
        },
        'status': {
            'privacyStatus': privacy,
            'selfDeclaredMadeForKids': False,
        }
    }

    media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)
    
    print(f"[YOUTUBE] Uploading: {title}")
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Upload progress: {int(status.progress() * 100)}%")
    
    video_id = response['id']
    video_url = f"https://youtube.com/watch?v={video_id}"
    print(f"[YOUTUBE] Uploaded! URL: {video_url}")

    # Set thumbnail if provided
    if thumbnail_path and os.path.exists(thumbnail_path):
        try:
            thumbnail_media = MediaFileUpload(thumbnail_path, mimetype='image/png')
            youtube.thumbnails().set(videoId=video_id, media_body=thumbnail_media).execute()
            print(f"[YOUTUBE] Thumbnail set for {video_id}")
        except Exception as e:
            print(f"[YOUTUBE] Thumbnail failed (may need verified account): {e}")

    # Log upload
    _log_upload(video_id, title, video_url, video_path)
    
    return {"id": video_id, "url": video_url, "title": title}


def upload_all_videos():
    """Upload all generated videos to YouTube."""
    from agent.video_generator import OUTPUT_DIR
    
    youtube_dir = os.path.join(OUTPUT_DIR, 'youtube')
    shorts_dir = os.path.join(OUTPUT_DIR, 'shorts')
    thumbs_dir = os.path.join(OUTPUT_DIR, 'thumbnails')
    
    uploads = []
    
    # YouTube videos
    if os.path.exists(youtube_dir):
        for f in os.listdir(youtube_dir):
            if f.endswith('.mp4'):
                title = _video_title_from_filename(f)
                desc = _generate_description(title)
                thumb = os.path.join(thumbs_dir, 'thumb_main.png')
                
                result = upload_video(
                    os.path.join(youtube_dir, f),
                    title=title,
                    description=desc,
                    tags=['AI', 'automation', 'business', 'myAI', 'artificial intelligence',
                          'marketing automation', 'business automation'],
                    thumbnail_path=thumb if os.path.exists(thumb) else None
                )
                if result:
                    uploads.append(result)
    
    # Shorts
    if os.path.exists(shorts_dir):
        for f in os.listdir(shorts_dir):
            if f.endswith('.mp4'):
                title = _video_title_from_filename(f) + " #Shorts"
                desc = _generate_description(title, is_short=True)
                
                result = upload_video(
                    os.path.join(shorts_dir, f),
                    title=title,
                    description=desc,
                    tags=['AI', 'Shorts', 'automation', 'business', 'myAI'],
                    privacy="public"
                )
                if result:
                    uploads.append(result)
    
    print(f"\n[YOUTUBE] Uploaded {len(uploads)} videos total")
    return uploads


def _video_title_from_filename(filename):
    """Generate a title from filename."""
    name = filename.replace('.mp4', '').replace('myai_', '').replace('_', ' ')
    return f"myAI — {name.title()}"


def _generate_description(title, is_short=False):
    """Generate YouTube video description."""
    base = f"""{title}

🤖 myAI — Your Business on Autopilot

AI-powered business automation that handles:
✅ Website building & management
✅ Content creation & publishing
✅ Email marketing campaigns
✅ Social media management
✅ Customer service chatbot
✅ Analytics & reporting

🔗 Try it FREE for 14 days (no credit card):
https://aoeua.com/

📧 Contact: info@aoeua.com
🌐 All 50 AI Business Solutions: https://businesses.aoeua.com/

#AI #Automation #Business #Marketing #myAI #ArtificialIntelligence
"""
    if is_short:
        base += "\n#Shorts"
    return base


def _log_upload(video_id, title, url, file_path):
    """Log upload to file."""
    os.makedirs(os.path.dirname(UPLOAD_LOG), exist_ok=True)
    logs = []
    if os.path.exists(UPLOAD_LOG):
        with open(UPLOAD_LOG, 'r') as f:
            logs = json.load(f)
    
    logs.append({
        "video_id": video_id,
        "title": title,
        "url": url,
        "file": file_path,
        "uploaded_at": datetime.now().isoformat()
    })
    
    with open(UPLOAD_LOG, 'w') as f:
        json.dump(logs, f, indent=2)


def get_upload_stats():
    """Get upload statistics."""
    if not os.path.exists(UPLOAD_LOG):
        return {"total_uploads": 0, "videos": []}
    with open(UPLOAD_LOG, 'r') as f:
        logs = json.load(f)
    return {"total_uploads": len(logs), "videos": logs}


def check_setup():
    """Check if YouTube API is set up correctly."""
    has_secrets = os.path.exists(SECRETS_PATH)
    has_token = os.path.exists(TOKEN_PATH)
    
    print(f"[YOUTUBE] client_secrets.json: {'FOUND' if has_secrets else 'MISSING'}")
    print(f"[YOUTUBE] Auth token: {'FOUND' if has_token else 'MISSING'}")
    
    if not has_secrets:
        print("\n[YOUTUBE] To set up YouTube uploads:")
        print("  1. Go to https://console.cloud.google.com")
        print("  2. Create a new project (or select existing)")
        print("  3. Enable 'YouTube Data API v3'")
        print("  4. Go to Credentials > Create Credentials > OAuth 2.0 Client ID")
        print("  5. Application type: Desktop App")
        print("  6. Download JSON → rename to 'client_secrets.json'")
        print(f"  7. Place it in: {BASE_DIR}")
    
    return has_secrets


if __name__ == "__main__":
    check_setup()
