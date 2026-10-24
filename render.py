#!/usr/bin/env python3
"""Render a local topic at explicit timestamps; encode frames through ffmpeg."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from engine.draw import W, H
from engine.topic import load_topic, frame_count, ffmpeg_exe
from engine.preview import write_preview

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--topic', required=True)
    p.add_argument('--time', type=float)
    p.add_argument('--fps', type=int)
    a = p.parse_args()
    path, meta, topic = load_topic(a.topic)
    fps = meta['fps'] if a.fps is None else a.fps
    if not 1 <= fps <= 60:
        p.error('fpsは1〜60です')
    count = frame_count(topic.DURATION, fps)
    out = path / 'output'
    out.mkdir(exist_ok=True)
    if a.time is not None:
        if not 0 <= a.time < topic.DURATION:
            p.error('timeはテーマの再生区間内にしてください')
        destination = out / f'frame-{a.time:07.2f}.png'
        topic.render(a.time).save(destination)
        print(destination)
        return
    print(render_video(a.topic, path, meta, topic, fps, count))


def render_video(name, path, meta, topic, fps, count):
    """Publish staged artifacts only after ffmpeg and sidecar generation succeed."""
    out = path / 'output'
    out.mkdir(exist_ok=True)
    ffmpeg = ffmpeg_exe()
    # Staging below output keeps replacements on the same filesystem.
    with tempfile.TemporaryDirectory(prefix='.render-', dir=out) as temporary:
        stage = Path(temporary)
        destination = stage / 'video.mp4'
        (stage / 'render.json').write_text(json.dumps({'topic': name, 'title': meta['title'], 'duration': topic.DURATION, 'fps': fps, 'frames': count, 'size': [W, H], 'audio': False}, ensure_ascii=False, indent=2) + '\n')
        write_preview(stage / 'index.html', meta, topic.SCENES, topic.DURATION)
        cmd = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps), '-i', 'pipe:0', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(destination)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        try:
            for i in range(count):
                frame = topic.render(i / fps)
                if frame.size != (W, H):
                    raise ValueError('描画サイズが共通キャンバスと一致しません')
                proc.stdin.write(frame.convert('RGB').tobytes())
                if i % (fps * 10) == 0:
                    print(f'{i / fps:g}/{topic.DURATION:g}s', flush=True)
            proc.stdin.close()
            if proc.wait() != 0:
                raise RuntimeError('ffmpeg failed')
        except BaseException:
            if proc.poll() is None:
                proc.kill()
            try:
                proc.stdin.close()
            except OSError:
                pass
            proc.wait()
            raise
        for filename in ('video.mp4', 'render.json', 'index.html'):
            (stage / filename).replace(out / filename)
    return out / 'video.mp4'

if __name__ == '__main__':
    main()
