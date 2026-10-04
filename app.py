import gradio as gr

from recommendation import (
    movies,
    recommend_movies
)

# GENERATE RECOMMENDATIONS

def generate_recommendations(
        movie_title,
        number_of_recommendations
):

    try:

        recommendations = recommend_movies(
            movie_title,
            number_of_recommendations
        )

        if not recommendations:

            return (
                "No recommendations "
                "were found."
            )

        output = (
            f"# Recommendations for "
            f"{movie_title}\n\n"
        )

        for number, movie in enumerate(
            recommendations,
            start=1
        ):

            output += (
                f"## {number}. "
                f"{movie['title']}\n\n"

                f"**Genre:** "
                f"{movie['genre']}\n\n"

                f"**Similarity Score:** "
                f"{movie['similarity']}%\n\n"

                f"**Description:** "
                f"{movie['description']}\n\n"

                f"**Why was this recommended?**  \n"
                f"{movie['explanation']}\n\n"

                "---\n\n"
            )

        return output

    except ValueError as error:

        return (
            f"⚠️ **Input Error:** "
            f"{error}"
        )

    except FileNotFoundError as error:

        return (
            f"⚠️ **Dataset Error:** "
            f"{error}"
        )

    except Exception as error:

        return (
            "⚠️ **Unexpected Error:** "
            f"{error}"
        )


# MOVIE TITLES

movie_titles = sorted(
    movies["title"].tolist()
)


# BUILD APPLICATION

with gr.Blocks(
    title="Movie Recommendation System"
) as demo:

    # Application heading

    gr.Markdown(
        """
# 🎬 Movie Recommendation System

Choose a movie you enjoy and this application will
recommend similar movies using a **content-based
recommendation algorithm**.

The system analyzes movie **genres, keywords, and
descriptions**, converts those features using
**TF-IDF**, and compares movies using
**cosine similarity**.
        """
    )

    # Application information section

    with gr.Accordion(
        "ℹ️ About This Application",
        open=False
    ):

        gr.Markdown(
            """
### How the Recommendation System Works

This application uses a content-based filtering approach.

1. Movie information is loaded from a CSV dataset.
2. Genre, keywords, and descriptions are used as movie features.
3. Genre information receives the highest weighting.
4. Keywords receive additional weighting.
5. TF-IDF converts the text features into numerical vectors.
6. Cosine similarity measures how similar movies are.
7. Movies with the highest similarity scores are returned.

### Recommendation Weighting

- **Genre:** Higher importance
- **Keywords:** Medium importance
- **Description:** Standard importance

### Recommendation Explanation

For every recommendation, the system identifies shared
genres and themes to explain why the movie was suggested.

### Technologies

- Python
- Pandas
- scikit-learn
- TF-IDF
- Cosine Similarity
- Gradio
            """
        )

    # User controls

    movie_dropdown = gr.Dropdown(
        choices=movie_titles,
        label="Select a Movie",
        info=(
            "Choose a movie you already enjoy."
        )
    )

    recommendation_count = gr.Slider(
        minimum=3,
        maximum=10,
        value=5,
        step=1,
        label="Number of Recommendations"
    )

    recommend_button = gr.Button(
        "Find Recommendations",
        variant="primary"
    )

    # Results

    recommendation_output = (
        gr.Markdown()
    )

    recommend_button.click(
        fn=generate_recommendations,
        inputs=[
            movie_dropdown,
            recommendation_count
        ],
        outputs=(
            recommendation_output
        )
    )


# START APPLICATION

if __name__ == "__main__":

    demo.launch()