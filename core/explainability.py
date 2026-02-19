class ExplainabilityEngine:
    def __init__(self, model, vectorizer):
        self.model = model
        self.vectorizer = vectorizer

    def build_reasoning(
        self,
        keywords,
        keyword_score,
        ml_pred,
        ml_prob,
        final_score,
        scam_category,
        confidence
    ):

        explanation = []

        # 1️⃣ Keyword reasoning
        if keywords:
            explanation.append(
                f"- Scam indicators detected: {', '.join(keywords)}."
            )
            explanation.append(
                f"- Keyword engine contributed a risk score of {keyword_score}."
            )
        else:
            explanation.append(
                "- No explicit scam-related keywords were detected."
            )

        # 2️⃣ ML reasoning
        explanation.append(
            f"- AI model prediction: {ml_pred} "
            f"(Probability: {ml_prob:.2f}%)."
        )

        explanation.append(
            f"- Model confidence level: {confidence:.2f}%."
        )

        # 3️⃣ Category reasoning
        explanation.append(
            f"- Identified scam category: {scam_category}."
        )

        # 4️⃣ Final risk reasoning
        explanation.append(
            f"- Final hybrid risk score: {final_score}% "
            f"(combined ML probability and keyword signals)."
        )

        return "\n".join(explanation)
