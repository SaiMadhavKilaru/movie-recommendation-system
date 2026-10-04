import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# STEP 1: LOAD AND VALIDATE DATASET

DATASET_FILE = "movies.csv"

required_columns = {
    "title",
    "genre",
    "description",
    "keywords"
}


def load_movies():
    """
    Load the movie dataset and perform basic validation.
    """

    if not os.path.exists(DATASET_FILE):
        raise FileNotFoundError(
            f"Dataset file '{DATASET_FILE}' was not found."
        )

    data = pd.read_csv(DATASET_FILE)

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            "The dataset is missing required columns: "
            + ", ".join(missing_columns)
        )

    if data.empty:
        raise ValueError("The movie dataset is empty.")

    # Remove duplicate movie titles
    data = data.drop_duplicates(
        subset=["title"]
    ).reset_index(drop=True)

    # Handle missing values
    data["title"] = data["title"].fillna("")
    data["genre"] = data["genre"].fillna("")
    data["description"] = data["description"].fillna("")
    data["keywords"] = data["keywords"].fillna("")

    return data


movies = load_movies()

# STEP 2: CREATE WEIGHTED FEATURES

"""
Genre and keywords are intentionally repeated.

This causes those features to contribute more strongly
to the TF-IDF representation than the description.

Weighting:

Genre       = 3
Keywords    = 2
Description = 1
"""


movies["weighted_features"] = (
    movies["genre"] + " "
    + movies["genre"] + " "
    + movies["genre"] + " "
    + movies["keywords"] + " "
    + movies["keywords"] + " "
    + movies["description"]
)

# STEP 3: TF-IDF VECTORIZATION

try:

    tfidf = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = tfidf.fit_transform(
        movies["weighted_features"]
    )

except ValueError as error:

    raise RuntimeError(
        f"Unable to create TF-IDF matrix: {error}"
    )


# STEP 4: CALCULATE COSINE SIMILARITY

similarity_matrix = cosine_similarity(
    tfidf_matrix
)


# STEP 5: HELPER FUNCTION FOR EXPLANATIONS

def get_shared_features(selected_movie, recommended_movie):
    """
    Find common genres and keywords between two movies.
    """

    selected_genres = set(
        selected_movie["genre"]
        .lower()
        .split()
    )

    recommended_genres = set(
        recommended_movie["genre"]
        .lower()
        .split()
    )

    selected_keywords = set(
        selected_movie["keywords"]
        .lower()
        .split()
    )

    recommended_keywords = set(
        recommended_movie["keywords"]
        .lower()
        .split()
    )

    shared_genres = sorted(
        selected_genres.intersection(
            recommended_genres
        )
    )

    shared_keywords = sorted(
        selected_keywords.intersection(
            recommended_keywords
        )
    )

    return shared_genres, shared_keywords


# STEP 6: CREATE "WHY RECOMMENDED?" EXPLANATION

def create_explanation(
        selected_movie,
        recommended_movie
):

    shared_genres, shared_keywords = (
        get_shared_features(
            selected_movie,
            recommended_movie
        )
    )

    explanation_parts = []

    if shared_genres:

        explanation_parts.append(
            "shared genres: "
            + ", ".join(shared_genres)
        )

    if shared_keywords:

        explanation_parts.append(
            "shared themes/keywords: "
            + ", ".join(
                shared_keywords[:5]
            )
        )

    if not explanation_parts:

        return (
            "Recommended because its overall "
            "text features are similar."
        )

    return (
        "Recommended because of "
        + " and ".join(explanation_parts)
        + "."
    )


# STEP 7: RECOMMENDATION FUNCTION

def recommend_movies(
        movie_title,
        number_of_recommendations=5
):

    # Input validation

    if not movie_title:

        raise ValueError(
            "Please select a movie."
        )

    try:
        number_of_recommendations = int(
            number_of_recommendations
        )

    except (TypeError, ValueError):

        raise ValueError(
            "Number of recommendations "
            "must be a valid number."
        )

    if number_of_recommendations < 1:

        raise ValueError(
            "Number of recommendations "
            "must be greater than zero."
        )

    max_recommendations = len(movies) - 1

    if (
        number_of_recommendations
        > max_recommendations
    ):

        number_of_recommendations = (
            max_recommendations
        )

    # Find selected movie

    matches = movies[
        movies["title"]
        .str.lower()
        .str.strip()
        ==
        movie_title.lower().strip()
    ]

    if matches.empty:

        raise ValueError(
            f"Movie '{movie_title}' "
            "was not found in the dataset."
        )

    movie_index = matches.index[0]

    selected_movie = movies.iloc[
        movie_index
    ]

    # Get similarity scores

    scores = list(
        enumerate(
            similarity_matrix[
                movie_index
            ]
        )
    )

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove selected movie itself
    scores = [
        item
        for item in scores
        if item[0] != movie_index
    ]

    scores = scores[
        :number_of_recommendations
    ]

    recommendations = []

    # Build recommendation objects

    for index, score in scores:

        recommended_movie = movies.iloc[
            index
        ]

        explanation = (
            create_explanation(
                selected_movie,
                recommended_movie
            )
        )

        recommendations.append(
            {
                "title":
                    recommended_movie[
                        "title"
                    ],

                "genre":
                    recommended_movie[
                        "genre"
                    ],

                "description":
                    recommended_movie[
                        "description"
                    ],

                "similarity":
                    round(
                        float(score) * 100,
                        2
                    ),

                "explanation":
                    explanation
            }
        )

    return recommendations


# MANUAL COMMAND-LINE TEST

if __name__ == "__main__":

    try:

        selected_movie = "Interstellar"

        results = recommend_movies(
            selected_movie,
            5
        )

        print(
            f"\nRecommendations for "
            f"{selected_movie}:\n"
        )

        for movie in results:

            print(
                movie["title"],
                "-",
                movie["similarity"],
                "%"
            )

            print(
                "Why:",
                movie["explanation"]
            )

            print()

    except Exception as error:

        print(
            "Application error:",
            error
        )