"""
The Greedy Budgeting rule.
"""
from __future__ import annotations

from copy import copy, deepcopy
from collections.abc import Collection

from pabutools.utils import Numeric

from pabutools.election import AbstractApprovalProfile
from pabutools.election.satisfaction.satisfactionmeasure import GroupSatisfactionMeasure
from pabutools.election.ballot.ballot import AbstractBallot
from pabutools.election.instance import Instance, Project
from pabutools.election.profile import AbstractProfile
from pabutools.election.satisfaction import SatisfactionMeasure
from pabutools.tiebreaking import lexico_tie_breaking
from pabutools.fractions import frac
from pabutools.tiebreaking import TieBreakingRule


class MESVoter:
    """
    Class used to summarise a voter during a run of the method of equal shares.

    Parameters
    ----------
        index: Numeric
            The index of the voter in the voter list
        ballot: :py:class:`~pabutools.election.ballot.ballot.AbstractBallot`
            The ballot of the voter.
        sat: SatisfactionMeasure
            The satisfaction measure corresponding to the ballot.
        budget: Numeric
            The budget of the voter.
        multiplicity: int
            The multiplicity of the ballot.

    Attributes
    ----------
        index: int
            The index of the voter in the list of voters MES maintains
        ballot: :py:class:`~pabutools.election.ballot.ballot.AbstractBallot`
            The ballot of the voter.
        sat: SatisfactionMeasure
            The satisfaction measure corresponding to the ballot.
        budget: Numeric
            The budget of the voter.
        multiplicity: int
            The multiplicity of the ballot.
        budget_over_sat_map: dict[Numeric, Numeric]
            Maps values of the budget to values of the budget divided by the total satisfaction.
    """

    def __init__(
        self,
        index: Numeric,
        ballot: AbstractBallot,
        sat: SatisfactionMeasure,
        budget: Numeric,
        multiplicity: int,
    ):
        self.index: int = index
        self.ballot: AbstractBallot = ballot
        self.sat: SatisfactionMeasure = sat
        self.budget: Numeric = budget
        self.multiplicity: int = multiplicity
        self.budget_over_sat_map: dict[tuple[Project, Numeric], Numeric] = dict()

    def total_sat_project(self, proj: Project) -> Numeric:
        """
        Returns the total satisfaction of a given project. It is equal to the satisfaction for the project,
        multiplied by the multiplicity.

        Parameters
        ----------
            proj: :py:class:`~pabutools.election.instance.Project`
                The project.

        Returns
        -------
            Numeric
                The total satisfaction.
        """
        return self.multiplicity * self.sat.sat_project(proj)

    def total_budget(self) -> Numeric:
        """
        Returns the total budget of the voters. It is equal to the budget multiplied by the multiplicity.

        Returns
        -------
            Numeric
                The total budget.
        """
        return self.multiplicity * self.budget

    def budget_over_sat_project(self, proj):
        """
        Returns the budget divided by the satisfaction for a given project.

        Parameters
        ----------
            proj: :py:class:`~pabutools.election.instance.Project`
                The collection of projects.

        Returns
        -------
            Numeric
                The total satisfaction.
        """
        res = self.budget_over_sat_map.get((proj, self.budget), None)
        if res is None:
            res = frac(self.budget, self.sat.sat_project(proj))
            self.budget_over_sat_map[(proj, self.budget)] = res
        return res

    def __str__(self):
        return f"MESVoter[{self.budget}]"

    def __repr__(self):
        return f"MESVoter[{self.budget}]"


class MESProject(Project):
    """
    Class used to summarise the projects in a run of MES. Mostly use to store details that can be retrieved
    efficiently.
    """

    def __init__(self, project):
        Project.__init__(self, project.name, project.cost)
        self.project = project
        self.total_sat = None
        self.sat_supporter_map = dict()
        self.unique_sat_supporter = None
        self.supporter_indices = []
        self.initial_affordability = None
        self.affordability = None

    def supporters_sat(self, supporter: MESVoter):
        if self.unique_sat_supporter:
            return self.unique_sat_supporter
        return supporter.sat.sat_project(self)

    def __str__(self):
        return f"MESProject[{self.name}, {float(self.affordability)}]"

    def __repr__(self):
        return f"MESProject[{self.name}, {float(self.affordability)}]"


def affordability_poor_rich(voters: list[MESVoter], project: MESProject) -> Numeric:
    """Compute the affordability factor of a project using the "poor/rich" algorithm.

    Parameters
    ----------
        voters: list[MESVoter]
            The list of the voters, formatted for MES.
        project: MESProject
            The project under consideration.

    Returns
    -------
        Numeric
            The affordability factor of the project.

    """
    rich = set(project.supporter_indices)
    poor = set()
    while len(rich) > 0:
        poor_budget = sum(voters[i].total_budget() for i in poor)
        numerator = frac(project.cost - poor_budget)
        denominator = sum(voters[i].total_sat_project(project) for i in rich)
        affordability = frac(numerator, denominator)
        new_poor = {
            i
            for i in rich
            if voters[i].total_budget()
            < affordability * voters[i].sat.sat_project(project)
        }
        if len(new_poor) == 0:
            return affordability
        rich -= new_poor
        poor.update(new_poor)

def greedy_add(voters: list[MESVoter], project: MESProject) -> Boolean:
    """Decides whether to select a new project
    Parameters
    ----------
        voters: list[MESVoter]
            The list of the voters, formatted for MES.
        project: MESProject
            The project under consideration.

    Returns
    -------
        Numeric
            The affordability factor of the project.
    """

    if (
                sum(voters[i].total_budget() for i in project.supporter_indices)
                < project.cost
            ):
        return False
    else:
        q=affordability_poor_rich(voters,project)
        for i in project.supporter_indices:
            voters[i].budget -= min(
                voters[i].budget, q * voters[i].sat.sat_project(selected)
            )
        return True 

def greedy_budgeting(
    instance: Instance,
    profile: AbstractProfile,
    sat_class: type[SatisfactionMeasure],
    stream: list[Projects],
) -> list[Project]:
    """
    Implementation of the greedy budgeting rule.

    Parameters
    ----------
        instance: Instance
            The instance.
        profile: AbstractProfile
            The profile.
        sat_class: type[SatisfactionMeasure]
            The satisfaction measure used as a proxy of the satisfaction of the voters.
        stream: list[Projects]
            The stream of projects for the online instance

    Returns
    -------
        list[Project]
            All the projects selected by the greedy budgeting rule.
    """
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
                sat_profile.multiplicity(sat),
            )
        )
        index += 1

    projects = set()
    mes_stream=[]
    for p in stream:
        mes_p = MESProject(p)
        total_sat = 0
        for i, v in enumerate(voters):
            indiv_sat = v.sat.sat_project(p)
            if indiv_sat > 0:
                total_sat += v.total_sat_project(p)
                mes_p.supporter_indices.append(i)
                mes_p.sat_supporter_map[v] = indiv_sat
        if total_sat > 0:
            if p.cost > 0:
                mes_p.total_sat = total_sat
                afford = frac(p.cost, total_sat)
                mes_p.initial_affordability = afford
                mes_p.affordability = afford
                projects.add(mes_p)
            else:
                initial_budget_allocation.append(p)
        mes_stream.append(mes_p)

    res = []
    for project in mes_stream:
        if (
                sum(voters[i].total_budget() for i in project.supporter_indices)
                >= project.cost
            ):
            q=affordability_poor_rich(voters,project)
            for i in project.supporter_indices:
                voters[i].budget -= min(
                    voters[i].budget, q * voters[i].sat.sat_project(project)
                )   
            res.append(project.project)
    return res
        
