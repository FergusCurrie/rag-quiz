from openai import OpenAI


class InterfaceCreateQA:
    def __init__(self, prompt_id: int, prompt: str, model: str = "gpt-4o-mini"):
        self.prompt_id = prompt_id
        self.prompt = prompt
        self.model = model

        pass

    def create_quiz_for_concept(self, concept: str):
        client = OpenAI()
        completion = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "developer", "content": self.prompt}, {"role": "user", "content": concept}],
        )

        content = completion.to_dict()["choices"][0]["message"]["content"]

        if not self._validate_qa_format(content):
            print(content)
            raise Exception("Schema validation failed.")

        return self._parse_qa_response(content)

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

    def _validate_qa_format(self, response: str) -> bool:
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
