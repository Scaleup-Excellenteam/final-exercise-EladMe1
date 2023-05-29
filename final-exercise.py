import asyncio
import os
from dotenv import load_dotenv
from extract_text import extract_text_from_powerpoint
from chatgpt import generate_explanation
from save_file import save_explanations_on_json_file

# Load environment variables from API.env
load_dotenv("API.env")

# Access the API key
API_KEY = os.getenv("API_KEY")


async def main() -> None:
    """
    Main function to extract text from PowerPoint, generate explanations using ChatGPT,
    and save the explanations to a JSON file.
    """
    file_path: str = input("Enter the file path to the PowerPoint presentation: ")
    text: list[str] = await extract_text_from_powerpoint(file_path)

    explanations: list[str] = []
    for slide_text in text:
        prompt: str = f"Can you please explain to me about: {slide_text}\n\n"
        response_text: str = await generate_explanation(prompt, API_KEY)
        explanations.append(response_text)

    print(explanations)

    explanations_file: str = "explanations.json"
    save_explanations_on_json_file(explanations, explanations_file)


if __name__ == '__main__':
    asyncio.run(main())
