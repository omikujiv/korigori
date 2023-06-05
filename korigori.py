## カメラで取り込んだ画像をリアルタイムで表示
## 顔検出でアイリスアウト

import numpy as np # numpy  1.23.1
import cv2 # opencv-python 4.7.0.72 (多分)
from insightface.app import FaceAnalysis # insightface 0.7.3
import warnings

# 自分の顔にブルアカ先生の顔画像を載せる(機能紹介動画撮影用)
sensei_flag = False
# 置き換える透過画像(PNG)のパス：画像の縦横比は1:1にしないとゆがみます
sensei_path = './sensei3.png' 
# 処理過程を表示する(処理紹介動画撮影用)
showALL_flag = False


# カメラ画像に、顔置き換え画像を重ねる関数
def add_pict(img, sensei, pos, size):
    
    sensei_resized = cv2.resize(sensei, dsize=(size, size))
    
    sensei_a = sensei_resized[:,:,3]
    sensei_rgb = sensei_resized[:,:,:3]
    sensei_a3 = cv2.merge((sensei_a,sensei_a,sensei_a))
    sensei_inv = cv2.bitwise_not(sensei_a3)
    
    x,y = pos
    result = img
    sensei_rgb = sensei_rgb - sensei_inv
    
    img_y, img_x = img.shape[:2]
    # print(f' {y+size} < {img_y} = { (y+size < img_y)} ,  {x+size}< { img_x} = {(x+size < img_x)}')
    if (y+size < img_y) and (x+size < img_x):
        result[y:y+size, x:x+size] =  cv2.bitwise_and(img[y:y+size, x:x+size] , sensei_inv) 
        result[y:y+size, x:x+size] =  cv2.bitwise_or(result[y:y+size, x:x+size] , sensei_rgb)
    
    
    return result

# こりごりするための関数
def show_camera():
    # こりごりスピード
    spd = 40
    
    # このフラグで、「こりごりだよ～」になるかどうかを見る
    korigori_flag = False
    korigori_flag2 = False
    korigori_flag3 = False
    korigori_flagfin = False
    rad_sub = 0 # 円を小さくするハバ
    
    cap = cv2.VideoCapture(0)

    app = FaceAnalysis()
    app.prepare(ctx_id=0, det_size=(640, 640))

    while(cap.isOpened()):
        ret, frame = cap.read()
        frame_x = frame.shape[0] 
        frame_y = frame.shape[1] 
        faces = app.get(np.asarray(frame))
        # print(f'face {len(faces)}')
        # 全ての顔に対して
        for face in faces:
            x1, y1, x2, y2 = face.bbox.astype(np.int32)
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(frame.shape[1] - 1,x2)
            y2 = min(frame.shape[0] - 1,y2)
            #cv2.rectangle(frame, (x1,y1), (x2, y2), (255,0,0),7)
            #print(f'x1:{x1}  , y1:{y1}')
            #print(f'x2:{x2}  , y2:{y2}\n')
            #print(f'frame  {frame.shape}')

            # アイリスアウト用の顔周辺の円を計算

            cent_x = round((x1+x2)/2)
            cent_y = round((y1+y2)/2)
            rad_x = (x2 - x1) / 2
            rad_y = (y2 - y1) / 2
            if rad_x < rad_y:
                rad = rad_x
            else:
                rad = rad_y
            rad = round(rad*1.6)
            cent_y = round(cent_y *0.9)
            # 表示用
            frame2 = frame.copy()
            
            rad = rad * 1.2

        if len(faces)>0:
            
            if frame_x > frame_y:
                msk_rad = frame_x
            else:
                msk_rad = frame_y

            # こりごり円の縮小処理
            if korigori_flag:
                
                if (msk_rad - rad_sub > rad)and (not korigori_flag3): # 1st korigori
                    # print(f'1st korigori')
                    rad_sub = rad_sub + spd
                    
                    if msk_rad-rad_sub < rad : # 顔の周辺まできたら一回ストップ
                        korigori_flag = False
                        korigori_flag2 = True
                
                if korigori_flag2: # 2nd korigori
                    # print(f'2nd korigori')
                    rad_sub = rad_sub + round(spd/2)
                    # radが0になる処理
                    if msk_rad-rad_sub < 0:
                        # print(f'fin korigori')
                        korigori_flag = False
                        korigori_flag2 = False
                        korigori_flag3 = True
                        korigori_flagfin = True
                        rad_sub = msk_rad
                        
                elif korigori_flag3:
                    korigori_flagfin = False
                    # print(f'3rd korigori')
                    rad_sub = rad_sub - round(spd*1.5)
                    if rad_sub < 5:
                        rad_sub = 0 
                        korigori_flag = False
                        korigori_flag3 = False
                        # print(f'0 {korigori_flag}, 2 {korigori_flag2}, 3 {korigori_flag3}, fin {korigori_flagfin}')

            # 先生フェイス をつける
            if sensei_flag:
                sensei = cv2.imread(sensei_path, cv2.IMREAD_UNCHANGED)
                sensei_size = round(rad*2.2)
                pos = (cent_x-round(sensei_size/2),cent_y-round(sensei_size/2))
                result = add_pict(frame2, sensei, pos, sensei_size)
                frame = add_pict(frame, sensei, pos, sensei_size)
            else:
                result = frame2
            
            if korigori_flagfin:
                korigori = np.full((frame_x,frame_y,3),0,dtype=np.uint8)
            else:
                # こりごりサークルを小さくする
                msk_rad = msk_rad - rad_sub
                # アイリスアウト用のマスクを作成
                msk = np.full((frame_x,frame_y,3),0,dtype=np.uint8)
                ## 表示用
                msk2 = msk.copy()
                ## 顔周辺を白、他を黒
                cv2.circle(msk, center=(cent_x, cent_y), radius=msk_rad,color=(1,1,1),thickness=-1 )
                cv2.circle(msk2, center=(cent_x, cent_y), radius=msk_rad,color=(255,255,255),thickness=-1 )
                # msk * frame で アイリスアウト
                korigori = result * (msk / 255)
                
                
                
        else:
            msk2 = np.full((frame_x,frame_y,3),255,dtype=np.uint8)
            korigori = frame
            
        ## frame に 検出の円をつける
        cv2.circle(frame, center=(cent_x, cent_y), radius=round(rad/1.2), color=(0,255,0), thickness=4)
        
        # GUI show
        if showALL_flag:
            cv2.imshow("mask",msk2)
            cv2.imshow("Camera", frame)
        cv2.imshow("korigori", korigori)
        #print(f'{faces}')

        # key input
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        elif k == ord('k'):
            print(f'korigori')
            korigori_flag = True
    
    cap.release()
    cv2.destroyAllWindows()
    
    pass

# 絶対に分ける必要のなかったメイン
def main():
    show_camera()

if __name__ == "__main__":
    main()