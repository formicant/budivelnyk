from typing import Iterable, Callable, cast
from dataclasses import dataclass
from itertools import groupby


# Abstract base classes

class Node:
    """ Abstract syntax tree node. """
    pass

class Command(Node):
    """ Any leaf node. """
    pass

@dataclass
class AdditiveCommand(Command):
    """ Command with an integer argument `n`.
        Consecutive commands of the same type can be merged
        into a single command with the argument equal
        to the sum of the arguments of the original commands.
    """
    n: int


# Node types

@dataclass
class Loop(Node):
    """ While current cell's value is non-zero, repeat loop's body. """
    body: list[Node]

@dataclass
class Add(AdditiveCommand):
    """ Add constant to current cell's value. """
    pass

@dataclass
class Move(AdditiveCommand):
    """ Add constant to cell pointer. """
    pass

@dataclass
class Output(AdditiveCommand):
    """ Output current cell's value. """
    pass

@dataclass
class Input(AdditiveCommand):
    """ Store input value in current cell. """
    pass


# Optimizations

Optimization = Callable[[list[Node]], list[Node]]

def same_command_sequence_optimization(intermediate: list[Node]) -> list[Node]:
    result: list[Node] = []
    for (group_type, g) in groupby(intermediate, type):
        group = list(g)
        match group[0]:
            case AdditiveCommand(_):
                # merge consecutive additive commands
                n = sum(cast(AdditiveCommand, ac).n for ac in group)
                result.append(group_type(n))
            case Loop(body):
                # only the first of consecutive loops can be executed
                optimized_body = same_command_sequence_optimization(body)
                result.append(Loop(optimized_body))
            case _:
                result.extend(group)
    return result

default_optimizations = [same_command_sequence_optimization]


# Parsing BF code

def bf_to_intermediate(bf_code: str, optimizations: list[Optimization]|None=None) -> list[Node]:
    sequence = iter(bf_code)
    intermediate = list(_bf_sequence_to_intermediate(sequence, expect_closing_bracket=False))
    for optimization in optimizations or default_optimizations:
        intermediate = optimization(intermediate)
    return intermediate


def _bf_sequence_to_intermediate(sequence: Iterable[str], expect_closing_bracket: bool) -> Iterable[Node]:
    for char in sequence:
        match char:
            case '+': yield Add(1)
            case '-': yield Add(-1)
            case '>': yield Move(1)
            case '<': yield Move(-1)
            case '.': yield Output(1)
            case ',': yield Input(1)
            case '[':
                body = _bf_sequence_to_intermediate(sequence, expect_closing_bracket=True)
                yield Loop(list(body))
            case ']':
                if expect_closing_bracket:
                    break
                else:
                    raise RuntimeError('Unexpected closing bracket')
                    # TODO: add line number and position
    else:
        if expect_closing_bracket:
            raise RuntimeError('Closing bracket expected') 
