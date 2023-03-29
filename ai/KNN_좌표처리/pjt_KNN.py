from sklearn.metrics import mean_absolute_error
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
import numpy as np


# 아마 여기에 Real Time 데이터가 넣어지지 않나. 싶음.

# 소켓으로 쏘아서 받으면 해당 list가 넘어옴. 넘어온 list들에 대해 def 해당 함수로 보내줘야 함.

# 아마 여기까지 Real Time 데이터이지 않나. 싶음.


# 음성 인식 처리.

if STT.data == "squat":
    squat()

elif STT.data == "push":
    push()

elif STT.data == "jump":
    jump()

# 음성의 해당 운동에 따라 함수 호출.

# 음성 인식 처리.


################# 대충 계획한 KNN 공식 시자악###################

# 1. Train_data.xlsx is ready? (O)
# 2. KNN Calc

# 2.1 KNN new Func is ready? (O) ACC : 80%

# if (new_data_inpput(knn(n)) -> correct!) now called answer_data_matrix
# else (!new_data_input(knn(n)) -> incorrect!) now called !answer_data_matrix

# if data is incorrect. append skeleton point

# 3. cmp count of answer_data_matrix and !answer_data_matrix

# 3.1 if speicfic number below return BAD + 1, else Good + 1

# 4. cmp answer sheet length if correct with Good return REAL_CNT+1 to DB

# 5. but BAD length is upper then 0

# 5.1 BAD cmp with answer[0, 1:33] find 0, append to body list, return REAL_BAD+1 to DB and wrong move to DB?

################ 대충 계획한 KNN 공식 끝#####################

# KNN Squat DataFrame

def squat():
    move = pd.read_excel(
        '/content/drive/MyDrive/RNN_Test/dataset4/Back_test3_Ver3.xlsx')

    move_input = move[['right_sight_x', 'right_sight_y', 'left_sight_x', 'left_sight_y', 'right_hip_x', 'right_hip_y', 'left_hip_x', 'left_hip_y',
                       'right_sh_x', 'right_sh_y', 'left_sh_x', 'left_sh_y'
                       ]].to_numpy()
    move_output = move['label'].to_numpy()

    train_input = move_input[0:764, 0:12]
    train_target = move_output[0:764]

    test_input = move_input[764:, 0:12]
    test_target = move_output[764:]

    ss = StandardScaler()
    ss.fit(train_input)
    train_scaled = ss.transform(train_input)
    test_scaled = ss.transform(test_input)

    sc = SGDClassifier(loss='log', max_iter=10, random_state=400)
    sc.fit(train_scaled, train_target)

    sc = SGDClassifier(loss='log', max_iter=10, random_state=400)
    sc.fit(train_scaled, train_target)
    
    sc = SGDClassifier(loss='log', random_state=400)

    train_score = []
    test_score = []

    classes = np.unique(train_target)

    for _ in range(0, 500):
      sc.partial_fit(train_scaled, train_target, classes=classes)

      train_score.append(sc.score(train_scaled, train_target))
      test_score.append(sc.score(test_scaled, test_target))

      sc = SGDClassifier(loss='log', max_iter=10, tol=None, random_state=390)
      
    sc.fit(train_scaled, train_target)

    print(sc.score(train_scaled, train_target))
    print(sc.score(test_scaled, test_target))

    kn = KNeighborsClassifier()

    kn.fit(train_scaled, train_target)

    kn.score(test_scaled, test_target)


    test = kn.predict(test_scaled)

    print(kn.score(train_scaled, train_target))

    kn.n_neighbors = 11

    kn.fit(train_scaled, train_target)
    print(kn.score(train_scaled, train_target))
    print(kn.score(test_scaled, test_target))

    print(train_scaled)

    ans = []
    ans = kn.predict(test_scaled)


def Push():

    # Train data
    move = pd.read_excel(
        'C:\\Users\\multicampus\\Desktop\\Tensor\\Back_test1_Ver2.xlsx')

    move.shape

    cell = move.iloc[1:738, 1:35]

    label = move.iloc[1:738, 35]

    test_cell = move.iloc[740:, 1:35]

    kn = KNeighborsClassifier()

    kn.fit(cell, label)

    kn.score(cell, label)

    ans = []
    ans = kn.predict(test_cell)

    print(ans)


def Jump():

    # Train data
    move = pd.read_excel(
        'C:\\Users\\multicampus\\Desktop\\Tensor\\Back_test2_Ver2.xlsx')

    move.shape

    cell = move.iloc[1:738, 1:35]

    label = move.iloc[1:738, 35]

    test_cell = move.iloc[740:, 1:35]

    kn = KNeighborsClassifier()

    kn.fit(cell, label)

    kn.score(cell, label)

    ans = []
    ans = kn.predict(test_cell)
