from core.pipeline import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    # Test run
    result = pipeline.run("What is the current repo rate in India?")
    print("\nAnswer:", result["answer"])
    print("\nEvaluation:", result["evaluation"])
