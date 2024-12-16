from random import shuffle
import pandas as pd
import matplotlib.pyplot as plt
import os


def str_to_float(s):
	n=''
	d=''
	b=0
	for i in s:
		if not b and i != '/':
			n+=i 
		if b:
			d+=i
		if i=='/':
			b=1
	return float(n)/float(d)



entries = []
print(os.listdir('pabulib'))
for str in os.listdir('pabulib'):
	entries+= os.listdir('pabulib/'+str)
print(len(entries))

df=pd.read_excel('results/test_greedy.ods')

X=[i for i in range(len(entries))]
S=[]
df2=pd.read_excel('results/test_mes.ods')
S2=[]
df3=pd.read_excel('results/test_mesc.ods')
S3=[]

measures=["avg_sat","gini","CC","ratio FS","dist_FS"]
for j in range(5):
	S=[]
	S2=[]
	S3=[]
	for st in entries: #change the index of columns when you want another measure
		S.append(df[st][3+j])
		S2.append(df2[st][3+j])
		S3.append(df3[st][3+j])
		#if df[st][3]!=df2[st][3]:
			#print("different")
	print('\n',measures[j],'\n')
	print('mes',sum(S2)/len(entries))
	print('mes xith completion',sum(S3)/len(entries))
	print('greedy',sum(S)/len(entries))

