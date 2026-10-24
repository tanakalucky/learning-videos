"""Validate any local topic's timeline, subtitle layout and repeatable rendering."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.topic import load_topic, frame_count
from engine.draw import font, W, H
from PIL import Image, ImageDraw

def check_topic(name):
    path, meta, topic = load_topic(name)
    count = frame_count(topic.DURATION, meta['fps'])
    draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    checked = 0
    for start, end, title, tag, subtitle in topic.SCENES:
        lines = subtitle.split('\n')
        if len(lines) > 2 or any(draw.textlength(line, font=font(27)) > W - 160 for line in lines):
            raise ValueError('字幕は表示幅内の2行以下にしてください')
        for t in [start, (start + end) / 2, end - min(1 / meta['fps'], (end - start) / 2)]:
            a, b = topic.render(t), topic.render(t)
            if a.size != (W, H) or a.tobytes() != b.tobytes():
                raise ValueError('描画サイズまたは同一時刻の再現性を確認してください')
            checked += 1
    return {'duration': topic.DURATION, 'fps': meta['fps'], 'frames': count, 'scenes': len(topic.SCENES), 'checked_frames': checked}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--topic', required=True)
    a = p.parse_args()
    print('PASS:', check_topic(a.topic))

if __name__ == '__main__':
    main()
