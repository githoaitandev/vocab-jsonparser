import json
import random
import re
import datetime
import streamlit as st

# Export JSON to file and display result
def json_exporter(vocabDict: dict):
    try:
        vocabJsonParsed = json.dumps(vocabDict, ensure_ascii=False, indent=2)
        # with open("./data/output.json", "w", encoding="utf-8") as f:
        #     f.write(vocabJsonParsed)
    except Exception as e:
        raise Exception(f"Error while exporting JSON: {e}")
    else:
        st.title("Your JSON Result")
        st.write(json.loads(vocabJsonParsed))
        return True

# Remove special characters from text
def remove_special_characters(text: str):
    text = re.sub(r"^[\s•\-\*\t\u2022]+", "", text).strip()
    text = re.sub(r"[\t\r\f\v]", " ", text)
    text = re.sub(r"\n", ":", text)
    text = re.sub(r"[^\w :]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Process paragraphs into structured data
def paragraphs_processing(content: str):
    target_fields = {"Title", "Context", "Vocabularies"}
    split_content = re.split(r'(Title|Context|Vocabularies)', content)
    english_dict = {
        "id": random.randint(100000000, 9999999999),
        "date": datetime.datetime.now().isoformat()
    }

    for i in range(1, len(split_content), 2):
        field = remove_special_characters(split_content[i])
        value = remove_special_characters(split_content[i + 1])
        if field not in target_fields:
            continue
        if field == "Vocabularies":
            cleaned = remove_special_characters(value)
            parts = cleaned.split(":")
            vocab_list = []
            for j in range(0, len(parts) - 1, 2):
                term = remove_special_characters(parts[j])
                definition = remove_special_characters(parts[j + 1])
                if term and definition:  # Bỏ qua nếu trống
                    vocab_list.append({"term": term, "definition": definition})
            english_dict[field.lower()] = vocab_list
        else:
            english_dict[field.lower()] = value.strip()

    # for field in target_fields:
        index = split_content.index(field)
        if field == "Vocabularies":
            preFormat = remove_special_characters(split_content[index + 1])
            vocabsArr = re.split(":", preFormat)
            finalVocabularies = []
            for i in range(0, len(vocabsArr), 2):
                vocabObj = {
                    "term": remove_special_characters(vocabsArr[i]),
                    "meaning": remove_special_characters(vocabsArr[i + 1])
                }
                finalVocabularies.append(vocabObj)
            english_dict[field.lower()] = finalVocabularies
        else:
            english_dict[field.lower()] = split_content[index + 1]

    return english_dict

# Main processor for user input
def main_processor():
    place_holder = '''
        Title
        How to Stay Healthy and Deal with Illness
        Context
        Good health is one of the most valuable things in life...
        Vocabularies
        •	valuable: quý giá, rất quan trọng và hữu ích

    '''
    user_input = st.text_area("Please input your content", height=500, placeholder=place_holder)
    if user_input:
        try:
            englishDict = paragraphs_processing(user_input)
            json_exporter(englishDict)
        except Exception as e:
            st.error(f"An error occurred: {e}")

main_processor()