import asyncio
import os
import re

from extract_text import extract_text_from_powerpoint
from chatgpt import generate_explanation
from save_file import save_explanations_on_json_file


async def main() -> None:
    """
    Main function to extract text from PowerPoint, generate explanations using ChatGPT,
    and save the explanations to a JSON file.
    """
    while True:
        asyncio.sleep(10)
        # Scan the uploads folder
        files = os.listdir('uploads')

        # Process each file
        for file in files:
            file_path = os.path.join('uploads', file)
        print(file_path)
        text: list[str] = await extract_text_from_powerpoint(file_path)

        explanations: list[str] = []
        for slide_text in text:
            prompt: str = f"Can you please explain to me about this slide: {slide_text}\n\n"
            response_text: str = await generate_explanation(prompt)

            explanations.append(response_text)

        print(explanations)

        # Replace ".pptx" with ".json" using regular expressions
        new_file_path = re.sub(r"\.pptx$", r".json", file_path)

        save_explanations_on_json_file(explanations, new_file_path)


if __name__ == '__main__':
    asyncio.run(main())
