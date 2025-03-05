from ics import Calendar
import requests

# Gets uni events from ical link, and compares to the cache.
#   If no changes since cache, return False
#   If calendar has changed since cache, update cache and return the events set
def getUniEvents ():
    # Parse the URL
    url = "https://timetable.sydney.edu.au/odd/rest/calendar/ical/a190fe5d-f66a-46e0-9be0-e4d0547aa373"
    cal = Calendar(requests.get(url).text)

    # Fetch the cached ical file from before 
    cache_file = open("py_envs/scheddy/cache.txt", "r")
    cache = cache_file.read()
    cache_file.close()

    if str(cal.events) != cache:
        # Update the cache file and return events
        cache_file = open("cache.txt", "w")
        cache_file.write(str(cal.events))
        cache_file.close()
        return cal.events
    else: 
        return False

