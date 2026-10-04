# Movie Recommendation System

This project is a content-based movie recommendation system
developed in Python.

The system recommends movies based on similarities in genre,
movie descriptions, and keywords.

## Technologies Used

- Python
- Pandas
- scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- Gradio

## How the System Works

1. Movie information is loaded from a CSV dataset.
2. Genre, description, and keyword information is combined.
3. TF-IDF converts textual information into numerical vectors.
4. Cosine similarity measures similarity between movies.
5. The system ranks movies based on similarity.
6. The highest-ranked movies are presented to the user.

## Features

- Movie selection using a dropdown
- Content-based recommendations
- Adjustable recommendation count
- Movie genre information
- Similarity scores
- Graphical user interface using Gradio

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt