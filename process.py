import json
import os
import re

def parse_and_finalize_questions(input_json_path, output_json_path):
    """
    The definitive script to process structured blocks into a clean, final
    question format. Uses a robust system to correctly differentiate
    question images from option images.
    """
    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_json_path}'.")
        return

    all_blocks = [block for page in data for block in page['blocks']]
    grouped_questions = {}
    current_q_number = None
    q_start_pattern = re.compile(r'^\s*(\d+)\.')
    for block in all_blocks:
        if block['type'] == 'text':
            match = q_start_pattern.match(block['content'])
            if match:
                current_q_number = int(match.group(1))
                if current_q_number not in grouped_questions:
                    grouped_questions[current_q_number] = []
        if current_q_number:
            grouped_questions[current_q_number].append(block)

    final_questions = []
    for q_number, q_blocks in grouped_questions.items():
        
        all_texts = [b['content'] for b in q_blocks if b['type'] == 'text']
        all_images = [b['path'] for b in q_blocks if b['type'] == 'image']
        full_text_content = " ".join(all_texts)

        correct_answer = None
        ans_match = re.search(r'Ans\s*\[\s*([A-D])\s*\]', full_text_content)
        if ans_match:
            correct_answer = ans_match.group(1)
            full_text_content = re.sub(r'Ans\s*\[\s*[A-D]\s*\]', '', full_text_content)
            
       
        option_letters_found = re.findall(r'\[\s*([A-D])\s*\]', full_text_content)
        num_options = len(set(option_letters_found))

        
        question_images = all_images[:-num_options] if num_options > 0 else all_images
        option_images = all_images[-num_options:] if num_options > 0 else []

        
        first_option_match = re.search(r'\[\s*[A-D]\s*\]', full_text_content)
        if first_option_match:
            question_text = full_text_content[:first_option_match.start()]
        else:
            question_text = full_text_content
        
        
        question_text = q_start_pattern.sub('', question_text).strip()
  
        final_options = {}
        option_text_matches = re.findall(r'\[\s*([A-D])\s*\]\s*([^\[]*)', full_text_content)
        for i, (letter, text) in enumerate(option_text_matches):
            final_options[letter] = {"text": text.strip()}
          
            if i < len(option_images):
                final_options[letter]["image"] = option_images[i]
        
  
        final_questions.append({
            "question_number": q_number,
            "question_text": re.sub(r'\s+', ' ', question_text).strip(),
            "question_images": question_images,
            "options": final_options,
            "correct_answer": correct_answer
        })

    final_questions.sort(key=lambda q: q['question_number'])
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(final_questions, f, indent=4)

    print(f"\n✅ Success! Final data saved to '{output_json_path}'")

if __name__ == "__main__":
    input_file = os.path.join("pdf_structured_output", "structured_content.json")
    output_file = os.path.join("pdf_structured_output", "final_questions.json")
    parse_and_finalize_questions(input_file, output_file)