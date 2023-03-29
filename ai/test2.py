def update(self):
        move = pd.read_excel(
            'C:\\Users\\multicampus\\Desktop\\gogo\\S08P12C102\\web\\logintest\\record\\real_test_Ver2.xlsx')

        cell = move.iloc[1:3332, 0:34]
        label = move.iloc[1:3332, 34]
        kn = KNeighborsClassifier()

        kn.n_neighbors = 5
        kn.fit(cell, label)

        zero = 0
        first = 0
        second = 0

        cycle01 = 0
        cycle10 = 0
        cycle02 = 0
        cycle20 = 0
        
        self.good = 0
        self.bad = 0

        while 1:
            try:
                packet = self.server_socket.recvfrom(100000000)
            except BlockingIOError:
                continue

            data = packet[0]
            self.data = pickle.loads(data)  # oriData[1] : 자세데이터

            self.ans = kn.predict([self.data[1]])

            if zero == 0 and self.ans == 0: 
                zero = 1
            
            elif zero == 1 and first == 0 and self.ans == 1 :  
                zero = 0
                first = 1
                cycle01 += 1
                
            elif zero == 0 and first == 1 and self.ans == 0 :
                zero = 1
                first = 0
                cycle10 += 1
                
            elif zero == 1 and second == 0 and self.ans == 2 :
                zero = 0
                second = 1
                cycle02 += 1
            
            elif zero == 0 and second == 1 and self.ans == 0 :
                zero = 1 
                second = 0
                cycle20 += 1
                
                
            if cycle20 == 1 and cycle02 == 1 and cycle