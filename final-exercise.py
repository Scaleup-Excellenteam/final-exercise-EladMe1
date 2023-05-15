from pptx import Presentation


def extract_text_from_powerpoint(filepath):
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


def main():
    file_path = input("Enter the file path to the PowerPoint presentation: ")
    text = extract_text_from_powerpoint(file_path)
    print(text)


if __name__ == '__main__':
    main()
