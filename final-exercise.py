import asyncio
import openai
from pptx import Presentation


async def extract_text_from_powerpoint(filepath):
    """
    Extracts text from a PowerPoint presentation.

    Args:
        filepath (str): The path to the PowerPoint presentation file.

    Returns:
        list: A list of strings, where each string represents the text content of a slide.
              If an error occurs during extraction, an empty list is returned.
    """
    try:
        prs = Presentation(filepath)
        text_list = []
        for slide in prs.slides:
            text = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        text.append(paragraph.text)
            text_list.append(' '.join(text))
        return text_list
    except Exception as e:
        print(f"Error occurred while extracting text: {str(e)}")
        return []


async def ask_chatgpt(prompt):
    """
    Generates a response from the ChatGPT model based on a given prompt.

    Args:
        prompt (str): The prompt for generating the response.

    Returns:
        str: The generated response from the ChatGPT model.
    """
    openai.api_key = "API_KEY"
    response =  await asyncio.to_thread(openai.ChatCompletion.create,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt}
        ],
    )
    if 'choices' in response:
        return response['choices'][0]['message']['content'].strip()
    return ""


async def main():
    file_path = input("Enter the file path to the PowerPoint presentation: ")
    text = await extract_text_from_powerpoint(file_path)

    explanations = []
    for slide_text in text:
        prompt = f"Can you pls explain to me about: {slide_text}\n\n"
        response_text = await ask_chatgpt(prompt)
        explanations.append(response_text)
    print(explanations)


if __name__ == '__main__':
    asyncio.run(main())
