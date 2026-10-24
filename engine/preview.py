import html
import json

def write_preview(path, meta, scenes, duration):
    chapters = json.dumps([[s[0], s[2]] for s in scenes], ensure_ascii=True).replace('<', '\\u003c')
    title = html.escape(meta['title'])
    path.write_text(f'''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{title}</title>
<style>body{{margin:40px auto;max-width:1100px;background:#0b1425;color:#f1f5fc;font:18px system-ui;padding:0 24px}}video{{width:100%;border-radius:18px}}button{{margin:5px;padding:10px 14px;background:#1d2e49;color:#f1f5fc;border:1px solid #72b6ff;border-radius:8px;cursor:pointer}}</style>
<h1>{title}</h1><p>{duration:g}秒 / 日本語字幕 / 音声なし</p><video controls preload="metadata" src="video.mp4"></video><div id="chapters"></div>
<script>const v=document.querySelector('video');{chapters}.forEach(([t,s])=>{{let b=document.createElement('button');b.textContent=s;b.onclick=()=>{{v.currentTime=t;v.pause()}};document.querySelector('#chapters').append(b)}})</script></html>''')
