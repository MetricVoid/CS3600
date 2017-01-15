from collections import deque

"""
    Base class for unary constraints
    Implement isSatisfied in subclass to use
"""


class UnaryConstraint:
    def __init__(self, var):
        self.var = var

    def isSatisfied(self, value):
        util.raiseNotDefined()

    def affects(self, var):
        return var == self.var


"""
    Implementation of UnaryConstraint
    Satisfied if value does not match passed in paramater
"""


class BadValueConstraint(UnaryConstraint):
    def __init__(self, var, badValue):
        self.var = var
        self.badValue = badValue

    def isSatisfied(self, value):
        return not value == self.badValue

    def __repr__(self):
        return 'BadValueConstraint (%s) {badValue: %s}' % (str(self.var), str(self.badValue))


"""
    Implementation of UnaryConstraint
    Satisfied if value matches passed in paramater
"""


class GoodValueConstraint(UnaryConstraint):
    def __init__(self, var, goodValue):
        self.var = var
        self.goodValue = goodValue

    def isSatisfied(self, value):
        return value == self.goodValue

    def __repr__(self):
        return 'GoodValueConstraint (%s) {goodValue: %s}' % (str(self.var), str(self.goodValue))


"""
    Base class for binary constraints
    Implement isSatisfied in subclass to use
"""


class BinaryConstraint:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def isSatisfied(self, value1, value2):
        util.raiseNotDefined()

    def affects(self, var):
        return var == self.var1 or var == self.var2

    def otherVariable(self, var):
        if var == self.var1:
            return self.var2
        return self.var1


"""
    Implementation of BinaryConstraint
    Satisfied if both values assigned are different
"""


class NotEqualConstraint(BinaryConstraint):
    def isSatisfied(self, value1, value2):
        if value1 == value2:
            return False
        return True

    def __repr__(self):
        return 'NotEqualConstraint (%s, %s)' % (str(self.var1), str(self.var2))


class ConstraintSatisfactionProblem:
    """
    Structure of a constraint satisfaction problem.
    Variables and domains should be lists of equal length that have the same order.
    varDomains is a dictionary mapping variables to possible domains.

    Args:
        variables (list<string>): a list of variable names
        domains (list<set<value>>): a list of sets of domains for each variable
        binaryConstraints (list<BinaryConstraint>): a list of binary constraints to satisfy
        unaryConstraints (list<BinaryConstraint>): a list of unary constraints to satisfy
    """

    def __init__(self, variables, domains, binaryConstraints=[], unaryConstraints=[]):
        self.varDomains = {}
        for i in xrange(len(variables)):
            self.varDomains[variables[i]] = domains[i]
        self.binaryConstraints = binaryConstraints
        self.unaryConstraints = unaryConstraints

    def __repr__(self):
        return '---Variable Domains\n%s---Binary Constraints\n%s---Unary Constraints\n%s' % (
            ''.join([str(e) + ':' + str(self.varDomains[e]) +
                    '\n' for e in self.varDomains]),
            ''.join([str(e) + '\n' for e in self.binaryConstraints]),
            ''.join([str(e) + '\n' for e in self.binaryConstraints]))


class Assignment:
    """
    Representation of a partial assignment.
    Has the same varDomains dictionary stucture as ConstraintSatisfactionProblem.
    Keeps a second dictionary from variables to assigned values, with None being no assignment.

    Args:
        csp (ConstraintSatisfactionProblem): the problem definition for this assignment
    """

    def __init__(self, csp):
        self.varDomains = {}
        for var in csp.varDomains:
            self.varDomains[var] = set(csp.varDomains[var])
        self.assignedValues = {var: None for var in self.varDomains}

    """
    Determines whether this variable has been assigned.

    Args:
        var (string): the variable to be checked if assigned
    Returns:
        boolean
        True if var is assigned, False otherwise
    """

    def isAssigned(self, var):
        return self.assignedValues[var] != None

    """
    Determines whether this problem has all variables assigned.

    Returns:
        boolean
        True if assignment is complete, False otherwise
    """

    def isComplete(self):
        for var in self.assignedValues:
            if not self.isAssigned(var):
                return False
        return True

    """
    Gets the solution in the form of a dictionary.

    Returns:
        dictionary<string, value>
        A map from variables to their assigned values. None if not complete.
    """

    def extractSolution(self):
        if not self.isComplete():
            return None
        return self.assignedValues

    def __repr__(self):
        return '---Variable Domains\n%s---Assigned Values\n%s' % (
            ''.join([str(e) + ':' + str(self.varDomains[e]) +
                    '\n' for e in self.varDomains]),
            ''.join([str(e) + ':' + str(self.assignedValues[e]) + '\n' for e in self.assignedValues]))


##########################################################################


"""
    Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
    Do not assign value to var. Only check if this value would be consistent or not.
    If the other variable for a constraint is not assigned, then the new value is consistent with the constraint.

    Args:
        assignment (Assignment): the partial assignment
        csp (ConstraintSatisfactionProblem): the problem definition
        var (string): the variable that would be assigned
        value (value): the value that would be assigned to the variable
    Returns:
        boolean
        True if the value would be consistent with all currently assigned values, False otherwise
"""


def consistent(assignment, csp, var, value):
    """Question 1"""
    """YOUR CODE HERE"""

    """
    tests whether a given value would be possible to assign to a variable without violating any of its
    constraints.
    """
    # test unary constraints

    for unary_constraint in csp.unaryConstraints:
        if unary_constraint.affects(var):
            if not unary_constraint.isSatisfied(value):
                return False

    # test binary constraints
    # NotEqualContraint: value dari a gk bole sama value dari b
    
    for binary_constraint in csp.binaryConstraints:
        # kalo 2 2 nya none, ngapaen di test?
        if binary_constraint.affects(var):
            if assignment.isAssigned(binary_constraint.otherVariable(var)):
                if not binary_constraint.isSatisfied(value, assignment.assignedValues[binary_constraint.otherVariable(var)]):
                    return False

    return True


"""
    Recursive backtracking algorithm.
    A new assignment should not be created. The assignment passed in should have its domains updated with inferences.
    In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
    the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.

    Examples of the functions to be passed in:
    orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
    selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
        orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
        selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
    Returns:
        Assignment
        A completed and consistent assignment. None if no solution exists.
"""


def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod):
    """Question 1"""
    """YOUR CODE HERE"""
    # base case: if the assignment is complete
    if assignment.isComplete():
        return assignment
    var = selectVariableMethod(assignment, csp)
    
    for value in orderValuesMethod(assignment, csp, var):
        if consistent(assignment, csp, var, value):
            assignment.assignedValues[var] = value
            result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
            # failure if assignment is None
            if result is not None:
                return assignment
            assignment.assignedValues[var] = None

    # Indicates failure, failure here is None
    return None



"""
    Uses unary constraints to eleminate values from an assignment.

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
    Returns:
        Assignment
        An assignment with domains restricted by unary constraints. None if no solution exists.
"""
def eliminateUnaryConstraints(assignment, csp):
    domains = assignment.varDomains
    for var in domains:
        for constraint in (c for c in csp.unaryConstraints if c.affects(var)):
            for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)):
                domains[var].remove(value)
                if len(domains[var]) == 0:
                    # Failure due to invalid assignment
                    return None
    return assignment


"""
    Trivial method for choosing the next variable to assign.
    Uses no heuristics.
"""
def chooseFirstVariable(assignment, csp):
    for var in csp.varDomains:
        # if variable is not assigned
        if not assignment.isAssigned(var):
            return var


"""
    Selects the next variable to try to give a value to in an assignment.
    Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        the next variable to assign
"""
def minimumRemainingValuesHeuristic(assignment, csp):
    nextVar = None
    domains = assignment.varDomains
    """Question 2"""
    """YOUR CODE HERE"""
    if assignment.isComplete():
        return None

    # remove already assigned variables from the domains
    # dictionaries are mutable, have to deep copy
    domainss = domains.copy()
    for var, values in domains.iteritems():
        if assignment.isAssigned(var):
            del domainss[var]

    # Use MRV, if there is a tie, find degree heuristic
    num_of_domains = []
    for domain in domainss:
        num_of_domains.append(len(domainss[domain]))
    
    # Check if there is any tie
    there_is_a_tie = False
    min_num = min(num_of_domains)
    min_occurence = num_of_domains.count(min_num)
    if min_occurence > 1:
        there_is_a_tie = True

    if not there_is_a_tie:
        nextVar = [key for key, value in domainss.iteritems() if len(value) == min_num]
        nextVar = nextVar[0]
    else:
        # Use degree heuristic to break the tie
        # set up a dictionary that will count number of occurence in the binary constraints
        count_dict = {}
        for key, value in domainss.iteritems():
            count_dict[key] = 0
        # now count the occurence in the binary constraint
        for constraint in csp.binaryConstraints:
            if count_dict.has_key(constraint.var1):
                count_dict[constraint.var1] += 1
            if count_dict.has_key(constraint.var2):
                count_dict[constraint.var2] += 1
        max_num = -1
        for key, value in count_dict.iteritems():
            if value > max_num:
                max_num = value
        nextVar = [key for key, value in count_dict.iteritems() if value == max_num]
        nextVar = nextVar[0]

    return nextVar


"""
    Trivial method for ordering values to assign.
    Uses no heuristics.
"""
def orderValues(assignment, csp, var):
    return list(assignment.varDomains[var])

"""
    Helper function for Question 3
"""
def count_constrained_values(assignment, csp, var, value, neighbours):
    constrained_moves = 0
    for neighbour in neighbours:
        domains = assignment.varDomains[neighbour]
        if value in domains:
            constrained_moves += 1

    return constrained_moves


"""
    Creates an ordered list of the remaining values left for a given variable.
    Values should be attempted in the order returned.
    The least constraining value should be at the front of the list.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable to be assigned the values
    Returns:
        list<values>
        a list of the possible values ordered by the least constraining value heuristic
"""
def leastConstrainingValuesHeuristic(assignment, csp, var):
    values = list(assignment.varDomains[var])
    # """Hint: Creating a helper function to count the number of constrained values might be useful"""
    # """Question 3"""
    # """YOUR CODE HERE"""
    
    # Find the variables in which the var are constrained with
    binary_constraints = csp.binaryConstraints
    constrained_variables = []
    for constraint in binary_constraints:
        if constraint.affects(var):
            constrained_variables.append(constraint.otherVariable(var))

    values_dict = {}
    for val in values:
        values_dict[val] = count_constrained_values(assignment, csp, var, val, constrained_variables)

    # Sort the list of values based on the data, from smallest to highest
    import operator
    sorted_dict = sorted(values_dict.items(), key=operator.itemgetter(1), reverse=False)
    values = [key for key, value in sorted_dict]
    return values

"""
    Trivial method for making no inferences.
"""
def noInferences(assignment, csp, var, value):
    return set([])


"""
    Implements the forward checking algorithm.
    Each inference should take the form of (variable, value) where the value is being removed from the
    domain of variable. This format is important so that the inferences can be reversed if they
    result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
    inferences made should be reversed before ending the fuction.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set<tuple<variable, value>>
        the inferences made in this call or None if inconsistent assignment
"""
def forwardChecking(assignment, csp, var, value):
    inferences = set([])
    domains = assignment.varDomains
    """Question 4"""
    """YOUR CODE HERE"""
    # Look at each unassigned variable that is connected to X
    concerned_variables = []
    binary_constraints = csp.binaryConstraints
    
    for constraint in binary_constraints:
        if constraint.affects(var):
            other = constraint.otherVariable(var)
            if not assignment.isAssigned(other):
                concerned_variables.append(other)

    # delete from concerned_variables' domain ANY value that is inconsistent with the value chosen for 'var'
    this_is_invalid_inference = False
    for concerned_variable in concerned_variables:
        domains = list(assignment.varDomains[concerned_variable])
        for domain in domains:
            if not consistent(assignment, csp, concerned_variable, domain):
                inferences.add((concerned_variable, domain))
                assignment.varDomains[concerned_variable].remove(domain)
                if len(assignment.varDomains[concerned_variable]) == 0:
                    this_is_invalid_inference = True

    # restore all changes made
    if this_is_invalid_inference:
        restoring_things = list(inferences)
        for thing in restoring_things:
            assignment.varDomains[thing[0]].add(thing[1])
        return None

    return inferences

"""
    Recursive backtracking algorithm.
    A new assignment should not be created. The assignment passed in should have its domains updated with inferences.

    In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
    the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.


    Examples of the functions to be passed in:
    orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
    selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
    inferenceMethod: noInferences, maintainArcConsistency, forwardChecking


    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
        orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
        selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
        inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>): a function to specify what type of inferences to use
                Can be forwardChecking or maintainArcConsistency
    Returns:
        Assignment

        A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod):
    """Question 4"""
    """YOUR CODE HERE"""
    # base case: if the assignment is complete
    if assignment.isComplete():
        return assignment
    var = selectVariableMethod(assignment, csp)
    
    for value in orderValuesMethod(assignment, csp, var):
        if consistent(assignment, csp, var, value):
            assignment.assignedValues[var] = value
            inferences = inferenceMethod(assignment, csp, var, value)
            result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
            # failure if assignment is None
            if result is not None:
                return assignment
            # if no solution found, have to restore all the things
            assignment.assignedValues[var] = None
            if inferences is not None:
                for inference in inferences:
                    assignment.varDomains[inference[0]].add(inference[1])
    # Indicates failure, failure here is None
    return None

"""
    Helper funciton to maintainArcConsistency and AC3.
    Remove values from var2 domain if constraint cannot be satisfied.
    Each inference should take the form of (variable, value) where the value is being removed from the
    domain of variable. This format is important so that the inferences can be reversed if they
    result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
    inferences made should be reversed before ending the fuction.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var1 (string): the variable with consistent values
        var2 (string): the variable that should have inconsistent values removed
        constraint (BinaryConstraint): the constraint connecting var1 and var2
    Returns:
        set<tuple<variable, value>>
        the inferences made in this call or None if inconsistent assignment
"""
def revise(assignment, csp, var1, var2, constraint):
    inferences = set([])
    """Question 5"""
    """YOUR CODE HERE"""

    """
    for each value 2,
    if no value1 in domain_of_var_1 allows (val1 ,val2) to satisfy the constraint between var1 and var2
    then delete value2 from domain_of_var_2; removed  true
    ---> from the book
    """
    domains_of_var2 = assignment.varDomains[var2]
    domains_of_var1 = assignment.varDomains[var1]
    
    for value2 in domains_of_var2:
        satisfied = False
        for value1 in domains_of_var1:
            if constraint.isSatisfied(value1, value2):
                satisfied = True
        # Kalo gak ad value di value1 yg bsa satisfy value2, include value2 ke inference
        if not satisfied:
            inferences.add((var2,value2))
 
    # housekeeping
    if len(inferences) == len(assignment.varDomains[var2]):
        return None
    else:
        for inference in inferences:
            assignment.varDomains[var2].remove(inference[1])

    return inferences

"""
    Implements the maintaining arc consistency algorithm.
    Inferences take the form of (variable, value) where the value is being removed from the
    domain of variable. This format is important so that the inferences can be reversed if they
    result in a conflicting partial assignment. If the algorithm reveals an inconsistency, and
    inferences made should be reversed before ending the fuction.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set<<variable, value>>
        the inferences made in this call or None if inconsistent assignment
"""
def maintainArcConsistency(assignment, csp, var, value):
    inferences = set([])
    
    # """Hint: implement revise first and use it as a helper function"""
    # """Question 5"""
    # """YOUR CODE HERE"""
    # # Important: an arc is basically a bin constraint

    consistent_var_index = 0
    check_var_index = 1
    constraint_index = 2

    queue_of_arcs = []
    binary_constraints = csp.binaryConstraints
    for constraint in binary_constraints:
        if constraint.affects(var):
            queue_of_arcs.append((var, constraint.otherVariable(var),constraint))

    while len(queue_of_arcs) > 0:
        curr_arc = queue_of_arcs.pop(0)
        revision = revise(assignment, csp, curr_arc[consistent_var_index], curr_arc[check_var_index], curr_arc[constraint_index])

        # remember that None is not equal to empty set here!!!
        if revision == None:
            restoring_things = list(inferences)
            for thing in restoring_things:
                assignment.varDomains[thing[0]].add(thing[1])
            return None

        # If it returns an empty set, meaning that the arcs are alr consistent, no need to add another thing here.
        # if there is any 'useless value', add new stuff to the queue, if no change, then 2 arcs are already consistent
        if len(revision) != 0:
            for bc in csp.binaryConstraints:
                if bc.affects(curr_arc[check_var_index]):
                    queue_of_arcs.append((curr_arc[check_var_index], bc.otherVariable(curr_arc[check_var_index]), bc))

        inferences = inferences.union(revision)
    return inferences

"""
    AC3 algorithm for constraint propogation. Used as a preprocessing step to reduce the problem
    before running recursive backtracking.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        Assignment
        the updated assignment after inferences are made or None if an inconsistent assignment
"""
def AC3(assignment, csp):
    inferences = set([])
    """Hint: implement revise first and use it as a helper function"""
    """Question 6"""
    """YOUR CODE HERE"""

    consistent_var_index = 0
    check_var_index = 1
    constraint_index = 2

    queue_of_arcs = []
    binary_constraints = csp.binaryConstraints
    for constraint in binary_constraints:
        # the only difference with MAC is this thing~
        queue_of_arcs.append((constraint.var1, constraint.otherVariable(constraint.var1), constraint))
        queue_of_arcs.append((constraint.var2, constraint.otherVariable(constraint.var2), constraint))

    while len(queue_of_arcs) > 0:
        curr_arc = queue_of_arcs.pop(0)
        revision = revise(assignment, csp, curr_arc[consistent_var_index], curr_arc[check_var_index], curr_arc[constraint_index])
        
        # invalid!!
        if revision == None:
            restoring_things = list(inferences)
            for thing in restoring_things:
                assignment.varDomains[thing[0]].add(thing[1])
            return None

        # if there is any 'useless value', add new stuff to the queue, if no change, then 2 arcs are already consistent
        if len(revision) != 0:
            for bc in csp.binaryConstraints:
                if bc.affects(curr_arc[check_var_index]):
                    queue_of_arcs.append((curr_arc[check_var_index], bc.otherVariable(curr_arc[check_var_index]), bc))

        # inferences = inferences.union(revision)

    return assignment

"""
    Solves a binary constraint satisfaction problem.

    Args:
        csp (ConstraintSatisfactionProblem): a CSP to be solved
        orderValuesMethod (function): a function to decide the next value to try
        selectVariableMethod (function): a function to decide which variable to assign next
        inferenceMethod (function): a function to specify what type of inferences to use
        useAC3 (boolean): specifies whether to use the AC3 preprocessing step or not
    Returns:
        dictionary<string, value>
        A map from variables to their assigned values. None if no solution exists.
"""
def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic, selectVariableMethod=minimumRemainingValuesHeuristic, inferenceMethod=None, useAC3=True):
    assignment = Assignment(csp)

    assignment = eliminateUnaryConstraints(assignment, csp)
    if assignment == None:
        return assignment

    if useAC3:
        assignment = AC3(assignment, csp)
        if assignment == None:
            return assignment
    if inferenceMethod is None or inferenceMethod==noInferences:
        assignment = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
    else:
        assignment = recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
    if assignment == None:
        return assignment

    return assignment.extractSolution()
