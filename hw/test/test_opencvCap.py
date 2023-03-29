import cv2


# 웹캠 연결
cap = cv2.VideoCapture(0)


# 웹캠에서 fps 값 획득
fps = cap.get(cv2.CAP_PROP_FPS)
print('fps', fps)


width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(width, height)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#writer = cv2.VideoWriter('./output.mp4', fourcc, fps, (width, height))
writer = cv2.VideoWriter('./1', fourcc, fps, (height, width))
cnt = 0
while True:

    # 웹캠에서 이미지 읽어옴
    ret,img_color = cap.read()

    if ret == False:
        print('웹캠에서 영상을 읽을 수 없습니다.')
        break
    img_color = cv2.rotate(img_color, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow("color", img_color)
    cv2.imwrite(f"./img/{cnt}.jpg", img_color)
    cnt = cnt + 1
    # ESC키 누르면 중지
    if cv2.waitKey(1)&0xFF == 27:
        break

cap.release()
writer.release()
cv2.destroyAllWindows()
