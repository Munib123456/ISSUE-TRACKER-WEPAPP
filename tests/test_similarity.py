"""
Tests for the TF-IDF duplicate detection logic.

The production function find_similar_issues in app/utils/__init__.py depends on
a database call (get_issues_for_board), which makes it harder to unit test in
isolation. These tests verify the underlying TF-IDF + cosine similarity logic
that powers it, using the same scikit-learn calls that the production function
uses. Any change to the similarity algorithm would also need to be reflected
here, so these tests act as a regression guard on the core duplicate-detection
behaviour.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarity(text_a, text_b):
    """Replicates the TF-IDF + cosine similarity logic used in find_similar_issues."""
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return score


def test_identical_text_returns_high_similarity():
    """Two identical strings should score very close to 1.0."""
    score = compute_similarity(
        "Python loops are confusing",
        "Python loops are confusing"
    )
    assert score > 0.99


def test_similar_phrasing_above_threshold():
    """Two issues describing the same problem with different words should clear the 0.3 threshold."""
    score = compute_similarity(
        "Struggling with SQL queries in the database lab",
        "Struggling with sql"
    )
    assert score >= 0.3


def test_unrelated_topics_below_threshold():
    """Two completely unrelated issues should score well below the 0.3 threshold."""
    score = compute_similarity(
        "I cannot log into my student portal",
        "How do I submit my coursework assignment"
    )
    assert score < 0.3


def test_python_loops_duplicate_detection():
    """Specific scenario from the test report - two phrasings of the Python loops issue."""
    score = compute_similarity(
        "I dont understand Python loops",
        "Python loops are confusing"
    )
    # Expect this to clear the 0.3 threshold based on shared 'python' and 'loops' terms
    assert score >= 0.3


def test_stopwords_are_filtered():
    """Generic stopwords like 'the', 'is', 'at' should not inflate similarity scores."""
    score = compute_similarity(
        "the cat is at the door",
        "the dog is in the garden"
    )
    # Without stopword filtering this would be artificially high; with filtering it should be low
    assert score < 0.5