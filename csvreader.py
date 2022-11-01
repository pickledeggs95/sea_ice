import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def add_to_radar(year_index, color):
    global df
    global ax
    global years
    global maximum
    values = df.loc[year_index].tolist()
    values += values[:1]
    n=int(max(values))
    if n > maximum:
        maximum=(max(values))
    else:
        pass
    if year_index==(len(df)-1):
        ax.plot(angles, values, color=color, linewidth=0)
        ax.fill(angles, values, color=color, alpha=0.2, label="2022")
    else:
        ax.plot(angles, values, color=color, linewidth=0)
        ax.fill(angles, values, color=color, alpha=0.2)

df=pd.read_csv('C:\\Users\\Liam\\python\\learning\\sea_ice\\sea_ice.csv')
df=df.iloc[: , 1:]
label=pd.read_csv('C:\\Users\\Liam\\python\\learning\\sea_ice\\sea_ice.csv', nrows=0)
label = label.iloc[: , 1:]
label=list(label)
years=pd.read_csv('C:\\Users\\Liam\\python\\learning\\sea_ice\\sea_ice.csv').iloc[:,0]


values = df.loc[0].tolist()
num_vars=len(label)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
values += values[:1]
maximum=(max(values))
angles += angles[:1]
label += label[:1]

fig, ax = plt.subplots(figsize=(5, 7), subplot_kw=dict(polar=True))
ax.plot(angles, values, color='#0090FA', linewidth=0)
ax.fill(angles, values, color='#0090FA', alpha=0.2,label="1979")

R=0
G=144
B=250
x=range(1,len(df))

for i in x:
    R+=5
    G-=2
    B-=4
    hex=rgb_to_hex((R, G, B))
    add_to_radar(i,hex)

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_thetagrids(np.degrees(angles), label)
ax.set_ylim(0, maximum)
ax.set_rlabel_position(0)

labels = ('1979','2022')

ax.tick_params(colors='#222222')
ax.tick_params(axis='y', labelsize=5)
ax.grid(color='#AAAAAA')
ax.spines['polar'].set_color('#222222')
ax.set_facecolor('#FAFAFA')
ax.set_title('''September Arctic Sea Ice Extent (km) 1979-2022
Data from (https://masie_web.apps.nsidc.org)''', y=1.2)

ax.legend(loc='upper center', bbox_to_anchor=(0.9, 1.15))

plt.show()