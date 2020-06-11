# README
これはTシャツの画像をAIが見て、値段を鑑定してくれるアプリです。
jpeg, pngなどの画像ファイルをアップロードするか、ウェブカメラ、スマホカメラ（スマホ上での動作は未確認今後実装予定）で撮影したTシャツの写真をアプリが読み込み、価格帯、鑑定結果の信頼度を出してくれます。

AIには畳み込みニューラルネットワークを採用しました。ニューラルネットワークの学習・検証には日本の某有名サイトの約定済みTシャツの画像１万枚を使用しました。

This app estimates the price of your T-shirt from image.
You can upload an image of a T-shirt in various formats such as jpeg, png and etc. You can also submit photos of your T shirt immediately from webcam or smartphone camera.

The AI used in this app is convolutional neural network trained with over 10 thousand samples of T-shirt image and actual transaction price. The samples are collected from one of the major e-commerce sites in Japan.

# T-shirts DB

## user table

|Column|Type|Options|
|------|----|-------|
|email|string|null: false|
|password|string|null: false|
|username|string|null: false|
### Association
- has_many tshirts

## tshirt table
|Column|Type|Options|
|------|----|-------|
|image|text||
|comment|text||
|price_range||
|confidence||
|user_id|integer|null: false, foreign_key: true|

### Association
- belongs_to user