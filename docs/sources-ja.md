# 出典と表現上の判断

確認日: 2026-10-24。Google Cloud公式資料を参照。Googleとの提携や監修を示す作品ではない。

1. https://docs.cloud.google.com/iap/docs/concepts-overview
   - IAPが認証と認可を行い、IAMポリシーに基づいてアプリへのアクセスを制御する根拠。
   - 動画の「認証→認可」は理解のための論理順序。ネットワークの個別通信を忠実に再現した図ではない。
2. https://docs.cloud.google.com/iap/docs/managing-access
   - ユーザー・グループへのアクセス権付与、および IAP-secured Web App User の役割。
   - Aさん/Bさんは架空。同じ認証済みでも対象リソースの有効なアクセス権によって結果が異なる例。
3. https://docs.cloud.google.com/run/docs/securing/identity-aware-proxy-cloud-run
   - Cloud Runサービスへ直接IAPを設定可能。ロードバランサーは常に必要ではない。
   - IAP service agentへのCloud Run Invoker付与はユーザーのIAPアクセス権と別。短編では設定手順を扱わない。
   - ロードバランサーとサービスの両方にIAPを設定しない。直接設定とLB経由の方式には保護範囲の違いがある。
4. https://docs.cloud.google.com/iap/docs/signed-headers-howto
   - 実装時は署名付きIAP JWTを適切に検証。単なるメールアドレスヘッダーを信用しない。
   - 本編は入門の模式説明。バイパス経路の制御、JWT検証、OAuth設定などの実装ガイドは別途必要。

IAPを通過した後の「閲覧・編集・承認」は架空のアプリ側業務ルール。IAPのロールがこれらを自動的に実装する意味ではない。
端末・場所などのコンテキスト条件、外部ID連携、サービス間アクセス、TCP転送は対象外。

## 制作方式の着想
https://zenn.dev/explaza/articles/c749042ecbe232

時刻を指定して絵を再現し、フレームを連結する考え方を参考にした。第三者のスキル・コードは導入していない。本作品は独自のPillow描画とffmpegで実装。HTML/Playwrightを必要としない。macOS標準エンコーダーが利用不可のため、承認手続きを通してimageio-ffmpeg 0.6.0をプロジェクト内に追加した。プレビューはローカルHTMLで動画と章移動を提供する。
