from random import shuffle
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

st='netherlands_amsterdam_166_'
instance, profile = parse_pabulib('pabulib/netherlands_amsterdam_166_.pb')
output2 = method_of_equal_shares(instance, profile, sat_class=Cost_Sat,voter_budget_increment=1)
s2=float(avg_satisfaction(instance, profile, output2, Cost_Sat))
gini2=float(gini_coefficient_of_satisfaction(instance, profile, output2, Cost_Sat))
CC2=float(percent_non_empty_handed(instance, profile, output2))
ratio2=float(fs_ratio(instance,profile,output2,sat_class=Cost_Sat))
diff2=float(fs_abs(instance,profile,output2,sat_class=Cost_Sat))
#S2.append(gini2)

l=[p for p in instance]
shuffle(l)

output = gb.greedy_budgeting(instance, profile, Cost_Sat,l)
s=float(avg_satisfaction(instance, profile, output, Cost_Sat))
gini1=float(gini_coefficient_of_satisfaction(instance, profile, output, Cost_Sat))
CC1=float(percent_non_empty_handed(instance,profile,output))
ratio1=float(fs_ratio(instance,profile,output,sat_class=Cost_Sat))
diff1=float(fs_abs(instance,profile,output,sat_class=Cost_Sat))
#S.append(gini1)


print("avg_sat: ",s2,"\n",s,"\n")
print("gini index: ",gini2,"\n",gini1,"\n")
print("ratio: ",ratio2,"\n",ratio1,"\n")
print("dist fs: ",diff2,"\n",diff1,"\n")



