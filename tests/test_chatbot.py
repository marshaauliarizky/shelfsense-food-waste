from src.chatbot import answer_question


def test_chatbot_answers_top_waste_question(sample_frame):
    response = answer_question("Which product has the most waste?", sample_frame, "2026-09-01")
    assert response.supported is True
    assert response.intent == "top_waste_product"
    assert "waste" in response.text.lower()


def test_chatbot_does_not_invent_answer_for_unsupported_question(sample_frame):
    response = answer_question("What will sales be next year?", sample_frame, "2026-09-01")
    assert response.supported is False
    assert "supported" in response.text.lower()
