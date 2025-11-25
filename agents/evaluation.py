import logging

logger = logging.getLogger(__name__)

class EvaluationAgent:
    def evaluate(self, query: str, answer: str, context_docs: list):
        """
        Evaluates the generated answer.
        """
        logger.info("Evaluating answer")
        
        # Ensure answer is a string
        if isinstance(answer, list):
            answer = " ".join(str(item) for item in answer)
        elif not isinstance(answer, str):
            answer = str(answer)
        
        # Simple heuristic evaluation
        score = 0.0
        feedback = []
        
        # Check if answer is too short
        if len(answer) < 50:
            feedback.append("Answer is too short.")
        else:
            score += 0.3
            
        # Check for citations (simple check for brackets)
        if "[" in answer and "]" in answer:
            score += 0.4
        else:
            feedback.append("No citations found.")
            
        # Check relevance (keyword overlap - very basic)
        query_words = set(query.lower().split())
        answer_words = set(answer.lower().split())
        overlap = query_words.intersection(answer_words)
        if len(overlap) > 0:
            score += 0.3
        else:
            feedback.append("Low keyword overlap with query.")
            
        return {
            "score": round(score, 2),
            "feedback": feedback
        }

evaluation_agent = EvaluationAgent()
