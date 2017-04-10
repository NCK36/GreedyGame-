# -*- coding: utf-8 -*-
"""
Created on Sat Apr 08 11:17:31 2017

@author: Navin Chandan
"""
import json, datetime, matplotlib
data_file = "C:/Users/navinchandan0/Documents/Data Dump, for data assignment ggevent.log/ggevent.log"

with open(data_file) as file:
    lines = file.read().splitlines()

dic_file = []

for i in lines:
    dic_file.append(json.loads(i))

gme = set()
for i in dic_file:
    gme.add(i["bottle"]["game_id"])

game_dic = {}
game_dev = {}
time_data = {}
for j in gme:
    game_dic[j] = []
    game_dev[j] = {}
    time_data[j] = {}
    
for i in dic_file:
    temp_lst = [i["headers"]["ai5"], i["headers"]["sdkv"], i["post"]["event"],i["post"]["ts"],i["bottle"]["timestamp"]]
    game_dic[i["bottle"]["game_id"]].append(temp_lst)

for i in gme:
    temp_dev = set()
    for j in game_dic[i]:
        temp_dev.add(j[0])
    
    for j in temp_dev:
        game_dev[i][j] = []
        time_data[i][j] = []
    
    for j in game_dic[i]:
        temp_lst = [j[1], j[2], j[3], j[4]]
        game_dev[i][j[0]].append(temp_lst)

for i in game_dev:
    for j in game_dev[i]:
        for k in game_dev[i][j]:
            temp_time = k[3]
            k[3] = datetime.datetime.strptime(temp_time, "%Y-%m-%d %H:%M:%S.%f")
        game_dev[i][j] = sorted(game_dev[i][j], key=lambda x: x[3])

total_valid = 0
total_inv = 0
total_time = 0.0
descrip = 0
for i in game_dev:
    for j in game_dev[i]:
        temp_lst = game_dev[i][j]
        valid = 0
        invalid = 0
        total_v = 0
        sess_time = 0
        ggstart = None
        ggstop = None
        for k in range(0, len(temp_lst)):
            if temp_lst[k][1] == 'ggstop':
                if ggstop == None:
                    if ggstart != None:
                        ggstop = k
                        tmp_t = (temp_lst[ggstop][3]-temp_lst[ggstart][3]).total_seconds()
                        sess_time += tmp_t
                    else:
                        descrip += 1
                else:
                    descrip += 1
            if temp_lst[k][1] == 'ggstart':
                if ggstop==None:
                    if ggstart != None:
                        descrip += 1
                    ggstart = k
                else:
                    if (temp_lst[k][3]-temp_lst[ggstop][3]).total_seconds() >= 30:
                        if sess_time >= 60:
                            valid += 1
                            total_v += sess_time
                        elif sess_time > 1:
                            invalid += 1
                        sess_time = 0
                    ggstart = k
                    ggstop = None
        if sess_time >= 60:
            valid += 1
            total_v += sess_time
        elif sess_time > 1:
            invalid += 1

        time_data[i][j] = [valid, invalid, total_v]
        total_valid += valid
        total_inv += invalid
        total_time += total_v

average_t = total_time/total_valid
total_sess = total_valid + total_inv

print("Number of valid Session: %d" % total_valid )
print("Number of Total Session: %d" % total_sess)
print("Average time of Valid Session: %f" % average_t)
print("Descrepency in Data: %d" % descrip)

# Insights about users

game_user = []
time_spent = []
for i in time_data:
    t = 0.0
    users = set()
    for j in time_data[i]:
        users.add(j)
        t += time_data[i][j][2]
    game_user.append(len(users))
    time_spent.append(t / len(users))

import matplotlib.pyplot as plt
import numpy as np
# Data to plot
labels = list(map(str, range(1, 21)))
sizes = list(map(np.log10, game_user))

# Bar Plot

y = sizes
N = len(y)
x = range(N)
width = 1/1.5
fig = plt.figure()
plt.xlabel('game_id')
plt.ylabel('log of numbers of users')

ax = plt.subplot(111)
ax.bar(x, y,width, color="red")
plt.title('No of Users per Game')
fig.savefig('plot.png')

sizes = time_spent

# Bar CHart

y = time_spent
N = len(y)
x = range(N)
width = 1/1.5
fig = plt.figure()
plt.xlabel('game_id')
plt.ylabel('Average time spent per user (seconds)')

ax = plt.subplot(111)
ax.bar(x, y,width, color="red")
plt.title('Average time spent per Game')
fig.savefig('plot1.png')

users = set()
for i in time_data:
    for j in time_data[i]:
        users.add(j)

time_user = np.zeros(len(users))
user_dict = {}
index = 0
for i in users:
    user_dict[i]=index
    index+=1

for i in time_data:
    for j in time_data[i]:
        time_user[user_dict[j]] += time_data[i][j][2]

import matplotlib.pyplot as plt
x = time_user
fig = plt.figure()
plt.xlabel('time spent (sec)')
plt.ylabel('Fraction of users')

ax = plt.subplot(111)
ax.hist(x, normed=True, bins=30,color='red')
plt.title('User vs Time Spent')
fig.savefig('plot2.png')

