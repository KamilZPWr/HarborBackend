import csv

import numpy as np
import tensorflow_hub as hub


class UseEmbedding:

    def __init__(self, feature_file='./assets/features_list.csv'):
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        feature_list = []
        feature_name_list = []
        with open(feature_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for idx, row in enumerate(spamreader):
                if idx > 0:
                    feature_list.append(row[1])
                    feature_name_list.append(row[0])
        self.feature_list = feature_list
        self.feature_name_list = feature_name_list
        self.feature_embeddings = self.embed(self.feature_list)

    def get_feature_list(self):
        return self.feature_list

    @staticmethod
    def cosine(u, v):
        return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


    def _get_most_importance_indices(self, text):
        text_embedding = self.embed([text])[0]
        scores = self.cosine(self.feature_embeddings, text_embedding)
        idx_range = range(len(scores))
        idx = sorted(idx_range, key=lambda x: scores[x], reverse=True)
        return idx


    def get_most_important_features(self, text, top_n=3):
        idx = self._get_most_importance_indices(text)
        idx = idx[:top_n]
        return [self.feature_name_list[i] for i in idx]


    def get_most_important_features_long(self, text, top_n=3):
        idx = self._get_most_importance_indices(text)
        idx = idx[:top_n]
        return [self.feature_list[i] for i in idx]


def main():
    ue = UseEmbedding()
    test = 'clothing store'
    features = ue.get_most_important_features(test)
    print(features)
    features_long = ue.get_most_important_features_long(test)
    print(features_long)


if __name__ == '__main__':
    main()
