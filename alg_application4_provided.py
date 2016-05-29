"""
Provide code and solution for Application 4
"""


import math
import random
import urllib2
import matplotlib.pyplot as plt
import alg_project4_solution as student



# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"


###############################################
# provided code


def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


###############################################
# My code

human = read_protein(HUMAN_EYELESS_URL)
fruit_fly = read_protein(FRUITFLY_EYELESS_URL)
scoring_matrix = read_scoring_matrix(PAM50_URL)
consensus = read_protein(CONSENSUS_PAX_URL)

# # Question 1
# alignment_matrix = student.compute_alignment_matrix(human, fruit_fly, scoring_matrix, False)
# hum_ff_l_align = student.compute_local_alignment(human, fruit_fly, scoring_matrix, alignment_matrix)
# print "Question 1"
# print "Score:", hum_ff_l_align[0]
# print "Human:", hum_ff_l_align[1]
# print "Fruit fly:", hum_ff_l_align[2], "\n"
#
# # Answer 1:
# # Score: 875
# # Human: 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ'
# # Fruit Fly: 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ'
#
#
# # Question 2
# human = 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQ'
# fruit_fly = 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ'
#
# hum_con_al_mat = student.compute_alignment_matrix(human, consensus, scoring_matrix)
# hum_con_g_align = student.compute_global_alignment(human, consensus, scoring_matrix, hum_con_al_mat)
#
# ff_con_al_mat = student.compute_alignment_matrix(fruit_fly, consensus, scoring_matrix)
# ff_con_g_align = student.compute_global_alignment(fruit_fly, consensus, scoring_matrix, ff_con_al_mat)
#
# def compare_sequences(seq_x, seq_y):
#     """ str, str -> float
#     Takes two strings and returns a percentage for how many letters at the same
#     index are the same value.
#     """
#     letters = len(seq_x)
#     len_y = len(seq_y)
#     same = 0
#     if letters != len_y:
#         return "Sequences of differing length"
#     for letter in range(letters):
#         if seq_x[letter] == seq_y[letter]:
#             same += 1
#     print "len:", letters
#     return (float(same) / letters) * 100
#
# human_percent = compare_sequences(hum_con_g_align[1], hum_con_g_align[2])
# fruit_fly_percent = compare_sequences(ff_con_g_align[1], ff_con_g_align[2])
#
# print "Question 2"
# # print "Human-Consensus Score:", hum_con_g_align[0]
# # print "Human Global Alignment to Consensus:", hum_con_g_align[1]
# # print "Consensus Global Alignment to Human:", hum_con_g_align[2]
# print "Human Percent Similar:", human_percent
#
# # print "Fruit Fly-Consensus Score:", ff_con_g_align[0]
# # print "Fruit Fly Global Alignment to Consensus:", ff_con_g_align[1]
# # print "Consensus Global Alignment to Fruit Fly:", ff_con_g_align[2]
# print "Fruit Fly Percent Similar:", fruit_fly_percent, "\n"
#
# # Answer 2
# # Human Percent Similar: 72.932%
# # Fruit Fly Percent Similar: 70.149%
#
#
# # Answer 3
# # No, it is not likely that the similarity could be due to chance.  If we were
# # to randomly assign proteins we'd get a 1 in 23 chance for a match at each
# # position in the sequence. This means that around 70% of the sequences of over
# # 130 proteins (so, about 90 proteins of the 130) would need to hit that 1/23
# # chance. So, the chance of a random match up of over 130 proteins being 70%
# # similar is about  1/(23^90).  Not likely to happen.


# Question 4
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """ str, str, dict of dict, int -> dict
    Takes two sequences, a scoring matrix, and a number of trials, and returns
    a dictionary of unnormalized
    """
    scoring_distribution = {}
    for trial in range(num_trials):
        list_y = list(seq_y)
        random.shuffle(list_y)
        rand_y = ''.join(list_y)
        alignment_matrix = student.compute_alignment_matrix(human, rand_y, scoring_matrix, False)
        alignment = student.compute_local_alignment(human, rand_y, scoring_matrix, alignment_matrix)
        score = alignment[0]
        if score in scoring_distribution:
            scoring_distribution[score] += 1
        else:
            scoring_distribution[score] = 1
    return scoring_distribution


def plot_distribution(scoring_distribution):
    x_values = []
    y_values = []
    normal_check = 0
    for score in scoring_distribution:
        x_values.append(score)
        y_values.append(float(scoring_distribution[score]) / 1000)
        normal_check += float(scoring_distribution[score]) / 1000
    print "Normal?", normal_check

    plt.bar(x_values, y_values)

    plt.grid(True)
    line1 = 'Normalized Distribution of Human Eyeless Protein Sequence\n'
    line2 = 'Scored with Fruit Fly Sequences Randomly Shuffled\n'
    line3 = 'Python Desktop Environment\n'
    plt.ylabel('Normalized Distribution')
    plt.xlabel('Scores')
    plt.title(line1 + line2 + line3)

    plt.show()

scoring_dist = generate_null_distribution(human, fruit_fly, scoring_matrix, 1000)
#plot_distribution(scoring_dist)


# Question 5

def mean_score(scoring_distribution):
    total_score = 0
    for score in scoring_distribution:
        total_score += score
    return float(total_score) / 1000

def standard_deviation(scoring_distribution, mean_score):
    deviation = 0
    for score in scoring_distribution:
        deviation += (score - mean_score)**2
    deviation = float(deviation) / 1000
    return deviation

def z_score(alignment_score, mean_score, standard_deviation):
    return (alignment_score - mean_score) / standard_deviation

mean = mean_score(scoring_dist)
deviation = standard_deviation(scoring_dist, mean)
z = z_score(875, mean, deviation)

print "Scoring Distribution"
print "Mean:", mean
print "Standard Deviation:", deviation
print "z-score:", z
