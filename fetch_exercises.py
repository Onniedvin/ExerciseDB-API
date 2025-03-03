import aiohttp
import asyncio

BASE_URL = "https://exercisedb-api.vercel.app/api/v1/exercises"
LIMIT = 100

async def fetch_page(session, offset):
    """Fetch a single page asynchronously."""
    url = f"{BASE_URL}?offset={offset}&limit={LIMIT}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            return None
        return await response.json()

async def fetch_all_exercises():
    """Fetch all exercises asynchronously using multiple requests."""
    async with aiohttp.ClientSession() as session:
        first_page_data = await fetch_page(session, 0)
        if not first_page_data or not first_page_data.get("success"):
            print("Failed to retrieve exercises.")
            return None

        total_exercises = first_page_data["data"]["totalExercises"]
        tasks = [fetch_page(session, offset) for offset in range(LIMIT, total_exercises, LIMIT)]
        results = await asyncio.gather(*tasks)

        # Combine all exercises
        exercises = first_page_data["data"]["exercises"]
        for result in results:
            if result and "exercises" in result["data"]:
                exercises.extend(result["data"]["exercises"])

        return exercises

def search_exercises(exercises, query):
    """Search exercises by keyword in their name."""
    return [ex for ex in exercises if query.lower() in ex["name"].lower()]

def get_exercises():
    """Wrapper function to fetch exercises synchronously for Flask."""
    return asyncio.run(fetch_all_exercises())


