"""
    File name: Factor.py
    Author: Sandip Katel, Sharad Pokharel

    This script contains the Factor class with necessary utility functions
    for doing inference using variable elimination or enumeration.
"""

from enum import IntEnum
import numpy as np
from typing import List


class Sign(IntEnum):
    POSITIVE = 5
    NEGATIVE = -5
    UNDEFINED = -10


class Factor:
    """
    Representation of a factor for inference
    Attributes
        solution_variables  Non-evidence variables that are on the solution side
        given_variables     Non-evidence variables that are on the given side
        variables           All of the variables that this factor
        table               2D numpy array, representing the factor's
                                probability table
        solution_evidence   Evidence variables that are on the solution side
                                (only used for printing the representation)
        given_evidence      Evidence variables that are on the given side
                                (only used for printing the representation)
        is_probability      Indicates if the factor is a probability table as well
    """
    def __init__(self, solution_variables: List[str],
                 given_variables: List[str], values: List[float],
                 solution_evidence=None, given_evidence=None, is_probability=True) -> None:
        """
        Constructor of a Factor

        :param solution_variables: Non-evidence variables that are on the solution side
        :param given_variables: Non-evidence variables that are on the given side
        :param values: probability values of the table
        :param solution_evidence: Evidence variables that are on the solution side
                                (only used for printing the representation)
        :param given_evidence: Evidence variables that are on the given side
                                (only used for printing the representation)
        :param is_probability: Indicates if the factor is a probability table as well 
        """
        self.solution_variables = solution_variables
        self.given_variables = given_variables
        self.variables = given_variables + solution_variables

        # generating the table using the variables and the values
        self.table = self.generate_table(self.variables, values)

        # default value must be set to None for solution_evidence 
        # and given_evidence so that each Factor object can create
        # its own copy of them. If default value is set to empty
        # list, multiple objects refer to the same empty list object
        # which causes issues 
        if solution_evidence is None:
            self.solution_evidence = []
        else:
            self.solution_evidence = solution_evidence
        if given_evidence is None:
            self.given_evidence = []
        else:
            self.given_evidence = given_evidence
        
        # If the factor is also a probability table.
        self.is_probability = is_probability

    @staticmethod
    def generate_table_skeleton(variables: List[str]) -> np.ndarray:
        """
        Generate a probability table with all the possible combinations
        of the input variables without any probability values

        :param variables: variables to generate the skeleton table for
        :return: Mutidimensional numpy array representing the factor table
                with the values (i.e. last column) unassigned
        """
        num_variables = len(variables)
        num_rows = 2**num_variables  # assuming the domain length is 2 for all vars
        num_cols = num_variables + 1  # one col per var + last col for probability values 
        table = np.zeros([num_rows, num_cols])
        table.fill(Sign.UNDEFINED)     # initializing everything with undefined
        for i in range(len(variables)):
            # combination_len is the length of same value for generating the
            # combinations with other variables. E.g., for a table with 3 variables,
            # The first column will be ++++---- (combination_len is 4 for this one)
            # The second column will be ++--++-- (combination_len is 2 for this one)
            # The last variable's column will be +-+-+-+- (combination_len is 1 here)
            combination_len = 2**(num_variables - i)//2
            for j in range(0, num_rows, combination_len*2):
                table[j:combination_len+j, [i]] = Sign.POSITIVE
                table[combination_len+j:2*combination_len+j, [i]] = Sign.NEGATIVE
        return table
        
    def generate_table(self, variables: List[str], values: List[float]) -> np.ndarray:
        """
        Generate a probability table with all the possible combinations
        of the input variables and the given probability values. Values
        must be in correct order for this to work correctly.

        :param variables: variables for the table
        :param values: probability values of each row in correct order
        :return: Mutidimensional numpy array representing the factor table
        """
        table = self.generate_table_skeleton(variables)
        table[:, -1] = values   # last column is the probability values
        return table

    def print_representation(self) -> None:
        """
        Print out the representation of a factor
        ex P(+x,y|-t,a)
        """
        if self.is_probability:
            print('P(', end='')
        else:
            print('f(', end='')
        Factor.print_representation_helper(self.solution_evidence, self.solution_variables)
        if len(self.given_variables) > 0 or len(self.given_evidence) > 0:
            print('|', end='')
        Factor.print_representation_helper(self.given_evidence, self.given_variables)
        print(')')

    @staticmethod
    def print_representation_helper(evidence_vars: List[str], variables: List[str]) -> None:
        """
        Print out the variables portion of a factor representation

        :param evidence_vars: Evidence vars to print
        :param variables: Non-evidence vars to print
        """
        for i, entry in enumerate(evidence_vars):
            var, value = entry
            if value == Sign.POSITIVE:
                print('+{0}'.format(var.lower()), end='')
            else:
                print('-{0}'.format(var.lower()), end='')
            if i != len(evidence_vars) - 1 or len(variables) > 0:
                print(',', end='')
        for i, var in enumerate(variables):
            print(var, end='')
            if i != len(variables) - 1:
                print(',', end='')

    def print_factor(self) -> None:
        """
        Print the factor

        """
        for row in self.table:
            for i, cell in enumerate(row):
                if cell == Sign.POSITIVE:
                    print('{:^10s}'.format("+" + self.variables[i].lower()), end='|')
                elif cell == Sign.NEGATIVE:
                    print('{:^10s}'.format("-" + self.variables[i].lower()), end='|')
                else:
                    cell_value = "{:^.5f}".format(cell)
                    print('{:^10s}'.format(cell_value), end='|\n')
        print()

    def remove_var(self, variable: str) -> None:
        """
        Remove a variable from variables, given_variables, and
        solution_variables after it's observed or summed out

        :param variable: The variable to remove
        """
        self.variables.remove(variable)
        self.safe_remove_list(self.given_variables, variable)
        self.safe_remove_list(self.solution_variables, variable)

    @staticmethod
    def safe_remove_list(input_list: list, value) -> None:
        """
        Deletes an entry from a list without throwing the ValueError exception
        in case the entry is not in the set

        :param input_list: set from which the entry has to be removed
        :param value: the set entry to be removed
        """
        try:
            input_list.remove(value)
        except ValueError:
            pass

    def observe_var(self, variable: str, value: Sign) -> None:
        """
        Restricts a variable to some value in the factor

        :param variable: Variable to restrict
        :param value: value for restriction
        """
        if variable not in self.variables:
            return
        index = self.variables.index(variable)
        self.table = self.table[self.table[:, index] == value]
        index = self.variables.index(variable)
        self.table = np.delete(self.table, index, axis=1)
        if variable in self.solution_variables:
            self.solution_evidence.append((variable.lower(), value))
        if variable in self.given_variables:
            self.given_evidence.append((variable.lower(), value))
        self.remove_var(variable)

    def normalize(self) -> None:
        """
        Normalizes the factor so that all rows add up to 1

        """
        sum_of_vals = sum(self.table[:, -1])
        self.table[:, -1] /= sum_of_vals
    
    def sumout(self, variable: str) -> None:
        """
        Sums out a variable in the factor

        :param variable: variable to sumout
        """
        if variable not in self.variables:
            return
        index = self.variables.index(variable) # getting the index of the variable
        self.table = np.delete(self.table, index, axis=1)
        self.remove_var(variable)
        # new table for summed out rows
        summed_out = self.generate_table_skeleton(self.variables)
        summed_out[:, -1] = 0
        for row1 in summed_out:
            for row2 in self.table:
                # if two rows are the same after removing a variable,
                # their values are added
                if np.array_equal(row1[:-1], row2[:-1]):
                    row1[-1] = row1[-1] + row2[-1]
        self.table = summed_out

    @staticmethod
    def multiply(factor1, factor2):
        """
        Multiply two factors together and return a new product factor

        :param factor1: The first factor to multiply
        :param factor2: The second factor to multiply
        :return: A new factor that's the product of factor1 and factor2
        """
        # factor1 cannot have any solution variables that factor2 has as given variables
        # since we assume that only the reverse is true later in the function
        if not any((True for x in factor1.solution_variables if x in factor2.given_variables)):
            temp = factor2
            factor2 = factor1
            factor1 = temp

        # list(dict.fromkeys( ... )) is used to remove duplicates while maintaining order
        new_solution_vars = list(dict.fromkeys(factor1.solution_variables
                                               + factor2.solution_variables))

        new_given_vars = list(dict.fromkeys(factor1.given_variables
            + [item for item in factor2.given_variables if item not in new_solution_vars]))

        # generate the probabilities for our new factor
        # (no sorting is required since the variable ordering consistent between
        #  the two original factors)
        new_prob_list = []
        for row1 in factor1.table:
            for row2 in factor2.table:
                if Factor.is_valid_row_multiply(factor1.variables,
                                                factor2.variables,
                                                row1, row2):
                    new_prob_list.append(row1[-1] * row2[-1])

        return Factor(new_solution_vars, new_given_vars, new_prob_list,
                      list(set(factor1.solution_evidence + factor2.solution_evidence)),
                      list(set(factor1.given_evidence + factor2.given_evidence)),
                      False)

    @staticmethod
    def is_valid_row_multiply(variables1: list, variables2: list, row1: list, row2: list) -> bool:
        """
        Two rows are valid if there are no contradictions between them
        Ex if two rows have +x and -x respectively then they're not valid

        :param variables1: Variables of factor 1
        :param variables2: Variables of factor 2
        :param row1: Row from factor 1
        :param row2: Row from factor 2
        :return: True if two rows are valid to multiply, False otherwise
        """
        for i, var1 in enumerate(variables1):
            for j, var2 in enumerate(variables2):
                if var1 == var2 and row1[i] != row2[j]:
                    return False
        return True
