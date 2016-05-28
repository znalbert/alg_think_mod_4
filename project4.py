"""
Algorithmic Thinking Project 4
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """ set, int, int, int -> dict of dict
    Takes a set of characters for the alphabet and three scores.  Returns a
    dictionary of dictionaries whose entries are indexed pairs of characters
    alphabet plus '-'.
    """

    letters = list(alphabet)
    letters.append('-')

    scoring_matrix = {}

    for letter_x in letters:
        scores = {}
        for letter_y in letters:
            if '-' in letter_x + letter_y:
                scores[letter_y] = dash_score
            elif letter_x == letter_y:
                scores[letter_y] = diag_score
            else:
                scores[letter_y] = off_diag_score
        scoring_matrix[letter_x] = scores
    return scoring_matrix


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag=True):
    """ str, str, dict of dict, boolean -> str, str
    Takes two input sequences with a common alphabet and scoring matrix
    and returns the alignment matrix.
    """
    len_x = len(seq_x)
    len_y = len(seq_y)
    scores = [[0 for y in range(len_y + 1)] for x in range(len_x + 1)]
    for ind_x in range(1, len_x + 1):
        pre_x = ind_x - 1
        scores[ind_x][0] = scores[pre_x][0] + scoring_matrix[seq_x[pre_x]]['-']
    for ind_y in range(1, len_y + 1):
        pre_y = ind_y - 1
        scores[0][ind_y] = scores[0][pre_y] + scoring_matrix['-'][seq_y[pre_y]]
    for row in range(1, len_x + 1):
        for col in range(1, len_y + 1):
            pre_r = row - 1
            pre_c = col - 1
            max_1 = scores[pre_r][pre_c] + scoring_matrix[seq_x[pre_r]][seq_y[pre_c]]
            max_2 = scores[pre_r][col] + scoring_matrix[seq_x[pre_r]]['-']
            max_3 = scores[row][pre_c] + scoring_matrix['-'][seq_y[pre_c]]
            scores[row][col] = max(max_1, max_2, max_3)
    return scores

# def 𝚌𝚘𝚖𝚙𝚞𝚝𝚎_𝚐𝚕𝚘𝚋𝚊𝚕_𝚊𝚕𝚒𝚐𝚗𝚖𝚎𝚗𝚝(𝚜𝚎𝚚_𝚡, 𝚜𝚎𝚚_𝚢, 𝚜𝚌𝚘𝚛𝚒𝚗𝚐_𝚖𝚊𝚝𝚛𝚒𝚡, 𝚊𝚕𝚒𝚐𝚗𝚖𝚎𝚗𝚝_𝚖𝚊𝚝𝚛𝚒𝚡):
#     pass
#
# def 𝚌𝚘𝚖𝚙𝚞𝚝𝚎_𝚕𝚘𝚌𝚊𝚕_𝚊𝚕𝚒𝚐𝚗𝚖𝚎𝚗𝚝(𝚜𝚎𝚚_𝚡, 𝚜𝚎𝚚_𝚢, 𝚜𝚌𝚘𝚛𝚒𝚗𝚐_𝚖𝚊𝚝𝚛𝚒𝚡, 𝚊𝚕𝚒𝚐𝚗𝚖𝚎𝚗𝚝_𝚖𝚊𝚝𝚛𝚒𝚡):
#     pass
#
#
# sm = build_scoring_matrix(set(['A', 'C', 'T', 'G']), 10, 4, -6)
#
# am = compute_alignment_matrix('AA', 'TAAT', sm)
#
# for a in am:
#     print a

#build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4)
#expected
#{'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
# 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
# '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
# 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
# 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
#
#but received
#{'A': {'A': 6, 'C': 2, 'T': 2, 'G': 2},
# 'C': {'A': 2, 'C': 6, 'T': 2, 'G': 2},
# '-': {'A': -4, 'C': -4, 'T': -4, 'G': -4},
# 'T': {'A': 2, 'C': 2, 'T': 6, 'G': 2},
# 'G': {'A': 2, 'C': 2, 'T': 2, 'G': 6}}
