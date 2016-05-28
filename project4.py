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
    alignment = [[0 for dummy_idy in range(len_y + 1)] for dummy_idx in range(len_x + 1)]

    for ind_x in range(1, len_x + 1):
        if global_flag == False:
            alignment[ind_x][0] = max(0,
                                   alignment[ind_x - 1][0] + scoring_matrix[seq_x[ind_x - 1]]['-'])
        else:
            alignment[ind_x][0] = alignment[ind_x - 1][0] + scoring_matrix[seq_x[ind_x - 1]]['-']

    for ind_y in range(1, len_y + 1):
        if global_flag == False:
            alignment[0][ind_y] = max(0,
                                   alignment[0][ind_y - 1] + scoring_matrix['-'][seq_y[ind_y - 1]])
        else:
            alignment[0][ind_y] = alignment[0][ind_y - 1] + scoring_matrix['-'][seq_y[ind_y - 1]]

    for row in range(1, len_x + 1):
        for col in range(1, len_y + 1):
            potential_max = max(alignment[row - 1][col - 1] + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]],
                                   alignment[row - 1][col] + scoring_matrix[seq_x[row - 1]]['-'],
                                   alignment[row][col - 1] + scoring_matrix['-'][seq_y[col - 1]])
            if global_flag == False:
                alignment[row][col] = max(0, potential_max)
            else:
                alignment[row][col] = potential_max

    return alignment


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """ str, str, dict of dict, list of list -> tuple(int, str, str)
    Takes two sequences that share a common alphabet with the scoring matrix and
    computes a global alignment of seq_x and seq_y using the alignment_matrix.
    The function returns a tuple (score, align_x, align_y).
    """
    ind_x, ind_y = len(seq_x), len(seq_y)
    score = 0
    align_x, align_y = '', ''
    global_alignment = [score, align_x, align_y]
    ind = [ind_x, ind_y]

    while ind_x > 0 and ind_y > 0:
        score, align_x, align_y, ind_x, ind_y, ind = compute_alignment(global_alignment, ind, seq_x, seq_y, scoring_matrix, alignment_matrix)
    while ind_x > 0:
        score, align_x, align_y, ind_x = compute_leading_dashes_y(global_alignment, ind_x, seq_x, seq_y, scoring_matrix, alignment_matrix)
    while ind_y > 0:
        score, align_x, align_y, ind_y = compute_leading_dashes_x(global_alignment, ind_y, seq_x, seq_y, scoring_matrix, alignment_matrix)
    return (score, align_x, align_y)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """ str, str, dict of dict, list of list -> tuple(int, str, str)
    Takes two sequences that share a common alphabet with the scoring matrix and
    computes a local alignment of seq_x and seq_y using the alignment_matrix.
    The function returns a tuple (score, align_x, align_y).
    """
    rows = len(seq_x)
    cols = len(seq_y)
    score = 0
    ind_x = rows
    ind_y = cols

    for row in range(rows + 1):
        for col in range(cols + 1):
            if score <= alignment_matrix[row][col]:
                score = alignment_matrix[row][col]
                ind_x = row
                ind_y = col

    score = 0
    align_x, align_y = '', ''

    local_alignment = [score, align_x, align_y]
    ind = [ind_x, ind_y]

    while ind_x > 0 and ind_y > 0:
        if alignment_matrix[ind_x][ind_y] == 0:
            break
        score, align_x, align_y, ind_x, ind_y, ind = compute_alignment(local_alignment, ind, seq_x, seq_y, scoring_matrix, alignment_matrix)
    while ind_x > 0:
        if alignment_matrix[ind_x][ind_y] == 0:
            break
        score, align_x, align_y, ind_x = compute_leading_dashes_y(local_alignment, ind_x, seq_x, seq_y, scoring_matrix, alignment_matrix)
    while ind_y > 0:
        if alignment_matrix[ind_x][ind_y] == 0:
            break
        score, align_x, align_y, ind_y = compute_leading_dashes_x(local_alignment, ind_y, seq_x, seq_y, scoring_matrix, alignment_matrix)

    return (score, align_x, align_y)


def compute_alignment(alignment, ind, seq_x, seq_y, scoring_matrix, alignment_matrix):
    """ int, str, str, int, int, str, str, dict of dict, list of list -> int, str, str, int, int
    Helper function that takes the current alignment strings and score and then
    computes the next pair in the alignment.  Returns the current position in
    seq_x and seq_y as well as the current score and alignment strings.
    """
    if alignment_matrix[ind[0]][ind[1]] == alignment_matrix[ind[0] - 1][ind[1] - 1] + scoring_matrix[seq_x[ind[0] - 1]][seq_y[ind[1] - 1]]:
        alignment[1] = seq_x[ind[0] - 1] + alignment[1]
        alignment[2] = seq_y[ind[1] - 1] + alignment[2]
        ind[0] -= 1
        ind[1] -= 1
    else:
        if alignment_matrix[ind[0]][ind[1]] == alignment_matrix[ind[0] - 1][ind[1]] + scoring_matrix[seq_x[ind[0] - 1]]['-']:
            alignment[1] = seq_x[ind[0] - 1] + alignment[1]
            alignment[2] = '-' + alignment[2]
            ind[0] -= 1
        else:
            alignment[1] = '-' + alignment[1]
            alignment[2] = seq_y[ind[1] - 1] + alignment[2]
            ind[1] -= 1
    alignment[0] += scoring_matrix[alignment[1][0]][alignment[2][0]]

    return alignment[0], alignment[1], alignment[2], ind[0], ind[1], ind


def compute_leading_dashes_y(alignment, ind_x, seq_x, seq_y, scoring_matrix, alignment_matrix):
    """ int, str, str, int, str, str, dict of dict, list of list -> int, str, str, int, int
    Helper function that takes the current alignment strings and score and then
    computes the next pair in the alignment with the remaining values in the y
    alignment string being dashes.  Returns the current position in seq_x and
    seq_y as well as the current score and alignment strings.
    """
    alignment[1] = seq_x[ind_x - 1] + alignment[1]
    alignment[2] = '-' + alignment[2]
    ind_x -= 1
    alignment[0] += scoring_matrix[alignment[1][0]][alignment[2][0]]

    return alignment[0], alignment[1], alignment[2], ind_x


def compute_leading_dashes_x(alignment, ind_y, seq_x, seq_y, scoring_matrix, alignment_matrix):
    """ int, str, str, int, str, str, dict of dict, list of list -> int, str, str, int, int
    Helper function that takes the current alignment strings and score and then
    computes the next pair in the alignment with the remaining values in the x
    alignment string being dashes.  Returns the current position in seq_x and
    seq_y as well as the current score and alignment strings.
    """
    alignment[1] = '-' + alignment[1]
    alignment[2] = seq_y[ind_y - 1] + alignment[2]
    ind_y -= 1
    alignment[0] += scoring_matrix[alignment[1][0]][alignment[2][0]]

    return alignment[0], alignment[1], alignment[2], ind_y
