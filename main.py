import sys
from core.graph import MultiMemoryGraph
from dotenv import load_dotenv

load_dotenv()

def main():
    print("--- Multi-Memory Agent (Lab 17) ---")
    print("Initializing...")
    
    try:
        agent = MultiMemoryGraph()
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return

    user_id = "user_default"
    print(f"User ID: {user_id}")
    print("Commands: '/exit' to quit, '/memory off' to disable memory, '/memory on' to enable.")
    
    with_memory = True
    history = [] # Maintain conversation history here
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == '/exit':
            break
        elif user_input.lower() == '/memory off':
            with_memory = False
            print("Memory disabled.")
            continue
        elif user_input.lower() == '/memory on':
            with_memory = True
            print("Memory enabled.")
            continue
            
        try:
            result = agent.run(user_id, user_input, with_memory=with_memory, history=history)
            response = result['messages'][-1]
            history.append(HumanMessage(content=user_input))
            history.append(response) # Store AI response too
            
            response_text = response.content
            intent = result.get('intent', 'N/A')
            memories = result.get('retrieved_memories', [])
            
            print(f"\n[Intent: {intent}]")
            if memories:
                print(f"[Retrieved {len(memories)} memory snippets]")
            
            print(f"Agent: {response}")
            
        except Exception as e:
            print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
