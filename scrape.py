import openai
import re
import argparse
from tqdm import tqdm
import os
import json
import numpy as np
from datetime import datetime
import torch
from collections import defaultdict
import torch.nn.functional as F
import torch
from PIL import Image
from transformers import CLIPModel, CLIPTokenizer, CLIPProcessor
import torch
from typing import Any, Callable, Dict, List, Optional, Union
from transformers import AutoTokenizer, BertModel
import torch
import pandas as pd
import numpy as np
from tqdm import tqdm
import csv 
from pycocotools.coco import COCO
from sentence_transformers import SentenceTransformer
import argparse

parser = argparse.ArgumentParser(description="Scraping from corpus data with steering (optional)")
    
parser.add_argument("--steer", type=str, default = "self-driving cars", help="Steering direction for the self-driving car")
parser.add_argument("--corpus_data", type=str, default = "MS-COCO", help="Corpus data to scrape")
parser.add_argument("--num_output", type=int, default = 150, help="Number of entries we want")
parser.add_argument("--api_key", type=str, default = "", help="API Key for openAI account")
parser.add_argument("--do_steer", action=argparse.BooleanOptionalAction, default=False, help="do_steer")

# Erik, your api_key
openai.api_key = args.api_key

# Define a function to query the OpenAI API and evaluate the answer
def get_yes_no_answer(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        #engine="gpt-3.5-turbo",
        prompt=f'Please respond with either "yes" or "no" to the following: {question}',
        max_tokens=3,
        n=1,
        stop=None,
        temperature=0.2,
    )

    answer = response.choices[0].text.strip()
    yes_no_regex = re.compile(r"^(yes|no)$", re.IGNORECASE)

    if yes_no_regex.match(answer):
        return answer.lower()
    else:
        return "Could not determine yes or no."


def load_bert_model():

    bert_model = SentenceTransformer('paraphrase-distilroberta-base-v1')

    return bert_model

def load_snli():
    # Define the path to the dataset file
    snli_train_file = "snli_1.0/snli_1.0_train.jsonl"
    snli_dev_file = "snli_1.0/snli_1.0_dev.jsonl"
    snli_test_file = "snli_1.0/snli_1.0_test.jsonl"
    
    # Read the dataset files using pandas
    train_data = pd.read_json(snli_train_file, lines=True)
    dev_data = pd.read_json(snli_dev_file, lines=True)
    test_data = pd.read_json(snli_test_file, lines=True)
    
    # Remove rows with '-' label (no label assigned)
    train_data = train_data[train_data['gold_label'] != '-']
    dev_data = dev_data[dev_data['gold_label'] != '-']
    test_data = test_data[test_data['gold_label'] != '-']
    # Collect all premises in the datasets
    train_premises = train_data['sentence1'].tolist()
    dev_premises = dev_data['sentence1'].tolist()
    test_premises = test_data['sentence1'].tolist()
    
    # Combine the premises from all splits
    all_premises = train_premises + dev_premises + test_premises
    
    # Remove duplicates if needed
    unique_premises = list(set(all_premises))
    
    return unique_premises


def load_captions(annotations_path):
    # Initialize COCO API
    coco = COCO(annotations_path)

    # Get all image IDs
    img_ids = coco.getImgIds()

    # Loop through all image IDs and get their captions
    all_captions = []
    for img_id in img_ids:
        ann_ids = coco.getAnnIds(imgIds=img_id)
        anns = coco.loadAnns(ann_ids)
        img_captions = [ann['caption'].lower() for ann in anns]
        all_captions.extend(img_captions)

    return all_captions

def load_coco():
    # Set the paths to the dataset and annotations files
    data_dir = 'coco_annotation'
    annotations_train_path = os.path.join(data_dir, 'captions_train2017.json')
    annotations_val_path = os.path.join(data_dir, 'captions_val2017.json')

    # Load captions for both training and validation sets
    all_captions_train = load_captions(annotations_train_path)
    all_captions_val = load_captions(annotations_val_path)

    # Combine both lists of captions
    all_captions = all_captions_train + all_captions_val

    print(f"Total number of captions (train): {len(all_captions_train)}")
    print(f"Total number of captions (val): {len(all_captions_val)}")
    print(f"Total number of captions (train + val): {len(all_captions)}")

    return all_captions

def load_clip_model():

    # Load the pre-trained CLIP model
    model = CLIPModel.from_pretrained('openai/clip-vit-large-patch14')
    model = model.cuda()

    # Load the corresponding tokenizer
    tokenizer = CLIPTokenizer.from_pretrained('openai/clip-vit-large-patch14')
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

    return model, tokenizer, processor

def write_unique_rows(row, writer):
    """
    Write unique rows to a CSV file, ignoring any rows that have already been written.
    """

    # Define a key as a tuple of the values in row[2] and row[3]
    key1 = (row[2], row[3])
    key2 = (row[0], row[1])
    key3 = (row[1], row[0])



    # Check if the key is already in the set, and write the row if it is not
    if (key1 not in unique_rows) and (key2 not in unique_rows) and (key3 not in unique_rows):
        unique_rows.add(key1)
        unique_rows.add(key2)
        unique_rows.add(key3)
        
        writer.writerow(row)

        return True
    return False
     

def scrape(clip_model, tokenizer, bert_model, premises, similarity_threshold = 0.9):

    num_premises = len(premises)
    batch_size = 1024
    
    # Compute the embeddings for each batch of premises
    bert_text_embeds_prompts = []
    for i in tqdm(range(0, len(premises), batch_size)):
        premises_batch = premises[i:i+batch_size]
        with torch.no_grad():
            text_embeds_prompts_batch = bert_model.encode(premises_batch)
    
        text_embeds_prompts_batch = torch.from_numpy(text_embeds_prompts_batch)
        text_embeds_prompts_batch = F.normalize(text_embeds_prompts_batch, dim=1)

        #text_embeds_prompts_batch = F.normalize(text_embeds_prompts_batch, dim=1)
        bert_text_embeds_prompts.append(text_embeds_prompts_batch)

    # Concatenate the embeddings for all batches
    bert_text_embeds_prompts = torch.cat(bert_text_embeds_prompts, dim=0)


    # split the premises into batches
    premises_batches = [premises[i:i+batch_size] for i in range(0, num_premises, batch_size)]

    # compute the embeddings for each batch of premises
    text_embeds_prompts = torch.zeros(num_premises, 768)
    for i, premises_batch in enumerate(tqdm(premises_batches)):
        tok = tokenizer(premises_batch, return_tensors="pt", padding=True, truncation=True)
        
        for key in tok.keys():
            tok[key] = tok[key].cuda()
        with torch.no_grad():
            text_outputs = clip_model.text_model(**tok)
        text_embeds = text_outputs[1]
        text_embeds = clip_model.text_projection(text_embeds)
        text_embeds_prompt = F.normalize(text_embeds, dim=1)
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, num_premises)
        text_embeds_prompts[start_idx:end_idx, :] = text_embeds_prompt 

    # Initialize an empty list to store similar pairs
    similar_pairs = []

    # Move the text embeddings to the GPU
    text_embeds_prompts = text_embeds_prompts.cuda()
    bert_text_embeds_prompts = bert_text_embeds_prompts.cuda()

    # Iterate over batches of embeddings
    for i in tqdm(range(0, len(premises), batch_size)):
        batch_premises = premises[i:i+batch_size]
        batch_text_embeds_prompts = text_embeds_prompts[i:i+batch_size]
        bert_batch_text_embeds_prompts = bert_text_embeds_prompts[i:i+batch_size]
        
        # Compute the dot product between each pair of embeddings in the batch
        similarity_matrix = torch.matmul(batch_text_embeds_prompts, text_embeds_prompts.t())
        bert_similarity_matrix = torch.matmul(bert_batch_text_embeds_prompts, bert_text_embeds_prompts.t())
       
        mask = (similarity_matrix > similarity_threshold) & (abs(similarity_matrix - bert_similarity_matrix) > 0.2)

        # Find the indices of the matching pairs
        j_indices, k_indices = mask.nonzero(as_tuple=True)

        # Collect the matching pairs and their similarity scores

        for j, k in zip(j_indices.tolist(), k_indices.tolist()):
            similarity_score = similarity_matrix[j, k].item()
            bert_similarity_score = bert_similarity_matrix[j, k].item()
            similar_pairs.append((batch_premises[j], premises[k], similarity_score, bert_similarity_score, similarity_score-bert_similarity_score))
        
   
    # Write similar pairs to a CSV file
    file_path = f'similar_premises_top{args.num_output}_do_steer{args.do_steer}_steer{args.steer}.csv'
    with open(file_path, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Sample 1', 'Sample 2', 'Similarity Score', 'Bert Score'])

        negative_keywords = ["there is no", "unable", "does not", "do not", "am not", "no image", "no picture"]

        similar_pairs.sort(key=lambda x: x[2], reverse=True)

        num_written = 1

        for pair in tqdm(similar_pairs):

            # Check if none of the negative keywords are present in the row
            if not any(keyword in field for field in pair[:2] for keyword in negative_keywords):

                # Ask your yes-no question
                prompt1, prompt2 = pair[0], pair[1]
                
                if args.do_steer:

                    question = f'Is the difference between "{prompt1}" and "{prompt2}" important for {args.steer}?'
                    answer = get_yes_no_answer(question)
                    #print(question)
                    #print(answer)

                    if answer == "yes":
                        # Write the unique row to the output file
                        is_unique = write_unique_rows(pair, csv_writer)
                        if is_unique:
                            num_written += 1

                        if num_written == args.num_output:
                            print("I finished!")
                            exit()
                else:
                    is_unique = write_unique_rows(pair, csv_writer)
                        if is_unique:
                            num_written += 1

                        if num_written == args.num_output:
                            print("I finished!")




if __name__ == '__main__':
    
    args = parser.parse_args()

    model, tokenizer, processor = load_clip_model()
    bert_model = load_bert_model()

    if args.corpus_data == "SNLI":
        unique_premise = load_snli()
    else: 
        unique_premise = load_coco()


    scrape(model, tokenizer, bert_model, unique_premise)
  

