# -*- coding: utf-8 -*-
from sentence_transformers import SentenceTransformer
import numpy as np


class FastLexRankSummarizer:
    """
    Calculate the LexRank score for each sentence in the corpus and return the top sentences using a fast implementation.
    :param corpus: list of sentences
    :param model_path: path to the sentence transformer model used for sentence embeddings
    :param threshold: threshold for the cosine similarity
    :return: list of sentences with the highest LexRank score
    """

    def __init__(
        self,
        corpus: list[str],
        model_path: str = "all-MiniLM-L12-v2",
        threshold: float = None,
    ) -> None:
        self.corpus = corpus
        self.model_path = model_path
        self.threshold = threshold

    def _get_sentence_embeddings(self) -> np.ndarray:
        """
        Calculate the sentence embeddings for the corpus
        :return: sentence embeddings
        """
        model = SentenceTransformer(self.model_path)
        embeddings = model.encode(self.corpus)
        return embeddings

    def _get_similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Calculate the cosine similarity between all sentences
        :param embeddings: sentence embeddings
        :return: cosine similarity matrix
        """
        similarity_matrix = np.inner(embeddings, embeddings)
        return similarity_matrix

    def get_lexrank_scores(self) -> np.ndarray:
        """
        Calculate the LexRank score for each sentence
        :param similarity_matrix: cosine similarity matrix
        :return: LexRank scores
        """
        embeddings = self._get_sentence_embeddings()
        similarity_matrix = self._get_similarity_matrix(embeddings)
        if self.threshold:
            similarity_matrix[similarity_matrix < self.threshold] = 0

        # Transpose the similarity matrix
        F = similarity_matrix.T
        # Normalize the similarity matrix
        z = similarity_matrix.sum(axis=0)
        z = z / np.sqrt((z**2).sum(axis=0))
        # Calculate the LexRank scores
        approx_scores = np.dot(z.T, F)
        return approx_scores

    def _get_top_sentences(self, lexrank_scores: np.ndarray, n: int = 3) -> list:
        """
        Return the top sentences with the highest LexRank score
        :param lexrank_scores: LexRank scores
        :param n: number of sentences to return
        :return: list of sentences with the highest LexRank score
        """
        top_sentences = np.argsort(lexrank_scores)[::-1][:n]
        return top_sentences

    def summarize(self, n: int = 3) -> list[str]:
        """
        Calculate the LexRank score for each sentence in the corpus and return the top sentences
        :param n: number of sentences to return
        :return: list of sentences with the highest LexRank score
        """

        lexrank_scores = self.get_lexrank_scores()
        top_sentences = self._get_top_sentences(lexrank_scores, n)
        return [self.corpus[i] for i in top_sentences]

    def __call__(self, n: int = 3) -> list:
        """
        Calculate the LexRank score for each sentence in the corpus and return the top sentences
        :param n: number of sentences to return
        :return: list of sentences with the highest LexRank score
        """
        return self.summarize(n)

    def __repr__(self) -> str:
        return f"fastLexRankSummarizer(corpus={self.corpus}, model_path={self.model_path}, threshold={self.threshold}, alpha={self.alpha})"

    def __str__(self) -> str:
        return f"fastLexRankSummarizer(corpus={self.corpus}, model_path={self.model_path}, threshold={self.threshold}, alpha={self.alpha})"


if __name__ == "__main__":
    sentences = [
        "One of David Cameron's closest friends and Conservative allies, "
        "George Osborne rose rapidly after becoming MP for Tatton in 2001.",
        "Michael Howard promoted him from shadow chief secretary to the "
        "Treasury to shadow chancellor in May 2005, at the age of 34.",
        "Mr Osborne took a key role in the election campaign and has been at "
        "the forefront of the debate on how to deal with the recession and "
        "the UK's spending deficit.",
        "Even before Mr Cameron became leader the two were being likened to "
        "Labour's Blair/Brown duo. The two have emulated them by becoming "
        "prime minister and chancellor, but will want to avoid the spats.",
        "Before entering Parliament, he was a special adviser in the "
        "agriculture department when the Tories were in government and later "
        "served as political secretary to William Hague.",
        "The BBC understands that as chancellor, Mr Osborne, along with the "
        "Treasury will retain responsibility for overseeing banks and "
        "financial regulation.",
        "Mr Osborne said the coalition government was planning to change the "
        'tax system "to make it fairer for people on low and middle '
        'incomes", and undertake "long-term structural reform" of the '
        "banking sector, education and the welfare state.",
    ]
    summarizer = FastLexRankSummarizer(sentences)
    print(summarizer.summarize())
