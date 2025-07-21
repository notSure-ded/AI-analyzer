import fitz 
import os
import json
from PIL import Image
import io
import argparse 
import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_directories(output_dir: str) -> str:
    """Creates the output and image directories if they don't exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created directory: {output_dir}")
    image_output_dir = os.path.join(output_dir, "images")
    if not os.path.exists(image_output_dir):
        os.makedirs(image_output_dir)
        logging.info(f"Created directory: {image_output_dir}")
    return image_output_dir

def extract_text_spans(page: fitz.Page) -> list:
    """Extracts all text spans from a page."""
    spans = []
    text_dict = page.get_text("dict")
    for block in text_dict.get('blocks', []):
        if block['type'] == 0:  # Text block
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    span_text = span.get('text', '').strip()
                    if span_text:
                        spans.append({
                            "type": "text",
                            "content": span_text,
                            "bbox": list(span["bbox"])
                        })
    return spans

def extract_and_save_images(page: fitz.Page, doc: fitz.Document, page_num: int, output_dir: str, image_output_dir: str) -> list:
    """Extracts all images from a page and saves them."""
    images = []
    for img_index, img_info in enumerate(page.get_images(full=True)):
        try:
            xref = img_info[0]
            img_bbox = page.get_image_bbox(img_info)
            image_filename = f"page_{page_num + 1}_image_{img_index + 1}.png"
            relative_image_path = os.path.join("images", image_filename)
            
            images.append({
                "type": "image",
                "path": relative_image_path,
                "bbox": list(img_bbox)
            })

         
            base_image = doc.extract_image(xref)
            image = Image.open(io.BytesIO(base_image["image"]))
            full_image_path = os.path.join(output_dir, relative_image_path)
            image.save(full_image_path, "PNG")
        except Exception as e:
            logging.warning(f"Could not process image on page {page_num + 1}, index {img_index}. Error: {e}")
    return images

def main(pdf_path: str, output_dir: str):
    """
    Main function to orchestrate the PDF content extraction process.
    """
    logging.info(f"Starting extraction for PDF: {pdf_path}")
    image_output_dir = setup_directories(output_dir)

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        logging.error(f"Failed to open PDF file: {e}")
        return

    all_pages_data = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        text_blocks = extract_text_spans(page)
        image_blocks = extract_and_save_images(page, doc, page_num, output_dir, image_output_dir)
        
        all_blocks = text_blocks + image_blocks
        all_blocks.sort(key=lambda b: b['bbox'][1])
        
        all_pages_data.append({
            "page_number": page_num + 1,
            "blocks": all_blocks
        })
        logging.info(f"Processed Page {page_num + 1}/{len(doc)}")

   
    json_output_path = os.path.join(output_dir, "structured_content.json")
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(all_pages_data, f, indent=4, ensure_ascii=False)

    logging.info(f"✅ Extraction complete! Structured JSON file saved to: {json_output_path}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extract text and images from a PDF file.")
    parser.add_argument("pdf_file", help="The path to the input PDF file.")
    parser.add_argument("-o", "--output", default="pdf_structured_output", help="The directory to save output files (default: pdf_structured_output).")
    
    args = parser.parse_args()

    if os.path.exists(args.pdf_file):
        main(args.pdf_file, args.output)
    else:
        logging.error(f"Error: The file '{args.pdf_file}' was not found.")