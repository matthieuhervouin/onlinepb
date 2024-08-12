import os
import pandas as pd

df=pd.read_excel('results/test_mes.ods')
df2=pd.read_excel('results/test_greedy.ods')

entries = []
for str in os.listdir('pabulib'):
	entries+= os.listdir('pabulib/'+str)
print(len(entries))

for str in df:
	if str not in entries:
		if 'lodz/' not in str:
			print(str)

print('other')
for str in entries:
	if str not in df:
		if 'lodz/'+str not in entries:
			print(str)


