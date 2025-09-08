import requests
import json
import time
from urllib.parse import urlparse, parse_qs
from colorama import Fore, Style, init
import pyfiglet

# Initialize colors
init(autoreset=True)
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
WHITE = Fore.WHITE

def banner():
    print(GREEN + pyfiglet.figlet_format("Code2Crypto"))
    print(f"{CYAN} Tool Name : {GREEN}Shiba Bot")
    print(f"{CYAN} Developed by {GREEN}@Anaik_Dev")
    print("=" * 60)
    print(WHITE + "Type 'exit' or 'quit' anytime to stop the program.")
    print("=" * 60)

def extract_session_from_url(url):
    """Extract session value from the link"""
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get('session', [None])[0]
    except Exception:
        return None

def make_view_request(session_id):
    """Send view request"""
    url = f"https://botpayproject.com/site/view.php?session={session_id}"
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        'sec-ch-ua': "\"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': "\"Android\"",
        'upgrade-insecure-requests': "1",
        'sec-fetch-site': "cross-site",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'accept-language': "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response
    except requests.RequestException as e:
        print(RED + f"Error in view request: {e}")
        return None

def complete_task(session_id):
    """Complete the task"""
    url = "https://botpayproject.com/site/complete_task.php"
    
    payload = {
        "session": session_id
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        'Content-Type': "application/json",
        'sec-ch-ua': "\"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua-mobile': "?1",
        'origin': "https://botpayproject.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': f"https://botpayproject.com/site/view.php?session={session_id}",
        'accept-language': "en-US,en;q=0.9"
    }
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
        return response
    except requests.RequestException as e:
        print(RED + f"Error in completing task: {e}")
        return None

def main():
    """Main function"""
    banner()
    
    while True:
        try:
            print(YELLOW + "\n" + "="*60)
            user_input = input(WHITE + "Enter link to start: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print(RED + "\n⏹️ Program terminated by user.")
                print("=" * 60)
                break
            
            if not user_input:
                print(RED + "❌ No link entered!")
                continue
            
            session_id = extract_session_from_url(user_input)
            if not session_id:
                print(RED + "❌ Error: session not found in link!")
                print(YELLOW + "Make sure the link contains ?session=")
                continue
            
            print(GREEN + f"✅ Extracted Session ID: {session_id}")
            print(CYAN + "🔄 Starting process...")
            
            # Send view request
            print(YELLOW + "\n1️⃣ Sending view request...")
            view_response = make_view_request(session_id)
            
            if view_response and view_response.status_code == 200:
                print(GREEN + "✅ View request successful")
                print(f"{CYAN}📄 View response:")
                print("-" * 40)
                print(view_response.text)
                print("-" * 40)
            else:
                print(RED + "❌ Failed to send view request")
                if view_response:
                    print(RED + f"Error code: {view_response.status_code}")
                continue
            
            # Wait before completing task
            print(YELLOW + "\n⏳ Waiting 3 seconds before completing task...")
            time.sleep(3)
            
            # Complete the task
            print(YELLOW + "2️⃣ Sending complete task request...")
            complete_response = complete_task(session_id)
            
            if complete_response and complete_response.status_code == 200:
                print(GREEN + "✅ Task completed successfully")
                print(f"{CYAN}📋 Complete task response:")
                print("-" * 40)
                print(complete_response.text)
                print("-" * 40)
            else:
                print(RED + "❌ Failed to complete task")
                if complete_response:
                    print(RED + f"Error code: {complete_response.status_code}")
            
            print(GREEN + "\n✅ Process finished! You can enter a new link or type 'exit' to quit.")
            print("=" * 60)
                
        except KeyboardInterrupt:
            print(RED + "\n⏹️ Program stopped by user")
            print("=" * 60)
            break
        except Exception as e:
            print(RED + f"❌ Unexpected error: {e}")
            print(YELLOW + "Try again...")

if __name__ == "__main__":
    main()