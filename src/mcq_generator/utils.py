import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFilerReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        
        except Exception as e :
           raise Exception("error in reading the file")

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception("unsupported file format only pdf and text files supported")


def get_table_data(quiz_str):  
    quiz_json_str = quiz_str.split('##Response_JSON')[-1].strip()

    try: 
        #convert striung to dict

         quiz_dict=json.loads(quiz_json_str)
         quiz_table_data=[]

         #iterate over the quiz dict and extract the required info
         for value in quiz_dict["questions"]:
            mcq = value["question"]
            options = " | ".join(
             [
                f"{option}: {option_value}"
                 for option, option_value in value["options"].items()
            ]
        )
            correct = value["correct_answer"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

         return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
    return false    
