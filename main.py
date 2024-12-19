from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from mangum import Mangum
  
app = FastAPI()
handler = Mangum(app)

class Book(BaseModel):
  id: str
  title: str
  authors: list[str] = []
  description: str
  thumbnail: str = None
  
@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get("/search", response_model=list[Book])
async def search(q: str, offset: int = 0, limit: int = 40):
  GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"
  try:
    async with httpx.AsyncClient() as client:
      response = await client.get(GOOGLE_BOOKS_API, params={"q": q, "startIndex": offset, "maxResults": limit })
      response.raise_for_status()
      # Reference - https://developers.google.com/books/docs/v1/reference/volumes/list
      data = response.json()

      books = []
      for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})

        thumbnail_url = volume_info.get("imageLinks", {}).get("thumbnail")
        
        book = Book(
          id=item.get("id", ""),
          title=volume_info.get("title", "No title available"),
          authors=volume_info.get("authors", []),
          description=volume_info.get("description", "No description available"),
          thumbnail=thumbnail_url
        )
        books.append(book)
          
      return books
  except httpx.HTTPError as e:
    raise HTTPException(status_code=400, detail=f"Error fetching books: {str(e)}")
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
