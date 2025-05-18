import json
import os
from datetime import datetime

def save_search_results(highest_rated, cheapest):
    """
    Save search results to a JSON file and a readable text file.
    
    Args:
        highest_rated: Dictionary containing details of the highest rated listing
        cheapest: Dictionary containing details of the cheapest listing
    """
    # Create a results directory if it doesn't exist
    results_dir = "search_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_filename = f"airbnb_results_{timestamp}"
    
    # Create a dictionary with all the data
    results_data = {
        "search_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "highest_rated_listing": highest_rated,
        "cheapest_listing": cheapest
    }
    
    # Save as JSON
    json_path = os.path.join(results_dir, f"{base_filename}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=4, ensure_ascii=False)
    
    # Save as readable text
    txt_path = os.path.join(results_dir, f"{base_filename}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("AIRBNB SEARCH RESULTS\n")
        f.write("=====================\n\n")
        f.write(f"Search Date: {results_data['search_date']}\n\n")
        
        # Write highest rated listing details
        f.write("HIGHEST RATED LISTING:\n")
        f.write("-----------------------\n")
        f.write(f"Name: {highest_rated.get('name', 'Unknown')}\n")
        f.write(f"Rating: {highest_rated.get('rating', 'Unknown')}\n")
        f.write(f"Price: {highest_rated.get('price', 'Unknown')}\n\n")
        
        # Write cheapest listing details
        f.write("CHEAPEST LISTING:\n")
        f.write("----------------\n")
        f.write(f"Name: {cheapest.get('name', 'Unknown')}\n")
        f.write(f"Rating: {cheapest.get('rating', 'Unknown')}\n")
        f.write(f"Price: {cheapest.get('price', 'Unknown')}\n")
    
    print(f"Results saved to:\n- {json_path}\n- {txt_path}")
    
    return json_path, txt_path