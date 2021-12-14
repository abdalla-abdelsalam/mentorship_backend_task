# first problem find min different
# -----------------------------------------------------------
# the naive approcuh : try all the possbilites
# Big O(n^2)
def find_min_different_navie_approach():
    n = int(input())
    lst = []
    for i in range(0, n):
        element = int(input())
        lst.append(element)

    diff = 20**20
    for i in range(0, n-1):
        for j in range(i+1, n):
            diff = min(diff, abs(lst[i]-lst[j]))

    return diff


# Big o(nlog(n))
# Sort array in ascending order and set difference variable to infinite 
# then copmarey all adjacent paris in the arry and keep track of the minimum difference
def find_min_different_optimal_approach():
    n = int(input())
    lst = []
    diff = 20**20
    for i in range(0, n):
        element = int(input())
        lst.append(element)

    lst = sorted(lst)

    for i in range(0, n-1):
        diff = min(diff, lst[i+1]-lst[i])
    return diff


# ---------------------------------------------------------------------
# second problem common substring problem
# naive approuch compare each character of string 1 with each character or string 2
# Big o(n^2)
def two_string_navie_approuch():
    s1 = input()
    s2 = input()
    for i in range(0, len(s1)):
        for j in range(0, len(s2)):
            if(s1[i] == s2[j]):
                return True
    return False

# more optimal
# check if there is a common character between the two strings
# Big o(n)
def two_string_optimal_approuch():
    s1 = input()
    s2 = input()
    Dict = {}
    for i in s1:
        Dict[i] = True

    for i in s2:
        if i in Dict:
            return True
    return False
