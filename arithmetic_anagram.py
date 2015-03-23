import inflect
import string
import sys
import click

p = inflect.engine()

ops = {
    "+": {
        "name": "plus",
        "function": lambda x, y: x + y
    },
    "*": {
        "name": "times",
        "function": lambda x, y: x * y
    }
}


def op_validation(ctx, param, value):

    if value not in ops.keys():
        raise click.BadParameter(
            "--op needs to be one of: {}".format(",".join(sorted(ops.keys()))))

    return value


@click.command()
@click.argument("n", type=int)
@click.option("--op", default="+",
              help="The operation you want to use ({}) [default: +]".format(
                  ",".join(sorted(ops.keys()))),
              callback=op_validation
              )
def main(n, op):
    """Find all pairs of n1 <operation> n2 where:

        * <operation> is one of +, -, or +

        * n1 and n2 are positive integers

        * n1 <operation> n2 == N
    """

    anagram_pairs = find_anagram_pairs(n, op, progress_bar=True)
    op_str = " {} ".format(op)

    for pairs in anagram_pairs:
        print(" = ".join([op_str.join(map(str, pair)) for pair in pairs]))


def find_anagram_pairs(n, op, progress_bar=False):
    """
    Find all distinct pairs ``(n1, n2)``, ``(m1, m2)`` of pairs of positive integers such that:

    * ``n1 <op> n2 == m1 <op> m2 == n``

    * The string representations of ``n1 <op> n2`` and ``m1 <op> m2`` are anagrams.

    :returns: Pairs of pairs of the form ``((n1, n2), (m1, m2))``
    :rtype: list of tuples
    """

    pairs = find_pairs(n, op)

    if progress_bar:

        result = []

        pairs_pairs = [(p1, p2) for p1 in pairs for p2 in pairs if p1 < p2]

        with click.progressbar(pairs_pairs) as bar:
            for p1, p2 in bar:
                if are_anagrams(p1, p2, op):
                    result.append((p1, p2))
    else:
        result = [
            (p1, p2) for p1 in pairs for p2 in pairs
            if p1 < p2 and are_anagrams(p1, p2, op)
        ]

    return result


def find_pairs(n, op):
    """
    All pairs (n1, n2) of positive integers such that n1 <op> n2 == n.

    If the operation is commutative, only pairs where n1 <= n2 are returned.
    """

    if op == "+":

        result = [(i, n - i) for i in range(1, n + 1) if i <= n - i]

    elif op == "*":

        result = [(i, int(n / i)) for i in range(2, n + 1)
                  if n % i == 0 and i <= n / i]
    else:
        raise ValueError("Unknown operation: {}".format(op))

    return result


def are_anagrams(pair1, pair2, op):
    """
    Converts each of the numbers in ``pair1`` and ``pair2`` to words (via :mod:`inflect`)
    and determines if the strings

    * ``<words for pair1[0]> <op> <words for pair1[1]>`` and

    * ``<words for pair2[0]> <op> <words for pair2[1]>``

    :param tuple pair1: A pair of positive integers
    :param tuple pair2: Another pair of positive integers
    :param op: The operation to be used
    :returns: Whether or not the string representations for the operation on ``pair1`` and the operation on ``pair2`` are anagrams.
    :rtype: bool
    """

    n1, n2 = pair1
    m1, m2 = pair2

    num_strs = [p.number_to_words(x) for x in [n1, n2, m1, m2]]

    first = "{} {} {}".format(num_strs[0], ops[op]["name"], num_strs[1])
    second = "{} {} {}".format(num_strs[2], ops[op]["name"], num_strs[3])

    return are_str_anagrams(first, second)


def are_str_anagrams(str1, str2):
    """
    Checks whether the strings ``str1`` and ``str2`` are anagrams.

    **Note:** This check is done case-insensitively, and all non-letter characters (spaces, punctuation, etc) are ignored.
    """

    if len(str1) != len(str2):
        return False

    list1 = [x.lower() for x in str1 if x in string.ascii_letters]
    list2 = [x.lower() for x in str2 if x in string.ascii_letters]
    return sorted(list1) == sorted(list2)

if __name__ == "__main__":
    main()
