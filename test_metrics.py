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

df=pd.read_excel('results/test_greedy.ods')
df2=pd.read_excel('results/test_mes.ods')
st='netherlands_amsterdam_166_'
instance, profile = parse_pabulib('pabulib/netherlands_amsterdam_166_.pb')
output2 = method_of_equal_shares(instance, profile, sat_class=Cost_Sat)
s2=avg_satisfaction(instance, profile, output2, Cost_Sat)
gini2=gini_coefficient_of_satisfaction(instance, profile, output2, Cost_Sat)
CC2=percent_non_empty_handed(instance, profile, output2)
ratio2=fs_ratio(instance,profile,output2,sat_class=Cost_Sat)
diff2=fs_abs(instance,profile,output2,sat_class=Cost_Sat)
#S2.append(gini2)

l=[p for p in instance]
shuffle(l)

output = gb.greedy_budgeting(instance, profile, Cost_Sat,l)
s=avg_satisfaction(instance, profile, output, Cost_Sat)
gini1=gini_coefficient_of_satisfaction(instance, profile, output, Cost_Sat)
CC1=percent_non_empty_handed(instance,profile,output)
ratio1=fs_ratio(instance,profile,output,sat_class=Cost_Sat)
diff1=fs_abs(instance,profile,output,sat_class=Cost_Sat)
#S.append(gini1)


data=[len([b for b in profile]),len([p for p in instance]),instance.budget_limit,s,gini1,CC1,ratio1,diff1]
data2=[len([b for b in profile]),len([p for p in instance]),instance.budget_limit,s,gini2,CC2,ratio2,diff2]
df[st]=data
df2[st]=data2
df.to_excel("results/test_greedy.ods", sheet_name="test_input", index=False)
df2.to_excel("results/test_mes.ods", sheet_name="test_input", index=False)


print(ratio1)
print(diff1)
