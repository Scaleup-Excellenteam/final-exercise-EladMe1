import asyncio
import os
import re
import shutil

from database import Upload, session

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
        # Scan from database
        files_pending = session.query(Upload).filter_by(status="pending").all()

        # Process each file
        for file in files_pending:
            uid = file.uid
            file_path = "uploads\\" + uid + ".pptx"
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

            handle_pending(file_path, "remove")  # Update status and finish time in the database


def handle_pending(file_path, action):
    """
    Move or remove a file from the pending folder.

    Args:
        file_path (str): The path of the file to be moved or removed.
        action (str): The action to perform. Can be "add" to move the file to the pending folder or "remove" to delete
            the file from the pending folder.

    Returns:
        None
    """
    file_name = os.path.basename(file_path)
    uidFile = file_path.split('\\')[-1].split('.')[0]
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
            # Update status and finish time in the database
            upload = session.query(Upload).filter_by(uid=uidFile).first()
            if upload:
                upload.status = "done"
                upload.set_finish_time()
                session.commit()


if __name__ == '__main__':
    asyncio.run(main())


