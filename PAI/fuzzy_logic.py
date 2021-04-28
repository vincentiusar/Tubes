## Library

import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter as xlw

"""## Data"""

data = pd.read_excel(r'D:\Downloads\\' + 'restoran.xlsx')
data

"""## Fuzzification

### Kategori Makanan"""

food = [3, 4, 5, 7, 8, 9]

def highFood(x) :
  if x > food[5] :
    return 1
  elif x <= food[3] :
    return 0
  elif x <= food[5] and x > food[3] :
    return (x - food[3])/(food[5] - food[3])

def medFood(x) :
  if x <= food[0] or x >= food[4] :
    return 0
  elif x == food[2] :
    return 1
  elif x < food[2] and x > food[0] :
    return (x - food[0])/(food[2] - food[0])
  elif x < food[4] and x > food[2] :
    return (food[4] - x)/(food[4] - food[2])

def lowFood(x) :
  if x <= food[0] :
    return 1
  elif x > food[1] :
    return 0
  elif x <= food[1] and x > food[0] :
    return (food[1] - x)/(food[1] - food[0])

y1 = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
y2 = [0, 0, 0, 0.5, 1, 0.66, 0.33, 0, 0, 0]
y3 = [0, 0, 0, 0, 0, 0, 0, 0.5, 1, 1]

rating = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

plt.plot(rating, y1, label="Low")
plt.plot(rating, y2, label="Med")
plt.plot(rating, y3, label="High")
plt.legend(title='Kualitas Makanan')
plt.show()

"""### Kategori Pelayanan"""

service = [30, 40, 70, 75, 80, 90]

def highService(x) :
  if x > service[5] :
    return 1
  elif x <= service[2] :
    return 0
  elif x <= service[5] and x > service[2] :
    return (x - service[2])/(service[5] - service[2])

def medService(x) :
  if x <= service[0] or x > service[4] :
    return 0
  elif x >= service[2] and x <= service[3] :
    return 1
  elif x < service[2] and x > service[0] :
    return (x - service[0])/(service[2] - service[0])
  elif x <= service[5] and x > service[3] :
    return (service[5] - x)/(service[5] - service[3])

def lowService(x) :
  if x <= service[0] :
    return 1
  elif x > service[1] :
    return 0
  elif x <= service[1] and x > service[0] :
    return (service[1] - x)/(service[1] - service[0])

y1 = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
y2 = [0, 0, 0, 0.25, 0.5, 0.75, 1, 1, 0.66, 0.33, 0, 0, 0]
y3 = [0, 0, 0, 0, 0, 0, 0, 0.25, 0.5, 0.75, 1, 1, 1]

rating = [10, 20, 30, 40, 50, 60, 70, 75, 80, 85, 90, 95, 100]

plt.plot(rating, y1, label="Low")
plt.plot(rating, y2, label="Med")
plt.plot(rating, y3, label="High")
plt.legend(title='Kualitas Pelayanan')
plt.show()

"""## Inferensi"""

def inference(x, y) :
  nk = []

  foodQ = []
  if x < food[4] and x > food[3] :
    foodQ.append([highFood(x), 'high'])
    foodQ.append([medFood(x), 'med'])
  elif x < food[1] and x > food[0] :
    foodQ.append([medFood(x), 'med'])
    foodQ.append([lowFood(x), 'low'])
  elif x <= food[0] :
    foodQ.append([lowFood(x), 'low'])
  elif x <= food[3] and x >= food[1] :
    foodQ.append([medFood(x), 'med'])
  elif x >= food[4] :
    foodQ.append([highFood(x), 'high'])

  serviceQ = []
  if y < service[5] and y >= service[2] :
    serviceQ.append([highService(y), 'high'])
    serviceQ.append([medService(y), 'med'])
  elif y <= service[1] and y > service[0] :
    serviceQ.append([medService(y), 'med'])
    serviceQ.append([lowService(y), 'low'])
  elif y <= service[0] :
    serviceQ.append([lowService(y), 'low'])
  elif y < service[4] and y > service[1] :
    serviceQ.append([medService(y), 'med'])
  elif y >= service[5] :
    serviceQ.append([highService(y), 'high'])

  print("inferensi : ", foodQ, serviceQ)

  for i in range(len(foodQ)) :
    for j in range(len(serviceQ)) :
      if foodQ[i][1] == 'high' and serviceQ[j][1] == 'high' :
        nk.append([min(foodQ[i][0], serviceQ[j][0]), 'tinggi'])
      if foodQ[i][1] == 'high' and serviceQ[j][1] == 'med' :
        nk.append([min(foodQ[i][0], serviceQ[j][0]), 'tinggi'])
      if foodQ[i][1] == 'high' and serviceQ[j][1] == 'low' :
        nk.append([min(foodQ[i][0], serviceQ[j][0]), 'dipertimbangkan'])
      if foodQ[i][1] == 'med' and serviceQ[j][1] == 'high' :
        nk.append([min(foodQ[i][0], serviceQ[j][0]), 'tinggi'])
      if foodQ[i][1] == 'med' and serviceQ[j][1] == 'med' :
        nk.append([min(foodQ[i][0], serviceQ[j][0]), 'dipertimbangkan'])
      if foodQ[i][1] == 'med' and serviceQ[j][1] == 'low' :
        nk.append([min(foodQ[i][0], serviceQ[j][0]), 'rendah'])
      if foodQ[i][1] == 'low' and serviceQ[j][1] == 'high' :
        nk.append([min(foodQ[i][0], serviceQ[j][0]), 'dipertimbangkan'])
      if foodQ[i][1] == 'low' and serviceQ[j][1] == 'med' :
        nk.append([min(foodQ[i][0], serviceQ[j][0]), 'rendah'])
      if foodQ[i][1] == 'low' and serviceQ[j][1] == 'low' :
        nk.append([min(foodQ[i][0], serviceQ[j][0]), 'rendah'])

    for i in range(len(nk)) :
      for j in range(i + 1, len(nk)) :
        if nk[i][1] == nk[j][1] :
          if nk[i][0] < nk[j][0] :
            del nk[i]
          else :
            del nk[j]
    return nk

"""## Defuzzification

"""

y1 = [1, 1, 0.5, 0, 0, 0, 0, 0, 0, 0]
y2 = [0, 0, 0, 0, 1, 1, 0.5, 0, 0, 0]
y3 = [0, 0, 0, 0, 0, 0, 0, 0.33, 0.66, 1]

rating = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
plt.plot(rating, y1, label="rendah")
plt.plot(rating, y2, label="dipertimbangkan")
plt.plot(rating, y3, label="tinggi")
plt.legend(title='Deffuzification')
plt.show()

"""### Fungsi tambahan"""

def fh(x) :
  return float(30 * x + 70)

def fm(x) :
  return float(10 * x + 40), float(-20 * x + 80)

def fl(x) :
  return float(-20 * x + 40)

"""### Fungsi Defuzzy"""

defuz = [10, 20, 30, 40, 50, 60, 70, 80]

def defuzzification(x) :
  pembilang = 0
  penyebut = 0
  for i in range(len(x)) :
    if x[i][0] != 0 :
      if x[i][1] == 'tinggi' :
        tmp = 1
        while tmp > 0.3 :
          if x[i][0] <= tmp :
            pembilang += x[i][0] * fh(tmp)
            penyebut += x[i][0]
          else :
            pembilang += tmp * fh(tmp)
            penyebut += tmp
          tmp -= 0.15
      elif x[i][1] == 'dipertimbangkan' :
        tmp = 1
        while tmp >= 0.2 :
          x1, x2 = fm(tmp)
          if x[i][0] <= tmp :
            pembilang += x[i][0] * (x1 + x2)
            penyebut += x[i][0] * 2
          else :
            pembilang += tmp * (x1 + x2)
            penyebut += tmp * 2
          tmp -= 0.15
      elif x[i][1] == 'rendah' :
        tmp = 1
        while tmp > 0.2 :
          if x[i][0] <= tmp :
            pembilang += x[i][0] * fl(tmp)
            penyebut += x[i][0]
          else :
            pembilang += tmp * fl(tmp)
            penyebut += tmp
          tmp -= 0.15
  return pembilang / penyebut

frag = []
for i in range(len(data)) :
  nk = inference(data["makanan"][i], data["pelayanan"][i])
  print(i + 1)
  print('infe : ', nk)
  print('defuz : ', defuzzification(nk), end='\n\n')
  frag.append([defuzzification(nk), i + 1])

frag.sort(key = lambda x: x[0], reverse=1)
for item in frag :
  print(item)

tmp = input('enter untuk print excel')
"""# Hasil 10 terbaik"""

terbaik = []
for i in range(10) :
  terbaik.append(frag[i][1])
terbaik

df = xlw.Workbook('peringkat.xlsx')
ds = df.add_worksheet()
row, coloumn = 0, 0

for item in terbaik :
  ds.write(row, coloumn, item)
  row += 1

df.close()

tmp = input('enter to exit')