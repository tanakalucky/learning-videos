# learning-videos

テーマごとの台本とシーンから、字幕・アニメーション付きの短い動画を作る自分用ツール。

```sh
python3 new_topic.py my-topic --title "説明したいテーマ"
```

`workspace/my-topic/` に雛形を作る。同名の作業があれば上書きしない。

- `topic.json`：題名・fps
- `scenes.py`：時間割・字幕・描画。`DURATION`は最終シーンの終了秒
- `storyboard.md`：台本・絵コンテ
- `sources.md`：出典
- `output/`：動画・プレビュー・確認用画像（生成時に作成）

台本・シーンを編集してから実行する。

```sh
python3 tools/check.py --topic my-topic
python3 render.py --topic my-topic --time 2
python3 render.py --topic my-topic
python3 tools/verify_video.py --topic my-topic
python3 -m http.server 8000 --bind 127.0.0.1
```

`http://127.0.0.1:8000/workspace/my-topic/output/` で動画と章移動を確認する。停止はCtrl+C。
`--fps`で書き出しを変更する場合は、検証コマンドにも同じ値を渡す。

共通の描画部品は`engine/`、テーマ固有の作業は`workspace/`に置く。`workspace/`全体をGit管理から除外する。動画や確認用画像は使い終わったら処分してよい一時生成物で、恒久保存・アップロードは必要なときだけ行う。

共通ツールのテスト：`python3 -m unittest discover -s tests`
