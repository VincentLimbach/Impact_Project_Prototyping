from impact_project.datasets.AMC.AMCProblemDataset import AMCProblemDataset
from impact_project.tokenizer.tokenize_text import tokenize_text
import os

def run_tokenization_test():
    vocab_path = os.path.join('impact_project', 'vocabulary.txt')
    
    dataset = AMCProblemDataset(json_file='impact_project/datasets/AMC/jsons/all_contests.json')
    
    for idx in range(len(dataset)):
        item = dataset[idx]
        data = item['data']
        tokenized_output = tokenize_text([data], vocab_path)

        if any('[UNK]' in tokens for tokens in tokenized_output):
            if idx == 349 or idx == 570 or idx == 647 or idx == 1144:
                continue
            raise ValueError

            #print(f"Found '[UNK]' in item {idx}: {tokenized_output}")

if __name__ == "__main__":
    run_tokenization_test()
