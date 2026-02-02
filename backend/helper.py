from typing import List
from models import SearchResult


def extract_data(data: dict) -> List[dict]:
    """
    Extract only isbn, title, author, and publication_year from Google Books API response.
    """

    results = []

    if "items" not in data:
        return results

    for item in data["items"]:
        volume_info = item.get("volumeInfo", {})

        # Extract ISBN
        identifiers = volume_info.get("industryIdentifiers", [])
        isbn = ", ".join(
            f"{item['type']}: {item['identifier']}" for item in identifiers
        )

        # Extract title
        title = volume_info.get("title", "")

        # Extract authors
        authors_list = volume_info.get("authors", [])
        authors = ", ".join(authors_list)

        # Extract publication year 
        published_year = volume_info.get("publishedDate", "")
        if len(published_year) > 0:
            publication_year = int(published_year[:4])
        else:
            publication_year = None
            

        results.append(
            SearchResult(
                isbn = isbn,
                title = title,
                author = authors,
                publication_year = publication_year
            )
        )

    return results
