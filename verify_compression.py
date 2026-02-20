from compression_utils import extract_code_summary
import os

def run_benchmark():
    # Sample Python code with class and functions
    sample_code = """
class DataProcessor:
    \"\"\"
    Processes large datasets with optimized memory management.
    Handles various data formats including CSV, JSON, and Parquet.
    \"\"\"
    def __init__(self, config: dict):
        self.config = config
        self.data = []

    def load_data(self, path: str):
        \"\"\"Load data from local filesystem.\"\"\"
        print(f"Loading from {path}")
        # Imagine 50 lines of complex loading logic here
        pass

    def transform(self, strategy: str):
        \"\"\"Apply transformations based on strategy.\"\"\"
        # Imagine 100 lines of complex math here
        pass

    def save(self, output: str):
        \"\"\"Save processed data.\"\"\"
        # Imagine 50 lines of saving logic here
        pass

def global_helper():
    \"\"\"Utility function and docstring.\"\"\"
    return True
"""
    print("--- BENCHMARK: SCALEDOWN COMPRESSION ---")
    print(f"Original Character Count: {len(sample_code)}")
    
    compressed = extract_code_summary(sample_code, "python")
    
    print("\n--- COMPRESSED OUTPUT ---")
    print(compressed)
    print("--------------------------")
    
    print(f"\nCompressed Character Count: {len(compressed)}")
    reduction = (1 - (len(compressed) / len(sample_code))) * 100
    print(f"Size Reduction: {reduction:.2f}%")

if __name__ == "__main__":
    run_benchmark()
