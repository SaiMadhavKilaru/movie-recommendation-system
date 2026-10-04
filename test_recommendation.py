from recommendation import recommend_movies


# TEST CASES

test_cases = [
    {
        "movie": "Interstellar",
        "category": "Science Fiction / Space"
    },
    {
        "movie": "The Dark Knight",
        "category": "Superhero / Crime"
    },
    {
        "movie": "The Avengers",
        "category": "Superhero / Marvel"
    },
    {
        "movie": "Titanic",
        "category": "Drama / Romance"
    },
    {
        "movie": "Toy Story",
        "category": "Animation / Family"
    },
    {
        "movie": "Jurassic Park",
        "category": "Science Fiction / Adventure"
    },
    {
        "movie": "Frozen",
        "category": "Animation / Fantasy"
    }
]


# RUN TESTS

print(
    "\n================================="
)

print(
    "MOVIE RECOMMENDATION SYSTEM TEST"
)

print(
    "=================================\n"
)


for test_number, test in enumerate(
    test_cases,
    start=1
):

    movie_title = test["movie"]

    category = test["category"]

    print(
        f"TEST {test_number}"
    )

    print(
        f"Selected Movie: "
        f"{movie_title}"
    )

    print(
        f"Expected Category: "
        f"{category}"
    )

    try:

        recommendations = (
            recommend_movies(
                movie_title,
                5
            )
        )

        print(
            "Recommendations:"
        )

        for number, movie in enumerate(
            recommendations,
            start=1
        ):

            print(
                f"  {number}. "
                f"{movie['title']} "
                f"({movie['similarity']}%)"
            )

        print(
            "\nSTATUS: PASSED "
            "- recommendations generated"
        )

    except Exception as error:

        print(
            f"\nSTATUS: FAILED "
            f"- {error}"
        )

    print(
        "\n---------------------------------\n"
    )


print(
    "Testing complete."
)

print(
    "\nERROR-HANDLING TESTS\n"
)


# Test invalid movie
try:

    recommend_movies(
        "Movie That Does Not Exist",
        5
    )

    print(
        "Invalid movie test: FAILED"
    )

except ValueError:

    print(
        "Invalid movie test: PASSED"
    )


# Test empty movie
try:

    recommend_movies(
        "",
        5
    )

    print(
        "Empty movie test: FAILED"
    )

except ValueError:

    print(
        "Empty movie test: PASSED"
    )


# Test invalid recommendation count
try:

    recommend_movies(
        "Interstellar",
        "abc"
    )

    print(
        "Invalid count test: FAILED"
    )

except ValueError:

    print(
        "Invalid count test: PASSED"
    )