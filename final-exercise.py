import asyncio
import os
import re
import shutil

from extract_text import extract_text_from_powerpoint
from chatgpt import generate_explanation
from save_file import save_explanations_on_json_file


async def main() -> None:
    """
    Main function to extract text from PowerPoint, generate explanations using ChatGPT,
    and save the explanations to a JSON file.
    """
    while True:
        await asyncio.sleep(10)
        # Scan the uploads folder
        files = os.listdir('uploads')

        # Process each file
        for file in files:
            file_path = os.path.join('uploads', file)
            print(file_path)
            text: list[str] = await extract_text_from_powerpoint(file_path)
            handle_pending(file_path, "add")
            explanations: list[str] = []
            for slide_text in text:
                prompt: str = f"Can you please explain to me about this slide: {slide_text}\n\n"
                response_text: str = await generate_explanation(prompt)
                explanations.append(response_text)

            print(explanations)

            # Replace ".pptx" with ".json" using regular expressions
            new_file_path = re.sub(r"\.pptx$", r".json", file_path)

            save_explanations_on_json_file(explanations, new_file_path)

            handle_pending(file_path, "remove")


def handle_pending(file_path, action):
    file_name = os.path.basename(file_path)
    pending_dir = 'pending'

    if action == "add":
        if not os.path.exists(pending_dir):
            os.makedirs(pending_dir)
        # Move the file from uploads to pending folder
        shutil.move(file_path, os.path.join(pending_dir, file_name))
    elif action == "remove":
        # Remove the file from the pending folder
        file_in_pending = os.path.join(pending_dir, file_name)
        if os.path.exists(file_in_pending):
            os.remove(file_in_pending)


if __name__ == '__main__':
    asyncio.run(main())
