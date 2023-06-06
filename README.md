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

PCすぺっこ
- windows 11 home
- AMD Ryzen 5 5600X
- DRAM 3600Hz 32GB

# 使用方法？
pythonファイルは一つなのでそれを実行してください。  
webカメラとして使う場合はOBSでキャプチャして、OBS仮想カメラで出力してください。
![obs](https://github.com/omikujiv/korigori/assets/128278435/3f9e2f78-073e-46ed-8dbb-460ce0b48541)


# 機能？


https://github.com/omikujiv/korigori/assets/128278435/abe5a726-b96d-41de-ac5a-d941e4cafa5d

