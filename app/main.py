
from flask import Flask, jsonify,request
import time

import numpy as np
from stl import mesh
import requests







app = Flask(__name__);
@app.route("/bot", methods=["POST"])
def response():
    url = 'https://firebasestorage.googleapis.com/v0/b/dismo-45c00.appspot.com/o/soner.stl?alt=media&token=e97408ce-0253-46c3-b755-72024bb4a1d2'
r = requests.get(url, allow_redirects=True)

open('model1.stl', 'wb').write(r.content)

c1 = mesh.Mesh.from_file('model1.stl')
c2 = c1

volume1, cog1, inertia = c1.get_mass_properties()


volume2, cog2, inertia = c2.get_mass_properties()



#buradaki elde ettiğimiz değerler tüm noktaların ötelenecek değerleri cube2 nin
#her noktasının x y ve z noktalarına bu değerler eklenerek cube 2 ve cube 1 üst üste getirilecek
ox = cog1[0]-cog2[0]
oy = cog1[1]-cog2[1]
oz = cog1[2]-cog2[2]


for i in c1.vectors:

    i[0][0] += ox
    i[0][1] += oy
    i[0][2] += oz

    i[1][0] += ox
    i[1][1] += oy
    i[1][2] += oz

    i[2][0] += ox
    i[2][1] += oy
    i[2][2] += oz



#list1=np.ndarray((len( c1.vectors),3,3),dtype=float)

#1.OBJE İÇİN OLAN KISIM

list1=np.ndarray(((len( c1.vectors)*c1.vectors.shape[1]),3),dtype=float)
o=0
#c1 x y z toplamı
c1xTop=0;
c1yTop=0;
c1zTop=0;
#c2 x y z toplamı
c2xTop=0;
c2yTop=0;
c2zTop=0;
while o< len(list1):
    for i in range(len(c1.vectors)):

        for j in range(c1.vectors.shape[1]):
            list1[o] = c1.vectors[i][j]
            o=o+1
            c1xTop+=c1.vectors[i][j][0];
            c1yTop += c1.vectors[i][j][1];
            c1zTop += c1.vectors[i][j][2];


#2.OBJE İÇİN OLAN KISIM
list2 = np.ndarray(((len(c2.vectors) * c2.vectors.shape[1]), 3), dtype=float)
a = 0
while a < len(list2):
    for i in range(len(c2.vectors)):

        for j in range(c2.vectors.shape[1]):
            list2[a] = c2.vectors[i][j]
            a = a + 1
            c2xTop += c2.vectors[i][j][0];
            c2yTop += c2.vectors[i][j][1];
            c2zTop += c2.vectors[i][j][2];
buyukX=c1xTop;
kucukX=c2xTop;
if(c2xTop>c1xTop):
    buyukX =c2xTop;
    kucukX = c1xTop;
buyukY=c1yTop;
kucukY=c2yTop;
if(c2yTop>c1yTop):
    buyukY =c2yTop;
    kucukY = c1xTop;
buyukZ=c1zTop;
kucukZ=c2zTop;""
if(c2zTop>c1zTop):
    buyukZ =c2zTop;
    kucukZ = c1zTop;

xTopOran =buyukX/kucukX;
yTopOran =buyukY/kucukY;
zTopOran =buyukZ/kucukZ;
if(xTopOran<0):
    xTopOran=xTopOran*-1;
if(yTopOran<0):
    yTopOran=yTopOran*-1;
if(zTopOran<0):
    zTopOran=zTopOran*-1;

#oranlar negatifse pozitife dönüştürlecek




distanceList = []

tempList =[]

kucukList=list1
if(len(list2)<len(list1)):
    kucukList=list2
for k in range(len(kucukList)):
 
    d1 = np.sqrt((list1[k][0] - list2[k][0]) ** 2 + (list1[k][1] - list2[k][1]) ** 2 + (
            list1[k][2] - list2[k][2]) ** 2)
   
    if(k<len(kucukList)-2):
        d2 = np.sqrt((list1[k][0] - list2[k + 1][0]) ** 2 + (list1[k][1] - list2[k + 1][1]) ** 2 + (
                list1[k][2] - list2[k + 1][2]) ** 2)
        d3 = np.sqrt((list1[k][0] - list2[k + 2][0]) ** 2 + (list1[k][1] - list2[k + 2][1]) ** 2 + (
                list1[k][2] - list2[k + 2][2]) ** 2)

    else:
        d2=d1
        d3=d1


    tempList.append(d1)
    tempList.append(d2)
    tempList.append(d3)

    temp=tempList[0]
    for m in tempList:

        if(m<temp):
            temp=m
    
    distanceList.append(temp)
    
    tempList.clear()


#puanlama deneme
onePerH=0
twoPerH=0
fourPerH=0
sixPerH=0

facesO1 = len(c1.points)
facesO2 = len(c2.points)
kucukFace = facesO1
buyukFace = facesO2
if(facesO2<facesO1):
    minFace=facesO2
    buyukFace=facesO1
facesOran=kucukFace/buyukFace
kucukV = volume1
buyukV = volume2
if(volume2<volume1):
    kucukV=volume2
    buyukV=volume1
VolumeOran=kucukV/buyukV
for p in distanceList:
    if(p<2):
        onePerH+=1
    elif(2<=p<=5):
        twoPerH+=1
    elif(5<p<=8):
        fourPerH+=1
    elif(8<p):
        sixPerH+=1

#yeni puanlama deneme
if(VolumeOran>=0.94 and facesOran>=0.94 and onePerH==0 and twoPerH==0 and fourPerH==0 ):
    onePerH=0;
    twoPerH=0;
    fourPerH=0;
    sixPerH=0;
    for p in distanceList:
        if (p > 10):
            p = p / 10;
        if (p < 2):
            onePerH += 1
        elif (2 <= p <= 5):
            twoPerH += 1
        elif (5 < p <= 8):
            fourPerH += 1
        elif (8 < p):
            sixPerH += 1


oo= onePerH/len(distanceList)
to= twoPerH/len(distanceList)
fo= fourPerH/len(distanceList)
so= sixPerH/len(distanceList)
tempPuan=150-((to*0.5*100)+(fo*1*100)+(so*2.5*100))

oriPuan=100*tempPuan/150


if(oriPuan<=50):
    oriPuan+=(facesOran*10)
   
    if(VolumeOran>=0.7):
        oriPuan+=(VolumeOran*10)
       
elif(50<oriPuan<70):
    oriPuan+=(VolumeOran*5)
    
    oriPuan+=(facesOran*5)
    
if(oriPuan<0):
    oriPuan*=-1
    
    oriPuan = 100-(oriPuan*1.5);
    if(50<=oriPuan<=70):
        oriPuan=oriPuan/2;
    if (70 < oriPuan <= 100):
        oriPuan = oriPuan / 3;
    #bu kısmı kapattım farklı deneme yoksa sonuç -1 se benzereliği çok yüksek yapıyor
   


if(VolumeOran>=0.9 and facesOran>=0.9 and oriPuan<=45):

    oriPuan += (VolumeOran * 10)
    
    oriPuan += (facesOran * 10)
    
#bu kısımdaki maks kısım arttırılıp oranı yüksek olana ek puan verilebilir
if(45<=oriPuan<=70 and VolumeOran>=0.95 and facesOran>=0.95):
    oriPuan=oriPuan+10;


oranKontrolSayi=0;
if(0.5<=xTopOran<=1.5):
    oranKontrolSayi+=1;
if(0.5<=yTopOran<=1.5):
    oranKontrolSayi+=1;
if(0.5<=zTopOran<=1.5):
    oranKontrolSayi+=1;

if(oranKontrolSayi==3 and 50<=oriPuan<=80):
    oriPuan+=10;
elif(oranKontrolSayi==2 and 50<=oriPuan<=80):
    oriPuan+=6;
elif(oranKontrolSayi==1 and 50<=oriPuan<=80):
    oriPuan+=3;

#yeni puanlama deneme bitiş


puanStr= str(oriPuan)

    query = dict(request.form)['query']
    res = query + " " + "naber brooooo güncelledin mi ? "
    return jsonify({"response" : puanStr})
if __name__=="__main__":
    app.run(host="0.0.0.0",)
