import requests
import time

def check_api_health(base_url: str, max_retries: int = 30) -> bool:
    """Check if the API is healthy and ready"""
    for i in range(max_retries):
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend API is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < max_retries - 1:
            print(f"⏳ Waiting for backend API... ({i+1}/{max_retries})")
            time.sleep(2)
    
    return False