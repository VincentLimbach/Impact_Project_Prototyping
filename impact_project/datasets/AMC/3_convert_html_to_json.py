import os
from bs4 import BeautifulSoup
import json 

def extract_problems_and_answers():
    base_dir = 'AMC/htmls'
    json_output_dir = 'AMC/jsons'
    os.makedirs(json_output_dir, exist_ok=True)

    all_problems_data = [] 

    for contest in os.listdir(base_dir):
        contest_path = os.path.join(base_dir, contest)
        if not os.path.isdir(contest_path):
            continue  

        problems_file = os.path.join(contest_path, 'problems.html')
        answers_file = os.path.join(contest_path, 'answers.html')
        
        with open(problems_file, 'r', encoding='utf-8') as file:
            problems_soup = BeautifulSoup(file.read(), 'html.parser')
        
        with open(answers_file, 'r', encoding='utf-8') as file:
            answers_soup = BeautifulSoup(file.read(), 'html.parser')
        
        answers = [li.get_text().strip() for li in answers_soup.select('ol li')]

        problems_data = []

        problems = problems_soup.find_all('h2')
        for index, problem in enumerate(problems[1:26]):
            problem_setup_paragraph = problem.find_next_sibling('p')
            for img in problem_setup_paragraph.find_all('img'):
                alt_text = img['alt']
                img.replace_with(alt_text)
            problem_text = problem_setup_paragraph.get_text().strip()

            problem_options_paragraph = problem_setup_paragraph.find_next_sibling('p')
            for img in problem_options_paragraph.find_all('img'):
                alt_text = img['alt']
                img.replace_with(alt_text)
            problem_options = problem_options_paragraph.get_text().strip()

            problem_answer = answers[index] if index < len(answers) else 'Unknown'

            problem_details = {
                'Index': index + 1,
                'Setup': problem_text,
                'Options': problem_options,
                'Answer': problem_answer
            }
            problems_data.append(problem_details)
            problem_details["Index"]=len(all_problems_data)+1
            all_problems_data.append(problem_details)

        json_file_path = os.path.join(json_output_dir, f"{contest}.json")
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(problems_data, json_file, indent=4)

    with open(os.path.join(json_output_dir, 'all_contests.json'), 'w', encoding='utf-8') as json_file:
        json.dump(all_problems_data, json_file, indent=4)

if __name__ == "__main__":
    extract_problems_and_answers()
