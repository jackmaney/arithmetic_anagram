import inflect
import string
import sys

p = inflect.engine()


def main():
    if not sys.argv[1:]:
        print("Usage: python sum_palindrome.py <max_int_to_search>")

    max_int = int(sys.argv[1])

    if max_int < 0:
        raise ValueError

    anagram_sum_pairs = find_anagram_sum_pairs(max_int)

    for pairs in sorted(anagram_sum_pairs):
        print(" = ".join([" + ".join(map(str, pair)) for pair in pairs]))


def find_anagram_sum_pairs(max_int):

    result = []

    for sum_total in range(2, max_int + 1):
        pairs = find_pairs(sum_total)
        result.extend([
            (p1, p2) for p1 in pairs for p2 in pairs
            if p1 < p2 and sum_are_anagrams(p1, p2)
        ])

    return result


def find_pairs(n):
    """
    All pairs (n1, n2) of positive integers such that n1 + n2 == n (and n1 <= n2)
    """

    return [(i, n - i) for i in range(1, n + 1) if i <= n - i]


def are_anagrams(str1, str2):

    if len(str1) != len(str2):
        return False

    list1 = [x.lower() for x in str1 if x in string.ascii_letters]
    list2 = [x.lower() for x in str2 if x in string.ascii_letters]
    return sorted(list1) == sorted(list2)


def sum_are_anagrams(p1, p2):
    """
    p1, p2: pairs of positive integers
    runs p.number_to_words on each of n1, n2, m1, and m2
    and sees if the strings
        "<words for n1> plus <words for n2>"
    and
        "<words for m1> plus <words for m2>"
    are anagrams
    """

    n1, n2 = p1
    m1, m2 = p2

    num_strs = [p.number_to_words(x) for x in [n1, n2, m1, m2]]

    first = "{} plus {}".format(num_strs[0], num_strs[1])
    second = "{} plus {}".format(num_strs[2], num_strs[3])

    return are_anagrams(first, second)

if __name__ == "__main__":
    main()
