from pabutools.election import Instance, Project, ApprovalBallot, ApprovalProfile
from pabutools.election import parse_pabulib
from pabutools.election import Cost_Sat
from pabutools.election.profile import AbstractProfile
from pabutools.election.satisfaction import SatisfactionMeasure
from rules.greedy_budgeting import MESVoter


def fair_share(
	instance: Instance,
	profile: AbstractProfile,
	voter: MESVoter
	):

	s=0
	for project in voter.ballot:
		s+=project.cost/profile.approval_score(project)
	return min(voter.budget,s)

def share(
	instance: Instance,
	profile: AbstractProfile,
	output: list[Project],
	voter: MESVoter
	):
	s=0
	for project in output:
		if project in voter.ballot:
			s+=project.cost/profile.approval_score(project)
	return s



def fs_ratio(
    instance: Instance,
	profile: AbstractProfile,
	output: list[Project],
	sat_class: type[SatisfactionMeasure]
	):

    nb_voters= len([b for b in profile])
    initial_budget_per_voter= instance.budget_limit / nb_voters
    voters = []
    sat_profile = profile.as_sat_profile(sat_class)
    for index, sat in enumerate(sat_profile):
        voters.append(
            MESVoter(
                index,
                sat.ballot,
                sat,
                initial_budget_per_voter,
                sat_profile.multiplicity(sat)
            )
        )
        index += 1

    s=0
    for voter in voters:
        v_share=0
        for project in output:
    	    if project in voter.ballot:
    		    v_share+=project.cost/profile.approval_score(project)
        fs=0
        for project in voter.ballot:
    	    fs+=project.cost/profile.approval_score(project)
        if fs>1:
            m=float(v_share / fs)
            s+=min(1,m)
    if s>nb_voters:
    	print('wtf fréro ?')
    return float(s / nb_voters)

def fs_abs(
    instance: Instance,
    profile: AbstractProfile,
    output: list[Project],
    sat_class: type[SatisfactionMeasure]
    ):

    nb_voters= len([b for b in profile])
    initial_budget_per_voter= instance.budget_limit / nb_voters
    voters = []
    sat_profile = profile.as_sat_profile(sat_class)
    for index, sat in enumerate(sat_profile):
        voters.append(
            MESVoter(
                index,
                sat.ballot,
                sat,
                initial_budget_per_voter,
                sat_profile.multiplicity(sat)
            )
        )
        index += 1
    s=0
    for voter in voters:
        v_share=0
        for project in output:
            if project in voter.ballot:
        	    v_share+=project.cost/profile.approval_score(project)
        fs=0
        for project in voter.ballot:
            fs+=project.cost/profile.approval_score(project)
        a=abs(v_share - fs)
        s+=a
    return float(s / nb_voters)

   






