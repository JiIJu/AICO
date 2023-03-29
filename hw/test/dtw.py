from dtaidistance import dtw

a = [1, 2, 5, 7, 4, 3, 6, 8, 2, 1]
b = [1, 2, 5, 7, 4, 3, 6, 8, 2, 1]
distance = dtw.distance(a, b)
print(distance)