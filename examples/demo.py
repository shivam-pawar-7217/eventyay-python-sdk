from eventyay.client import EventyayClient
from eventyay.exceptions import EventyayConnectionError

def main():
    print("🚀 Connecting to Eventyay API...")
    client = EventyayClient()

    try:
        # Fetch public events
        events = client.get_events()
        print(f"✅ Successfully fetched {len(events)} events!")
        
        for event in events[:3]:
            print(f"- {event['name']} (ID: {event['id']})")
            
    except EventyayConnectionError:
        print("❌ Connection Error: Please check your internet connection.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
