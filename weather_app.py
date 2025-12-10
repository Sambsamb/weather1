import requests
import sys
import os

# ------------------------------------------------------------
# API KEY SETUP (Environment Variable)
# ------------------------------------------------------------
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    print("Error: OPENWEATHER_API_KEY environment variable is not set.")
    exit(1)

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# In-memory storage for favourite cities
favourites = []   # max 3 items


# ------------------------------------------------------------
# API CALL
# ------------------------------------------------------------
def get_weather(city_name: str):
    """
    Calls the OpenWeather API to retrieve current weather for a city.
    Returns a dict on success, or None on failure.
    """
    try:
        params = {"q": city_name, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error: Unable to fetch weather for '{city_name}'. "
                  f"({response.status_code})")
            return None

    except Exception as e:
        print("❌ Exception occurred:", e)
        return None


# ------------------------------------------------------------
# DISPLAY FUNCTIONS
# ------------------------------------------------------------
def print_weather(data):
    """
    Formats and prints weather data from the OpenWeather API response.
    """
    name = data.get("name", "Unknown")
    main = data.get("main", {})
    weather = data.get("weather", [{}])[0]

    temp = main.get("temp", "N/A")
    feels = main.get("feels_like", "N/A")
    desc = weather.get("description", "N/A").title()

    print("\n------------------------------")
    print(f"Weather for: {name}")
    print("------------------------------")
    print(f"Temperature:     {temp}°C")
    print(f"Feels Like:      {feels}°C")
    print(f"Condition:       {desc}")
    print("------------------------------\n")


# ------------------------------------------------------------
# FAVOURITES MANAGEMENT
# ------------------------------------------------------------
def add_favourite(city: str):
    """
    Adds a city to favourites (max 3). Rejects duplicates.
    """
    global favourites

    if city in favourites:
        print(f"⚠️ '{city}' is already in favourites.\n")
        return

    if len(favourites) >= 3:
        print("⚠️ You already have 3 favourite cities.")
        print("Remove one before adding a new favourite.\n")
        return

    favourites.append(city)
    print(f"✅ '{city}' added to favourites.\n")


def remove_favourite(city: str):
    """
    Removes a city if it exists in favourites.
    """
    global favourites

    if city not in favourites:
        print(f"⚠️ '{city}' is not in your favourites.\n")
        return

    favourites.remove(city)
    print(f"🗑️ '{city}' removed from favourites.\n")


def list_favourites():
    """
    Displays favourite cities and their live weather.
    """
    if not favourites:
        print("⭐ No favourite cities yet.\n")
        return

    print("\n====== Favourite Cities ======")

    for city in favourites:
        data = get_weather(city)
        if data:
            print_weather(data)

    print("==============================\n")


# ------------------------------------------------------------
# APPLICATION MENU
# ------------------------------------------------------------
def menu():
    print("""
============================
 WEATHER APP - MAIN MENU
============================
1. Search weather for a city
2. Add a city to favourites
3. List favourite cities
4. Remove a city from favourites
5. Exit
============================
""")


def main():
    while True:
        menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            city = input("Enter city name: ").strip()
            data = get_weather(city)
            if data:
                print_weather(data)

        elif choice == "2":
            city = input("Enter city name to add: ").strip()
            add_favourite(city)

        elif choice == "3":
            list_favourites()

        elif choice == "4":
            city = input("Enter city name to remove: ").strip()
            remove_favourite(city)

        elif choice == "5":
            print("Goodbye! 👋")
            sys.exit()

        else:
            print("❌ Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
