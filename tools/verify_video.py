"""Decode a topic's MP4 and check it against its current duration and selected fps."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.topic import load_topic, frame_count, ffmpeg_exe
from engine.draw import W, H

def verify(name, fps_override=None):
    path, meta, topic = load_topic(name)
    fps = meta['fps'] if fps_override is None else fps_override
    if type(fps) is not int or not 1 <= fps <= 60:
        raise ValueError('fpsは1〜60です')
    count = frame_count(topic.DURATION, fps)
    out = path / 'output'
    manifest = json.loads((out / 'render.json').read_text())
    if manifest['duration'] != topic.DURATION or manifest['fps'] != fps or manifest['frames'] != count or manifest['size'] != [W, H]:
        raise ValueError('テーマ・fpsと書き出し記録が一致しません。再生成してください')
    ffmpeg = ffmpeg_exe()
    result = subprocess.run([ffmpeg, '-hide_banner', '-xerror', '-i', str(out / 'video.mp4'), '-progress', 'pipe:1', '-f', 'null', '-'], text=True, capture_output=True, check=True)
    log = result.stderr
    duration = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', log)
    rate = re.search(r'(\d+(?:\.\d+)?) fps', log)
    frames = re.findall(r'^frame=(\d+)$', result.stdout, re.M)
    if not duration or not rate or not frames:
        raise ValueError('動画のメタデータを取得できませんでした')
    actual_duration = int(duration[1]) * 3600 + int(duration[2]) * 60 + float(duration[3])
    if 'Audio:' in log or 'Video: h264' not in log or not re.search(rf'\b{W}x{H}\b', log) or abs(float(rate[1]) - fps) > .01 or abs(actual_duration - topic.DURATION) > .02 or int(frames[-1]) != count:
        raise ValueError('動画の時間・fps・フレーム数・形式が期待値と一致しません')
    qa = out / 'qa'
    qa.mkdir(exist_ok=True)
    times = [(s[0] + s[1]) / 2 for s in topic.SCENES]
    for i, t in enumerate(times):
        subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(t), '-i', str(out / 'video.mp4'), '-frames:v', '1', str(qa / f'scene-{i + 1:02d}.png')], check=True)
    report = {'result': 'PASS', 'duration': actual_duration, 'fps': fps, 'frames_decoded': int(frames[-1]), 'size': [W, H], 'audio_tracks': 0, 'review_times': times}
    (qa / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--topic', required=True)
    p.add_argument('--fps', type=int)
    a = p.parse_args()
    print(json.dumps(verify(a.topic, a.fps)))

if __name__ == '__main__':
    main()
