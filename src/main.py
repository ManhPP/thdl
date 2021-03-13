from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class StringMatching:
    @staticmethod
    def convert_to_tfidf(corpus):
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(corpus)
        return cosine_similarity(vectors)

    @staticmethod
    def cal_edit_distance(s, t, ratio_calc=True):
        """ cal_edit_distance:
            For all i and j, distance[i,j] will contain the
            distance between the first i characters of s and the
            first j characters of t
        """
        rows = len(s) + 1
        cols = len(t) + 1
        distance = np.zeros((rows, cols), dtype=int)

        for i in range(1, rows):
            for k in range(1, cols):
                distance[i][0] = i
                distance[0][k] = k

        for col in range(1, cols):
            for row in range(1, rows):
                if s[row - 1] == t[col - 1]:
                    cost = 0
                else:
                    cost = 1

                distance[row][col] = min(distance[row - 1][col] + 1,  # Cost of deletions
                                         distance[row][col - 1] + 1,  # Cost of insertions
                                         distance[row - 1][col - 1] + cost)  # Cost of substitutions
        if ratio_calc:
            # ratio = ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))
            ratio = 1 - distance[row][col] / max(len(s), len(t))
            return ratio
        else:
            return distance[row][col]


if __name__ == '__main__':
    corpus = [
        '128',
        '512'
    ]
    print(StringMatching.convert_to_tfidf(corpus))
    # print(StringMatching.cal_edit_distance(corpus[0], corpus[1]))
