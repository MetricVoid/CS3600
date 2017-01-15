import pandas as pd
# %matplotlib inline
import matplotlib.pyplot as plt

df_car = pd.read_csv('q6_result_car.txt')
df_car.columns = ['Num Hidden Layer', 'Max Car', 'Average Car', 'STD Car']

df_pen = pd.read_csv('q6_result_pen.txt')
df_pen.columns = ['Num Hidden Layer', 'Max Pen', 'Average Pen', 'STD Pen']

df_pen['Max Car'] = df_car['Max Car']

df_pen['Average Car'] = df_car['Average Car']

df_pen['STD Car'] = df_car['STD Car']

df_merged = df_pen[['Num Hidden Layer', 'Max Pen', 'Max Car', 'Average Pen', 'Average Car', 'STD Pen', 'STD Car']]

df_merged = df_merged[['Num Hidden Layer', 'Max Pen', 'Max Car', 'Average Pen', 'Average Car', 'STD Pen', 'STD Car']]
df_merged.columns = [['Num Hidden Layer', 'Max Pen', 'Max Car', 'Average Pen Accuracy', 'Average Car Accuracy', 'STD Pen', 'STD Car']]

df_merged.set_index('Num Hidden Layer')

df_merged.plot(x='Num Hidden Layer', y=['Average Pen Accuracy', 'Average Car Accuracy'])
plt.show()