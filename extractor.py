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

for st in entries: #change the index of columns when you want another measure
	S.append(df[st][4])
	S2.append(df2[st][4])
	S3.append(df3[st][4])
	#if df[st][3]!=df2[st][3]:
		#print("different")




for i in range(len(S)):
	min=S[i]
	k=i
	for j in range(i+1,len(S)):
		if S[j]<min:
			k=j 
			min=S[j]
	tmp=S[i]
	tmp2=S2[i]
	tmp3=S3[i]
	S[i]=min 
	S2[i]=S2[k]
	S3[i]=S3[k]
	S[k]=tmp 
	S2[k]=tmp2
	S3[k]=tmp3

print('mes',sum(S2)/len(S2))
print('mes xith completion',sum(S3)/len(S3))
print('greedy',sum(S)/len(S))





plt.figure()
plt.plot(X,S,label='greedy',color='red')
plt.plot(X,S2,label='mes',color='blue')
plt.plot(X,S3,label='mes comp',color='green')
plt.xlabel('instance')
plt.ylabel('Gini index')
#plt.yscale('log')
plt.title('Gini index')
plt.legend(loc='upper left')
plt.show()

