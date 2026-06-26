import time
import numpy as np
import torch

class SaGeQueryEngine:
    def __init__(self, data, time_quantum=0.1):
        """
        Initialize the SaGe query engine.

        Args:
            data (list of dict): The dataset represented as a list of dictionaries.
            time_quantum (float): Maximum time (in seconds) allowed for a single execution slice.
        """
        self.data = data
        self.time_quantum = time_quantum
        self.query_state = None

    def execute_query(self, query_fn, resume_state=None):
        """
        Execute a SPARQL-like query with preemption support.

        Args:
            query_fn (function): A function that takes a data item and returns True if it matches the query.
            resume_state (dict): State to resume query execution from.

        Returns:
            tuple: (results, new_state) where results is the list of matched items and new_state is the state to resume.
        """
        start_time = time.time()
        results = []
        state = resume_state if resume_state else {"index": 0}

        while state["index"] < len(self.data):
            item = self.data[state["index"]]
            if query_fn(item):
                results.append(item)
            
            state["index"] += 1

            # Check if the time quantum has been exceeded
            if time.time() - start_time >= self.time_quantum:
                return results, state

        # If we finish processing all data, return None as the new state
        return results, None

if __name__ == '__main__':
    # Dummy dataset
    dataset = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
        {"id": 3, "name": "Charlie", "age": 35},
        {"id": 4, "name": "Diana", "age": 40},
        {"id": 5, "name": "Eve", "age": 28},
    ]

    # Query function: Find people older than 30
    def query_fn(item):
        return item["age"] > 30

    # Initialize the SaGe query engine
    sage_engine = SaGeQueryEngine(dataset, time_quantum=0.05)

    # Execute the query with preemption
    state = None
    all_results = []
    while True:
        results, state = sage_engine.execute_query(query_fn, resume_state=state)
        all_results.extend(results)
        print(f"Partial results: {results}")
        if state is None:  # Query execution is complete
            break

    print(f"Final results: {all_results}")