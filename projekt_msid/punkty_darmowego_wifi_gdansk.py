import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import seaborn as sns
import pandas as pd
import geocoder

datafr=pd.read_csv('./punkty_darmowego_wifi.csv',sep=';',encoding = "UTF-8")       #czytanie pliku

punkty_wifi=[]

for i in range(0,104):
    g = geocoder.osm(datafr.iat[i,1]+',Gdańsk')                                       #wyszukiwanie szerokosc i wysokosci geograficznej w osm
    if(g.osm!=None):                                                                  #wyszukiwanie chwile potrwa, cierpliwości
        punkty_wifi.append([g.osm['x'],g.osm['y'],datafr.iat[0,3],datafr.iat[0,4]])   #dodawanie adresów oraz przepływów danych naszych punktów wifi


def odleglosc_i_sila(I, punkty_wifi):
    x, y = I
    tx, ty,transfer_przych,transfer_wych = punkty_wifi
    dystans = np.sqrt((x-tx)*(x-tx) + (y-ty)*(y-ty))
    return (float(transfer_wych)+float(transfer_przych))/(1+dystans)/10000000        #na końcu dzielimy przez 10000000, zeby nie operowac na duzych liczbach, nie zmienia to koncowego wyniku

def Fcelu4(I):
    return -sum([odleglosc_i_sila(I, punkt_wifi) for punkt_wifi in punkty_wifi]) 

x = np.linspace(18.45, 18.95)
y = np.linspace(54.25, 54.45)


ograniczenia = {'y': (18.45, 18.95),                                                         #ograniczenia pochodzą ze najdalej wysuniętych punktów Gdańska
                'x': (54.25, 54.45)}

x0 = (np.random.uniform(*ograniczenia['y']),
      np.random.uniform(*ograniczenia['x']))                                                 #optymalizujemy funkcje z ograniczeniami
x_opt = optimize.minimize(Fcelu4, x0, method='TNC', bounds=list(ograniczenia.values())).x

#minimum globalne znajdujące się w punkcie o współrzędnych  18.642213948160073, 54.359146103144845
#budynek o tych wspólrzędnych to Ateneum-Akademia Nauk Stosowanych w Gdańsku
#tam najbardziej opłaca się postawić następny darmowy punkt wi-fi

mesh_x, mesh_y = np.meshgrid(x, y)
mesh_z = np.clip(Fcelu4([mesh_x, mesh_y]), -1000000, 0)

cmap = 'Spectral_r'
fig = plt.figure(figsize=(15,5))
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.plot_surface(mesh_x, mesh_y, mesh_z, cmap=cmap) 
ax = fig.add_subplot(1, 2, 2)                                                                  #wyświetlamy funkcje
c = ax.contourf(mesh_x, mesh_y, mesh_z, cmap=cmap)
c2 = ax.contour(mesh_x, mesh_y, mesh_x, colors='black')
ax.set_aspect('equal')
fig.colorbar(c, ax=ax)
plt.clabel(c2, inline=True, fontsize=10)
plt.show()
