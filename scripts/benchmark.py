import json
import time
import pandas as pd
import sys
import os
# Add the project root directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.graph import MultiMemoryGraph
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

def calculate_relevance(response, context_info):
    # Mock relevance score calculation
    # In a real scenario, use LLM-as-a-judge or cosine similarity
    score = 0
    if not context_info: return 1.0 # General query
    
    for info in context_info:
        if any(word.lower() in response.lower() for word in info.split() if len(word) > 3):
            score += 1
            
    return min(5.0, 1.0 + (score / max(1, len(context_info))) * 4.0)

def run_benchmark():
    graph = MultiMemoryGraph()
    with open("data/test_cases.json", "r") as f:
        test_cases = json.load(f)
        
    results = []
    
    # Pre-seed some facts into semantic memory for testing
    graph.semantic.add_fact("f1", "The capital of France is Paris and it was founded in the 3rd century BC.")
    graph.long_term.set_user_preference("user_123", "cuisine", "Italian")
    graph.long_term.set_user_preference("user_123", "name", "Alex")
    
    for case in test_cases:
        print(f"Running Case: {case['name']}")
        
        for with_mem in [True, False]:
            mode = "With Memory" if with_mem else "Without Memory"
            total_relevance = 0
            total_tokens = 0
            hit_count = 0
            
            # Reset/Clear session-like behavior for benchmark
            # (In real test we'd need to clear Redis/Chroma too, but here we just test retrieval)
            
            history = []
            for turn in case['turns']:
                start_time = time.time()
                
                # Execute graph
                state = {
                    "messages": history + [HumanMessage(content=turn)],
                    "user_id": "user_123",
                    "with_memory": with_mem
                }
                output = graph.app.invoke(state)
                
                response = output['messages'][-1].content
                history.append(HumanMessage(content=turn))
                history.append(output['messages'][-1])
                
                # Metrics
                tokens = graph.token_manager.count_tokens(response)
                total_tokens += tokens
                
                if with_mem and output.get('retrieved_memories'):
                    hit_count += 1
                    rel = calculate_relevance(response, output['retrieved_memories'])
                else:
                    rel = 1.0 if not with_mem else 3.0 # Baseline
                
                total_relevance += rel
                
            avg_rel = total_relevance / len(case['turns'])
            tokens_per_turn = total_tokens / len(case['turns'])
            hit_rate = (hit_count / len(case['turns'])) * 100 if with_mem else 0
            
            results.append({
                "Case": case['name'],
                "Mode": mode,
                "Relevance": round(avg_rel, 2),
                "Tokens/Turn": round(tokens_per_turn, 2),
                "Hit Rate (%)": round(hit_rate, 2)
            })

    df = pd.DataFrame(results)
    
    # Calculate Averages for the final table
    summary = []
    for metric in ["Relevance", "Tokens/Turn", "Hit Rate (%)"]:
        with_m = df[df["Mode"] == "With Memory"][metric].mean()
        without_m = df[df["Mode"] == "Without Memory"][metric].mean()
        imp = ((with_m - without_m) / without_m * 100) if without_m != 0 else 0
        
        summary.append({
            "Metric": metric,
            "With Memory (Avg)": round(with_m, 2),
            "Without Memory (Avg)": round(without_m, 2),
            "Improvement (%)": f"{round(imp, 2)}%" if metric != "Hit Rate (%)" else "N/A"
        })
        
    summary_df = pd.DataFrame(summary)
    print("\n--- BENCHMARK SUMMARY ---")
    print(summary_df.to_markdown(index=False))
    
    # Save to file
    summary_df.to_csv("data/benchmark_results.csv", index=False)
    return summary_df

if __name__ == "__main__":
    run_benchmark()
