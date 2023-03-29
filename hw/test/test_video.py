import cv2


# 비디오 캡처 생성
cap = cv2.VideoCapture(0)
print('Frame width:', int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print('Frame height:', int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('Frame count:', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

# 비디오 캡처 반복
while(True):
    # 비디오 프레임 캡처
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    # 프레임 출력
    cv2.imshow('frame', frame)
    
    # 'q'키를 누르면 반복 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 캡처 종료
cap.release()
cv2.destroyAllWindows()