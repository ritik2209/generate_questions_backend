import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import spacy
from typing import List
from fastapi import HTTPException



ckpt_path = './app/models/checkpoint-11000'
model = AutoModelForSeq2SeqLM.from_pretrained(ckpt_path)


model_checkpoint = "t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)


def run_model(input_string, model, tokenizer, device, **generator_args):
    try:
        input_ids = tokenizer.encode(input_string, return_tensors="pt").to(torch.device(device))
        res = model.generate(input_ids, **generator_args)
        output = tokenizer.batch_decode(res, skip_special_tokens=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred during model generation: {e}")
    return output


def get_entities(text):
    try:
        seen = set()
        entities = []
        spacy_nlp = spacy.load('en_core_web_sm')
        for entity in spacy_nlp(text).ents:
            if entity.text not in seen:
                seen.add(entity.text)
                entities.append(entity)
        return sorted(entities, key=lambda e: e.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while getting entities: {e}")



def generate_question(context, answer):
    try:
        return run_model(f"generate question: {answer} context: {context}", model, tokenizer, 'cpu', max_length=50)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while generating question: {e}")




def generate_questions_from_model(context: str) -> List:
    try:
        seen = set()
        entities = get_entities(context)
        generated_questions = []
        for entity in entities:
            print(entity)
            generated_question = generate_question(context, entity)
            if generated_question[0] not in seen:
                generated_questions.extend(generated_question)
                seen.add(generated_question[0])
        return generated_questions
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error occurred while generating questions: {e}")
