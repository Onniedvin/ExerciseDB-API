import aiohttp
import asyncio

BASE_URL = "https://exercisedb-api.vercel.app/api/v1/exercises"
LIMIT = 100  # Fetch 100 exercises per request for speed improvement

async def fetch_page(session, offset):
    """Fetch a single page asynchronously."""
    url = f"{BASE_URL}?offset={offset}&limit={LIMIT}"
    async with session.get(url) as response:
        if response.status != 200:
            return None
        return await response.json()

async def fetch_all_exercises():
    """Fetch all exercises asynchronously using multiple requests."""
    async with aiohttp.ClientSession() as session:
        # Fetch the first page to determine total count
        first_page_data = await fetch_page(session, 0)
        if not first_page_data or not first_page_data.get("success"):
            print("Failed to retrieve exercises.")
            return None

        total_exercises = first_page_data["data"]["totalExercises"]
        print(f"Fetching {total_exercises} exercises")

        # Fetch all pages concurrently
        tasks = [fetch_page(session, offset) for offset in range(LIMIT, total_exercises, LIMIT)]
        results = await asyncio.gather(*tasks)

        # Combine all exercises from all pages
        exercises = first_page_data["data"]["exercises"]
        for result in results:
            if result and "exercises" in result["data"]:
                exercises.extend(result["data"]["exercises"])

        return exercises

def search_exercises(exercises, query):
    """Search exercises by keyword in their name."""
    return [ex for ex in exercises if query.lower() in ex["name"].lower()]

def display_exercises(exercises):
    """Display search results."""
    if not exercises:
        print("\nNo exercises found matching your search.")
        return False

    print("\nMatching Exercises:")
    for idx, exercise in enumerate(exercises, start=1):
        print(f"{idx}. {exercise['name']}")

    return True

def get_user_choice(exercises):
    """Let the user select an exercise or search again."""
    while True:
        choice = input("\nEnter exercise number to see details, 'n' to search again, or 'q' to quit: ").strip().lower()
        if choice == "q":
            return None
        if choice == "n":
            return "search_again"
        try:
            choice = int(choice) - 1
            if 0 <= choice < len(exercises):
                return exercises[choice]
            else:
                print("Invalid number, try again.")
        except ValueError:
            print("Invalid input, enter a number.")

def show_exercise_details(exercise):
    """Display details of the selected exercise."""
    print("\nExercise Details:")
    print(f"Name: {exercise['name']}")
    print(f"Target Muscles: {', '.join(exercise['targetMuscles'])}")
    print("Instructions:")
    for step in exercise["instructions"]:
        print(f"- {step}")
    print(f"GIF: {exercise['gifUrl']}\n")

async def main():
    """Main function to handle user interaction."""
    all_exercises = await fetch_all_exercises()
    if not all_exercises:
        return

    while True:
        query = input("\nEnter a keyword to search for exercises (or 'q' to quit): ").strip().lower()
        if query == "q":
            break

        filtered_exercises = search_exercises(all_exercises, query)
        if not display_exercises(filtered_exercises):
            continue

        while True:  # Keep looping until the user either picks an exercise or searches again
            selected_exercise = get_user_choice(filtered_exercises)
            if selected_exercise == "search_again":
                break  # Allow user to enter a new keyword
            if selected_exercise:
                show_exercise_details(selected_exercise)

if __name__ == "__main__":
    asyncio.run(main())
