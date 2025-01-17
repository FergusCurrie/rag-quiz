PROMPT_QUESTION = """
You will be provided information on a concept from an academic STEM subject. 
You will use your knowledge to generate 5 questions and answers to test the students knowledge of the concept. 
The questions should be no more than a few sentences. 
Give your answer in the format: 
1. 
Question: <question>
Answer: <answer>
2.
...
"""

PROMPT_ANSWER = """
You are judging the answer of a student to a quiz question. 
You will be provided the following:
Question: 
Answer: 
Correct Answer: 
Using a combination of your own knowledge and the correct answer, please give a short judgement on the quality of the answer and provide a rating between 1 and 10. 
Where 10 is perfect and 1 is terrible answer. 
Please respond with:
Response: 
Score: 
"""


from openai import OpenAI


def validate_qa_format(response: str) -> bool:
    """
    Validates if the response follows the expected Q&A format:
    1.
    Question: <question>
    Answer: <answer>
    2.
    ...
    """
    lines = response.strip().split("\n")
    current_number = 1
    expected_patterns = [str(current_number) + ".", "Question:", "Answer:"]
    pattern_index = 0

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        if pattern_index == 0:  # Should be number
            if line != expected_patterns[0]:
                return False
            pattern_index = 1

        elif pattern_index == 1:  # Should be Question
            if not line.startswith(expected_patterns[1]):
                return False
            pattern_index = 2

        elif pattern_index == 2:  # Should be Answer
            if not line.startswith(expected_patterns[2]):
                return False
            pattern_index = 0
            current_number += 1
            expected_patterns[0] = str(current_number) + "."

    return current_number == 6  # Should have processed 5 questions


def parse_qa_response(response: str) -> dict:
    """
    Parses the Q&A response into a dictionary format:
    {
        1: {'question': 'What is...?', 'answer': 'The answer is...'},
        2: {'question': '...', 'answer': '...'},
        ...
    }
    """
    qa_dict = {}
    current_number = None
    current_qa = {}

    for line in response.strip().split("\n"):
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        # Check for number
        if line.endswith(".") and line[:-1].isdigit():
            # Save previous Q&A if it exists
            if current_number is not None and current_qa:
                qa_dict[current_number] = current_qa

            current_number = int(line[:-1])
            current_qa = {}
            continue

        # Check for Question
        if line.startswith("Question:"):
            current_qa["question"] = line[len("Question:") :].strip()
            continue

        # Check for Answer
        if line.startswith("Answer:"):
            current_qa["answer"] = line[len("Answer:") :].strip()
            continue

    # Don't forget to save the last Q&A pair
    if current_number is not None and current_qa:
        qa_dict[current_number] = current_qa

    return qa_dict


def query_concept_quiz(concept: str):
    client = OpenAI()
    print(f"Sending concept: {concept}")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "developer", "content": PROMPT_QUESTION}, {"role": "user", "content": concept}],
    )
    content = completion.to_dict()["choices"][0]["message"]["content"]

    if not validate_qa_format(content):
        print(content)
        raise Exception("Schema validation failed.")

    return parse_qa_response(content)


def validate_judge_response(response: str) -> bool:
    """
    Validates if the response follows the expected answer format:
    Response: <feedback>
    Score: <number between 1-10>
    """
    lines = response.strip().split("\n")
    has_response = False
    has_score = False

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        if line.startswith("Response:"):
            has_response = True
        elif line.startswith("Score:"):
            # Verify score is a number between 1-10
            try:
                score = int(line[len("Score:") :].strip())
                has_score = 1 <= score <= 10
            except ValueError:
                return False

    return has_response and has_score


def parse_judge_response(response: str) -> dict:
    """
    Parses the answer response into a dictionary format:
    {
        'response': 'feedback text...',
        'score': integer_score
    }
    """
    result = {}

    for line in response.strip().split("\n"):
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        if line.startswith("Response:"):
            result["response"] = line[len("Response:") :].strip()
        elif line.startswith("Score:"):
            result["score"] = int(line[len("Score:") :].strip())

    return result


def judge_quiz_answer(question: str, user_answer: str, correct_answer: str):
    client = OpenAI()
    message_content = f"""
    Question: {question}
    Answer: {user_answer}
    Correct Answer: {correct_answer} 
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "developer", "content": PROMPT_ANSWER}, {"role": "user", "content": message_content}],
    )
    content = completion.to_dict()["choices"][0]["message"]["content"]

    if not validate_judge_response(content):
        raise Exception("Schema validation failed.")

    return parse_judge_response(content)
