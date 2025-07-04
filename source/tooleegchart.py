
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

eeg_width = 512
eeg_data = []
eeg_result = []

eeg_result_x = []
eeg_result_y = []

eeg_file = open('data\Z_All.txt', "r")   # 파일을 연다
for line_data in eeg_file:
    eeg_data.append(abs(float(line_data.replace('\n',''))))

np_eeg_data = np.array(eeg_data)
for i in range(0, len(np_eeg_data) // eeg_width):
    eeg_width_data = np_eeg_data[(i * eeg_width) : (i + 1) * eeg_width]
    for j in range(0, len(eeg_width_data), 100):
        eeg_result_x.append(eeg_width_data[j])
        eeg_result_y.append(eeg_width_data[j + 1])
    plt.scatter(eeg_result_x, eeg_result_y)
    plt.savefig("eegImages\eegfig" + str(i) + ".png", dpi=600)
    plt.clf()
    eeg_result_x.clear()
    eeg_result_y.clear()


    #eeg_width_data2 = eeg_width_data ** 2
    #eeg_result.append(np.mean(eeg_width_data))
    #eeg_result.append(np.median(eeg_width_data))
    #eeg_result.append(np.mean(eeg_width_data2))
    #eeg_result.append([np.mean(eeg_width_data), np.median(eeg_width_data), np.mean(eeg_width_data2)])

#df4eeg_result = pd.DataFrame(eeg_result, columns=['mean', 'median', 'mean2'])
#df4eeg_result = pd.DataFrame(eeg_result)
#df4eeg_result.to_csv('eeg_result11111111.csv', index=False, header=False, encoding='cp949')
#print(eeg_result)



#xData = np.arange(20, 50)
#yData = xData + 2* np.random.randn(30)  # xData에 randn() 함수로 잡음을 섞는다.
# 잡음은 정규분포로 만들어 질 것이다.

#plt.scatter(eeg_result_x, eeg_result_y)
#plt.title('Real Age vs Physical Age')
#plt.xlabel('Real Age')
#plt.ylabel('Physical Age')

#plt.savefig("age.png", dpi=600)
#plt.show()