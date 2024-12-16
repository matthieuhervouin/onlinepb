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
entries2= []
for str in os.listdir('pabulib'):
	li= os.listdir('pabulib/'+str)
	entries2+= li
	for i in range(len(li)):
		li[i]=str+'/'+li[i]
	entries+=li
df2=pd.read_excel('results/test_mesc.ods')

for i,st in enumerate(entries):
	st2=entries2[i]
	if st2 not in df2:
		print(st)
		instance, profile = parse_pabulib('pabulib/'+st)
		output2 = method_of_equal_shares(instance, profile, sat_class=Cost_Sat,voter_budget_increment=1)
		s2=float(avg_satisfaction(instance, profile, output2, Cost_Sat))
		gini2=float(gini_coefficient_of_satisfaction(instance, profile, output2, Cost_Sat))
		CC2=float(percent_non_empty_handed(instance, profile, output2))
		ratio2=float(fs_ratio(instance,profile,output2,sat_class=Cost_Sat))
		diff2=float(fs_abs(instance,profile,output2,sat_class=Cost_Sat))
		print(ratio2)


		data2=[len([b for b in profile]),len([p for p in instance]),instance.budget_limit,s2,gini2,CC2,ratio2,diff2]
		df2[st2]=data2
		df2.to_excel("results/test_mesc.ods", sheet_name="test_input", index=False)

		
	



