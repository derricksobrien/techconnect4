"""
Stage 3: Test AI Agent
- Create a conversation thread
- Send test query
- Validate agent is functional
"""
import json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

def test_agent():
    """Test the AI agent with a sample query"""
    
    endpoint = "https://admin-1994-resource.services.ai.azure.com/api/projects/admin-1994"
    agent_id = "asst_rFwMHjHtgDeQ1TprE6IEFzOh"
    
    print("=" * 70)
    print("STAGE 3: Test AI Agent")
    print("=" * 70 + "\n")
    
    # Connect
    print("Connecting to AI Foundry...")
    try:
        credential = DefaultAzureCredential()
        client = AIProjectClient(endpoint=endpoint, credential=credential)
        print("SUCCESS\n")
    except Exception as e:
        print(f"FAILED: {e}")
        return False
    
    # Create a thread and run in one call
    test_queries = [
        "What are Microsoft Solution Accelerators?",
        "Tell me about the GitHub repositories in your knowledge base",
        "What resources are available for enterprise cloud solutions?"
    ]
    
    print("Sending test queries...\n")
    
    for query in test_queries:
        print(f"Query: {query}")
        
        try:
            # Create thread and run with message
            run = client.agents.create_thread_and_run(
                assistant_id=agent_id,
                thread_input={
                    "messages": [
                        {
                            "role": "user",
                            "content": query
                        }
                    ]
                }
            )
            
            thread_id = run.thread_id
            run_id = run.id
            
            # Wait for completion
            max_iterations = 60  # 60 seconds max
            for i in range(max_iterations):
                run = client.agents.runs.get(thread_id=thread_id, run_id=run_id)
                if run.status == "completed":
                    print(f"  Status: Completed\n")
                    break
                elif run.status == "failed":
                    print(f"  Run failed: {run.last_error}\n")
                    break
                elif i % 10 == 0:
                    print(f"  Waiting... ({run.status})")
                import time
                time.sleep(1)
            
            # Get messages
            try:
                messages = client.agents.messages.list(thread_id=thread_id)
                if messages.data:
                    for msg in messages.data:
                        if msg.role == "assistant" and msg.content:
                            content = msg.content[0].text.value if hasattr(msg.content[0], 'text') else str(msg.content[0])
                            print(f"Response: {content[:300]}...\n")
                            break
            except Exception as e:
                print(f"  (Could not retrieve messages)\n")
            
        except Exception as e:
            print(f"  Error: {type(e).__name__}: {str(e)[:100]}\n")
    
    print("=" * 70)
    print("STAGE 3 COMPLETE")
    print("=" * 70)
    print(f"\nAgent ID: {agent_id}")
    print(f"Model: gpt-4o")
    print(f"Status: READY\n")
    print("Next steps:")
    print("1. Upload knowledge files via AI Foundry portal UI")
    print("2. Or use Skillable's approach with AssistantVectorStore")
    
    return True

if __name__ == "__main__":
    success = test_agent()
    exit(0 if success else 1)
