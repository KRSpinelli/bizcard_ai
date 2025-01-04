# bizcard-ai

`bizcard-ai` is a Python package that extracts information from images of business cards using the OpenAI API. It processes an image file and returns a dict containing the extracted details.

## Features

- Extracts text information from business card images.
- Returns data in a structured JSON format.
- Includes a graphical user interface (GUI) for easy image uploading and result viewing.

## Installation

Install the package using pip:

```bash
pip install bizcard-ai
```

## Setup

Before using `bizcard-ai`, set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

Replace `your_openai_api_key` with your actual OpenAI API key.

## Usage

### Extract Information from an Image

Use the `get_image_information` function to process a business card image and obtain the extracted information:

```python
from bizcard_ai import get_image_information

filepath = 'path_to_your_image.jpg'
info = get_image_information(filepath)
print(info)
```

Replace `'path_to_your_image.jpg'` with the path to your business card image file.

### Launch the GUI

To use the graphical interface for uploading a business card image and viewing the results:

```python
from bizcard_ai import load_test_gui

load_test_gui()
```

This will open a window where you can upload an image and see the extracted information.

## License

This project is licensed under the GNU General Public License v3.0.

## Contact

For questions or support, please contact [kyle.spinelli@gmail.com](mailto:kyle.spinelli@gmail.com). 
