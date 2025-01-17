from openai import OpenAI


class InterfaceJudgeResponse:
    def __init__(self, prompt_id: int, prompt: str, model: str = "gpt-4o-mini"):
        self.prompt_id = prompt_id
        self.prompt = prompt
        self.model = model

    def judge_quiz_answer(self, question: str, user_answer: str, correct_answer: str):
        client = OpenAI()
        message_content = f"""
        Question: {question}
        Answer: {user_answer}
        Correct Answer: {correct_answer} 
        """
        completion = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "developer", "content": self.prompt}, {"role": "user", "content": message_content}],
        )
        content = completion.to_dict()["choices"][0]["message"]["content"]

        if not self._validate_judge_response(content):
            raise Exception("Schema validation failed.")

        result = self._parse_judge_response(content)
        result["prompt_id"] = self.prompt_id
        return result

    def _parse_qa_response(self, response: str) -> dict:
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

    def _parse_judge_response(self, response: str) -> dict:
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

    def _validate_judge_response(self, response: str) -> bool:
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
