from langchain.tools import tool

@tool
def find_route(from_station: str, to_station: str) -> str:
    """
    Finds and provides the metro route between two stations.
    Example: from_station = "Sarthana", to_station = "DREAM City"
    """
    from_station = from_station.lower().strip()
    to_station = to_station.lower().strip()

    red_line = [
        "sarthana", "nature park", "varachha chopati garden", "kapodra",
        "labheshwar chowk", "central warehouse", "surat railway station",
        "maskati hospital", "gandhi baug", "majura gate", "althan tenament",
        "althan gam", "vip road", "bhimrad", "convention center", "dream city"
    ]

    green_line = [
        "bhesan", "botanical garden", "adajan gam", "athwa chopati",
        "majura gate", "udhna darwaja", "kamela darwaja", "anjana farm",
        "model town", "magob", "saroli"
    ]

    # Same line check
    if from_station in red_line and to_station in red_line:
        return "Both stations are on the Red Line. Direct train is available. Route: Red Line"

    if from_station in green_line and to_station in green_line:
        return "Both stations are on the Green Line. Direct train is available. Route: Green Line"

    # Interchange needed
    if (from_station in red_line and to_station in green_line) or \
       (from_station in green_line and to_station in red_line):
        return "An interchange is required at Majura Gate. Board the train to Majura Gate, then switch to the other line."

    return "Sorry, could not find these stations. Please provide valid station names."

@tool
def calculate_fare(from_station: str, to_station: str) -> str:
    """
    Calculates and provides the approximate fare between two stations.
    """
    # Simple fare estimation logic (can be expanded later)
    return "The approximate fare is between ₹10 and ₹40. The exact fare depends on the total distance traveled."

@tool
def get_station_info(station_name: str) -> str:
    """
    Returns basic information and highlights about a given station.
    """
    station_name = station_name.lower().strip()

    info = {
        "majura gate": "Majura Gate is a key interchange station where both the Red Line and Green Line connect.",
        "dream city": "DREAM City is the terminal station on the Red Line.",
        "sarthana": "Sarthana is the starting terminal station on the Red Line.",
        "bhesan": "Bhesan is the starting terminal station on the Green Line.",
        "surat railway station": "This underground station provides direct connectivity to Surat Railway Station."
    }

    return info.get(station_name, f"Limited information is available for {station_name.title()} station.")