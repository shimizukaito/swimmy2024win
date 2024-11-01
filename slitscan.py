import cv2
import numpy as np
import time

# 動画キャプチャを開始
cap = cv2.VideoCapture(1)

# カメラが正しく開けているか確認
if not cap.isOpened():
    print("カメラが開けませんでした。")
    exit()

# 初期設定：フレームサイズとスリットを保存するキャンバス
ret, frame = cap.read()
if not ret:
    print("フレームが取得できませんでした。")
    cap.release()
    exit()

height, width, _ = frame.shape
slit_width = 10  # 各スリットの幅
slit_count = height  # 追加したいスリットの数
slit_spacing = 20  # スリット間の間隔
slit_canvas = np.zeros((height, width, 3), dtype=np.uint8)

# ループ処理で動画をフレームごとに取得
y_position = 0  # スリットの開始位置を管理
direction = "vertical"  # 初期のスリットの方向
change_time = time.time()  # 最後に方向を切り替えた時間
switch_interval = 5  # スリット方向を切り替える間隔（秒）

while True:
    ret, frame = cap.read()
    if not ret:
        print("フレームの読み込みに失敗しました。")
        break

    # スリットの方向を切り替える
    if time.time() - change_time > switch_interval:
        direction = "horizontal" if direction == "vertical" else "vertical"
        change_time = time.time()  # 最後に切り替えた時間を更新

    # 複数のスリットを追加
    if direction == "vertical":
        for i in range(slit_count):
            current_y = (y_position + i * (slit_width + slit_spacing)) % height
            slit = frame[current_y:current_y + slit_width, :, :]
            slit_canvas[current_y:current_y + slit_width, :, :] = slit

        # 次のスリット位置へ移動
        y_position += slit_width
        if y_position >= height:
            y_position = 0  # スリットが下端に達したらリセット
    else:  # direction == "horizontal"
        for i in range(slit_count):
            current_x = (y_position + i * (slit_width + slit_spacing)) % width
            slit = frame[:, current_x:current_x + slit_width, :]
            slit_canvas[:, current_x:current_x + slit_width, :] = slit

        # 次のスリット位置へ移動
        y_position += slit_width
        if y_position >= width:
            y_position = 0  # スリットが右端に達したらリセット

    # 結果を表示
    cv2.imshow('Slit Scan - Direction Change', slit_canvas)

    # ESCキーが押されたら終了
    if cv2.waitKey(1) & 0xFF == 27:
        break

# リソースの解放
cap.release()
cv2.destroyAllWindows()
