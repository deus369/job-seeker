import re

def convert_text_to_slug(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove any non-alphanumeric characters
    text = re.sub(r'\s+', '-', text)  # Replace whitespace with '-'
    text = text.lower()  # Convert to lowercase
    return text

# def convert_text_to_slug(text):
#     text = text.replace(" ", "-")
#     text = text.lower()
#     return text

# print(convert_text_to_slug("Game Designer")) # Output: "game-designer"
