#!/usr/bin/env python3
"""Create a local topic without overwriting any existing directory."""
import argparse
import json
from engine.topic import topic_path, WORKSPACE

STARTER = '''from engine.draw import Canvas, progress, BLUE, GREEN

SCENES = [
    (0, 4, "全体像", "何が起きる？", "説明したいことを、短い字幕にします。"),
    (4, 8, "仕組み", "順番を追う", "矢印の動きは論理的な順序を示します。"),
]
DURATION = SCENES[-1][1]

def render(t):
    t = max(0, min(DURATION - 1e-9, t))
    index, scene = next((i, s) for i, s in enumerate(SCENES) if s[0] <= t < s[1])
    start, end, title, tag, subtitle = scene
    c = Canvas(scene_count=len(SCENES))
    c.frame(index + 1, title, tag, subtitle, t, DURATION)
    c.card(120, 250, 360, 230, "入力", "ここを書き換える", BLUE)
    c.card(800, 250, 360, 230, "結果", "ここを書き換える", GREEN)
    c.arrow(510, 365, 770, 365, progress(t - start, 0.5, 2), GREEN)
    return c.im
'''

def create_topic(name, title, fps):
    path = topic_path(name)
    if type(fps) is not int or not 1 <= fps <= 60:
        raise ValueError('fpsは1〜60の整数です')
    if not title.strip():
        raise ValueError('titleが必要です')
    WORKSPACE.mkdir(exist_ok=True)
    path.mkdir()  # Atomic refusal if any file, directory or symlink exists.
    (path / 'topic.json').write_text(json.dumps({'title': title, 'fps': fps}, ensure_ascii=False, indent=2) + '\n')
    (path / 'scenes.py').write_text(STARTER)
    (path / 'storyboard.md').write_text('# 台本・絵コンテ\n\n対象読者：\n伝えたいこと：\n\n秒数・画面・字幕を整理する。\n')
    (path / 'sources.md').write_text('# 出典\n\n確認日・URL・主張との対応を残す。\n')
    return path

def main():
    p = argparse.ArgumentParser()
    p.add_argument('topic')
    p.add_argument('--title')
    p.add_argument('--fps', type=int, default=30)
    a = p.parse_args()
    try:
        print(create_topic(a.topic, a.title or a.topic, a.fps))
    except (ValueError, FileExistsError) as e:
        p.error(str(e))

if __name__ == '__main__':
    main()
