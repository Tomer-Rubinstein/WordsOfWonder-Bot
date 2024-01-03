import os
from dotenv import load_dotenv
from openai import OpenAI


class GPT:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")

    def find_anagrams(self, letters) -> list[str]:
        client = OpenAI(api_key=self.api_key)

        prompt = f"""\
        Find 100 different anagrams that are valid English words from the letters \"{letters}\".
        Only write the valid anagrams without additional text or notes.
        Seperate your answers by newlines only.
        Write your answers in caps.
        Only include answers which have more than 3 letters.
        """

        print("\nSENDING PROMPT:\n" + prompt + "\n")

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        gpt_answer = chat_completion.choices[0].message.content
        return list(set(gpt_answer.split("\n"))) # remove duplicates
