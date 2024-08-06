from pabutools.election import Instance, Project, ApprovalBallot, ApprovalProfile
"""
p1 = Project("p1", 1)   # The constructor takes the name and cost of the project
p2 = Project("p2", 1)
p3 = Project("p3", 3)



instance = Instance()   # There are many optional parameters
instance.add(p1)   # Use set methods to populate
instance.update([p2, p3])

instance.budget_limit = 3   # The instance stores the budget limit for the projects



b1 = ApprovalBallot([p1, p2])   # Initialize an approval ballot with two projects
b1.add(p2)   # Add projects to the approval ballot using set methods
b2 = ApprovalBallot({p1, p2, p3})
b3 = ApprovalBallot({p3})
profile=ApprovalProfile([b1,b2,b3])
"""
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

from random import shuffle
import pandas as pd
import matplotlib.pyplot as plt
import rules.greedy_budgeting as gb 
import metrics as mt
from pabutools.election import parse_pabulib
from pabutools.election import Cost_Sat
from pabutools.election import Instance, Project, ApprovalBallot, ApprovalProfile
from pabutools.rules import sequential_phragmen, method_of_equal_shares
from pabutools.analysis import avg_satisfaction, gini_coefficient_of_satisfaction, percent_non_empty_handed
import os
from metrics import fs_ratio, fs_abs


entries = []
for str in os.listdir('pabulib'):
	entries+= os.listdir('pabulib/'+str)
df=pd.read_excel('results/test_greedy.ods')

X=[i for i in range(len(entries))]
S=[]
df2=pd.read_excel('results/test_mes.ods')
S2=[]
S3=[]

for st in entries: #change the index of columns when you want another measure
	S.append(df[st][3])
	S2.append(df2[st][3])
	S3.append(df2[st][3]-df[st][3])
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





plt.figure(figsize=(5, 2.7), layout='constrained')
plt.plot(X,S,label='greedy',color='red')
plt.plot(X,S2,label='mes',color='blue')
plt.plot(X,S3,label='mes - greedy',color='green')
plt.xlabel('instance')
plt.ylabel('avg sat')
plt.title('avg sat')
plt.legend(loc='upper left')
plt.show()

