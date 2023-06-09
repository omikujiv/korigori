# korigori
web会議中などにアイリスアウトの演出で退場できるようにしたかった。

アイリスアウトっていうのはこういうやつ。
![こりごりでやんす](https://github.com/omikujiv/korigori/assets/128278435/f3987307-5f4c-4b94-9842-a223822050b9)

# 動作デモ
表示されるウィンドウをアクティブにした状態で、'k'キーを押すことで状態が遷移。  
「通常webカムモード」→「顔の中心まで黒背景が来る」→「完全に黒背景に飲まれる」→ 以下ループ

https://github.com/omikujiv/korigori/assets/128278435/33302ca9-be9f-4c20-885d-0df967f1bac1

※ プライバシー保護のために、顔面をイラストでマスクしています。  
※ 顔面素材は付属しません、自分で描いてください。  

# 環境など
ライブラリとか
- Python 3.10.11
- numpy  1.23.1  
- opencv-python 4.7.0.72 (多分)  
- insightface 0.7.3  

顔認識モジュールであるinsightfaceのインストールがなんか順番とか依存関係とかあって、めんどくさかった。  
インストール後になんかエラー出たら、OpenCVを入れなおしたらイケた。

PCすぺっこ
- windows 11 home
- AMD Ryzen 5 5600X
- DRAM 3600Hz 32GB

# 使用方法？
pythonファイルは一つなのでそれを実行してください。  
webカメラとして使う場合はOBSでキャプチャして、OBS仮想カメラで出力してください。
![obs](https://github.com/omikujiv/korigori/assets/128278435/3f9e2f78-073e-46ed-8dbb-460ce0b48541)


https://github.com/omikujiv/korigori/assets/128278435/2ef7589b-3430-4e90-bb4a-8dde4bbc8f92



# 機能？
3つのウィンドウで、各処理を紹介する。
まず、左右のウィンドウで顔部分に変なイラストがくっついてるのはプライバシー保護兼イケメンが流出するのを防いでいるだけで、本筋の機能ではない。

## 顔検出
- 左のウィンドウのように、顔検出で顔の大きさと座標を取得している
- ここでは、顔の大きさくらいに緑色の円を描画している
## マスクの作成
- アイリスアウトで迫って来る黒背景をマスクで表現
- 表示では白(255)と黒(0)だが、内情は1と0
- マスクは顔の座標と大きさをベースに大きさを変化させる
## 2画像の乗算
- カメラ画像とマスクを乗算することで、1の部分のみが残る
    - 円形部分のみ元映像で、周囲は0(黒)になる

https://github.com/omikujiv/korigori/assets/128278435/abe5a726-b96d-41de-ac5a-d941e4cafa5d

# License
MIT
https://github.com/omikujiv/korigori/blob/main/LICENSE
