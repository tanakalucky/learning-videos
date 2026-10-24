# learning-videos

日本語の短い仕組み解説動画を作る、最小限のローカル制作リポジトリ。
第1作は「IAPは、アプリの入口を守る」。78秒、1280×720、30fps、H.264 MP4、日本語焼き込み字幕、音声なし。

## 制作とプレビュー

既存環境: macOS、Python 3.9以降 + Pillow 11.3.0、ffmpeg（libx264対応）、ヒラギノ角ゴシック W4。
今回の制作ではimageio-ffmpeg 0.6.0を .build/deps に限定して追加した。macOS標準H.264エンコーダーは利用不可だった。未導入の依存関係は実行者の承認手順に従い準備する。Python依存は requirements.txt に固定。

```sh
cd learning-videos
python3 -m pip install --target .build/deps --no-deps --only-binary=:all: imageio-ffmpeg==0.6.0
python3 tools/check.py
python3 render.py --time 37
python3 render.py
python3 tools/inspect.py
python3 -m http.server 8000 --bind 127.0.0.1
```

ブラウザで http://127.0.0.1:8000/preview.html を開く。終了はCtrl+C。
画面録画やクラウドサービス、認証情報、ネットワーク接続はレンダリングに不要。
`VIDEO_FONT=/absolute/path/to/font.ttf` で代替日本語フォントを指定可能。フォントを変更したらレイアウトを再確認する。フォント自体は再配布しない。

## 構成

- `engine/draw.py`: カード、人物、矢印、強調、字幕、進行バー
- `topics/iap/scenes.py`: このテーマの字幕・時間割・シーン
- `render.py`: 指定秒のPNG、固定fpsの全フレーム生成
- `render.py` はRGBフレームをffmpegのlibx264へ渡してMP4化
- `tools/check.py`: 時間割・字幕幅・同一時刻の描画再現性
- `tools/inspect.py`: MP4全フレームのデコード、映像仕様・音声なし検証、代表フレーム抽出
- `docs/`: 日本語台本、出典、次回制作手順、QA記録
- `output/`: 生成物（Git管理外）

時刻は編集上の時間。実測レイテンシーを示さない。絵は同じ入力時刻から再現可能だが、OS・フォント・エンコーダー差でMP4バイト列まで同一とは限らない。

次の依頼例: 「このリポジトリを使って、Cloud Runの認証を初心者向けに75秒、日本語字幕・音声なしで作って。公式資料を確認して、MP4とソースを納品して」。詳細は `docs/new-topic-ja.md`。

このリポジトリはローカルのみ。公開・remote登録・pushは保存先確認後に行う。
