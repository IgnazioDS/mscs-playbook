from src.nlp.vectorizers import TfidfVectorizerLite


def test_tfidf_shape():
    vec = TfidfVectorizerLite()
    X = vec.fit_transform(["alpha beta", "beta gamma"])
    assert X.shape[0] == 2
    assert X.shape[1] > 0
