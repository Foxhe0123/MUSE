from docx import Document  # pip install python-docx
import fitz  # pip install pymupdf
import os
from datetime import datetime
from base import callLLM_with_file ,set_model
from logger_config import get_logger

# Get the configured logger
logger = get_logger()

prompt = (
       "You are a professional article evaluation expert. I will provide you with an introductory article. Your task is to rate the article across multiple quality dimensions. "
        "To ensure fair and differentiated evaluation, your scores must reflect **both strengths and weaknesses** of the article.\n\n"
        "**IMPORTANT SCORING GUIDELINES:**\n"
        "- You must assign different scores across dimensions to reflect the true strengths and weaknesses.\n"
        "- Avoid assigning all scores in the 9–10 range unless the article is near-perfect.\n"
        "- Use the full 0–10 scale if necessary.\n"
        "- Only a flawless performance should receive a 10. A solid but not outstanding section should receive 6–7.\n"
        "- Use 4–5 for mediocre or partially flawed sections, and 3 or below for serious issues.\n"
        "- Do NOT average the individual scores for the overall score. Instead, give an **independent comprehensive score** based on overall impression.\n\n"
        "Respond only with scores in the following format:\n"
        "[Aspect] - [Sub-aspect]: [Score (0–10)]\n\n"
        "Scoring Scale:\n"
        "- 0: Does not meet the criteria at all\n"
        "- 10: Fully meets the criteria with excellence\n\n"
        "Evaluation Criteria:\n\n"
        "Theme\n"
        "- Clarity of Theme: The main theme is clear, understandable, and consistently maintained throughout the article.\n"
        "- Relevance of Chapter Themes: Each section supports the overall goal; chapter-level themes are both independent and coherent.\n"
        "- Theme Coherence: The narrative follows a single logical thread without interruptions or digressions.\n\n"
        "Structure\n"
        "- Structural Integrity: Clear introduction, body, and conclusion; all sections form a unified whole.\n"
        "- Logical Clarity: Logical connections such as cause-effect, general-specific, or temporal order are effectively used.\n"
        "- Structural Coherence: Transitions between sections are smooth and natural; there is a clear hierarchical progression.\n\n"
        "Content\n"
        "- Content Fluency: Sentences and paragraphs read smoothly, with no awkward breaks or tonal shifts.\n"
        "- Richness and Creativity: Includes specific examples, reasoning, or unique insights instead of vague generalizations.\n"
        "- Redundancy and Repetition Control: Content is concise, avoids unnecessary repetition or filler.\n"
        "- Content Accuracy: Factual claims are correct and verifiable; no misleading or false information.\n\n"
        "Writing\n"
        "- Language Style: Clear, reader-friendly, and natural writing, avoiding academic jargon or robotic expressions.\n"
        "- Writing Skills and Rhetoric: Rhetorical tools (e.g., metaphors, parallelism) are used effectively and appropriately.\n"
        "- Accuracy and Standardization: Free from grammar, spelling, and punctuation errors; words are precise and appropriate.\n\n"
        "Overall\n"
        "- Overall Score: Provide a comprehensive score reflecting the article’s overall writing quality and communication effectiveness.\n\n"
        "Your output must follow this format exactly. Do not provide any extra commentary or explanation."
    )

# Read docx file
def read_docx(filepath):
    doc = Document(filepath)
    full_text = [para.text for para in doc.paragraphs]
    return '\n'.join(full_text)

# Read pdf file
def read_pdf(filepath):
    doc = fitz.open(filepath)
    full_text = [page.get_text() for page in doc]
    return '\n'.join(full_text)

def load_file_content(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".docx":
        return read_docx(filepath)
    elif ext == ".pdf":
        return read_pdf(filepath)
    else:
        return None

# General LLM evaluation function
def evaluate_text_with_llm(text):
    response = callLLM_with_file(prompt, text)

    logger.notice(f"Evaluation results:{response}\n")
    return response


def save_evaluation_result(output_path, filename, model_name, result_text):
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(f"file name：{filename}\n")
        f.write(f"Model：{model_name}\n")
        f.write("Evaluation results：\n")
        f.write(result_text + "\n")
        f.write("-" * 40 + "\n")


# 主函数
def evaluate_all_files_in_folder(folder_path,model_name):
    today = datetime.now().strftime("%Y%m%d%H")
    output_file = os.path.join(folder_path, f"evaluate_{today}.txt")

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath) and filepath.lower().endswith(('.docx', '.pdf')):
            logger.notice(f"Processing File: {filename}")
            try:
                text = load_file_content(filepath)
                if text:
                    result = evaluate_text_with_llm(text)
                    save_evaluation_result(output_file, filename, model_name, result)
                else:
                    logger.notice("Unsupported file format, skipping.")
            except Exception as e:
                logger.notice(f"Processing failure:{e}")

if __name__ == "__main__":
    #model_name = "deepseek"
    model_name ="gpt-4o-mini"
    #model_name ="qwen2.5-32b"

    set_model(model_name)
    filepath = "\\test_text\\text-deepseek"
    evaluation_result = evaluate_all_files_in_folder(filepath, model_name)
    logger.notice(evaluation_result)
