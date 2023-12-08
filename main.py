import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('mexico_crime.csv')

# гипотеза
print("Статическая гипотеза: Каждый год кол-во преступлений в Мексике увеличивается.")
total_crimes_per_year = df.groupby('year')['count'].sum()

# вывод кол-ва преступлений каждый год
print(total_crimes_per_year)

# Проверка гипотезы
trend = all(total_crimes_per_year.diff().dropna() > 0)
if trend:
    print("Гипотеза верна. Количество преступлений увеличивается с каждым годом.")
else:
    print("Гипотеза не верна. Количество преступлений не увеличивается с каждым годом.")


# Построение графика
df.groupby(["year"])["count"].sum().plot()
ax = plt.gca()
ax.ticklabel_format(style='plain', axis='y')
plt.xlabel("Year")
plt.ylabel("Total Crimes")
plt.title("Total Crimes per Year in Mexico")
plt.show()



