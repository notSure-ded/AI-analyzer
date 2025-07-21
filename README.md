PDF Question Paper Extractor
This project is a Python-based tool designed to analyze PDF documents, specifically educational materials like question papers. It extracts all meaningful content—text, images, questions, options, and answers—and organizes it into a clean, structured, and machine-readable JSON file.



Features
High-Precision Text Extraction: Extracts text at a granular level to prevent unrelated content from being merged.

Image Extraction: Identifies and saves all images from the PDF, linking them to their respective questions and options.

Intelligent Content Parsing: Differentiates between the question body, question images, option text, option images, and the correct answer.

Structured JSON Output: The final output is a clean, predictable JSON array, making it easy to use as an input for other applications, such as AI models or databases.

Command-Line Interface: The main extraction script uses command-line arguments for flexibility and ease of use in automated workflows.

Prerequisites
Before you begin, ensure you have Python 3 installed on your system. You will also need to install the following Python libraries:

PyMuPDF: For core PDF parsing and content extraction.

Pillow: For robust image handling and saving.

You can install these dependencies using pip:

pip install PyMuPDF Pillow

How to Use
The process is divided into two main steps. First, you extract the raw structured data from the PDF. Second, you process that raw data to create the final, clean JSON file.

Step 1: Extract Structured Content from the PDF
This step reads the source PDF and creates an intermediate JSON file (structured_content.json) that contains all text and image blocks with their coordinates.

Place your source PDF file (e.g., IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf) in the project's root directory.

Run the main extraction script (main.py) from your terminal, providing the PDF file as an argument.

python main.py "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"

This will create a new folder named pdf_structured_output. Inside, you will find:

structured_content.json: The raw, block-by-block data.

An images folder containing all the extracted image files.

Step 2: Process the Structured Data into Final JSON
This step reads the intermediate structured_content.json, applies the parsing logic to understand the layout, and generates the final, clean question file.

Make sure you have successfully completed Step 1.

Run the final processing script (final_processor.py) from your terminal. It requires no arguments as it knows where to find the input file.

python final_processor.py

The script will create a new file, final_questions.json, inside the pdf_structured_output folder. This is your final, clean output.

Final Output Structure
The final_questions.json file is an array of question objects. Each object follows this structure:

[
    {
        "question_number": 1,
        "question_text": "Find the next figures in the figure pattern given below.",
        "question_images": [
            "images\\page_1_image_1.png"
        ],
        "options": {
            "A": {
                "text": "",
                "image": "images\\page_1_image_2.png"
            },
            "B": {
                "text": "",
                "image": "images\\page_1_image_3.png"
            },
            "C": {
                "text": "",
                "image": "images\\page_1_image_4.png"
            },
            "D": {
                "text": "",
                "image": "images\\page_1_image_5.png"
            }
        },
        "correct_answer": "D"
    }
]

Scripts
main.py: The primary extraction script. It takes a PDF file as input and produces a raw, structured JSON file that maps out all the content blocks (text and images) with their positions on the page.

final_processor.py: The parsing and finalization script. It reads the raw data from main.py, intelligently groups the blocks into questions, and formats them into the clean, final JSON structure.
