import openai
import csv
import os

api_key = os.getenv('OPENAI_API_KEY', '')
openai.api_base = ""

def chat_with_gpt3_5(messages):
    response = openai.ChatCompletion.create(
        model=" ",
        messages=messages,
        api_key=api_key,
        stream=True
    )

    full_response = ""
    for chunk in response:
        if 'choices' in chunk and len(chunk['choices']) > 0:
            content = chunk['choices'][0].get('delta', {}).get('content', '')
            if content:
                print(content, end='', flush=True)
                full_response += content
    print()
    return full_response


def read_questions_from_csv(file_path, max_lines=10000):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i < max_lines:
                questions.append(row[0])
            else:
                break
    return questions

questions = read_questions_from_csv('')


for question in questions:

    conversation = [
        {
            "role": "system",
            "content": '''
        You are a supply chain expert tasked with evaluating a supplier’s quality level based on four dimensions and 16 criteria. Provide concise, accurate, and format-specific assessments. The key evaluation details are:

        - **Dimensions and Weights**: 
          - Delivery Status: 26.22%
          - Profit Margin: 56.50%
          - Shipping Mode: 11.75%
          - Market: 5.53%

        - **Criteria and Weights**: 
          - Delivery Status: [Advance shipping (12.40%), Shipping on time (4.45%), Late delivery (7.46%), Shipping canceled (1.91%)]
          - Profit Margin: [>1 (28.97%), 0-0.5 (14.77%), -0.5 to 0 (7.29%), -1 to -0.5 (3.58%), < -1 (1.88%)]
          - Shipping Mode: [Standard Class (6.64%), Second Class (3.08%), First Class (1.38%), Same Day (0.65%)]
          - Market: [USCA (2.20%), Europe (1.33%), LATAM (0.95%), Africa (0.65%), Pacific Asia (0.40%)]

        For each dimension, evaluate the ratings (Good, Fair, Average, Poor) based on the criteria, and calculate the overall score by considering the weights.

        **Examples for Reference**:
        1. Supplier: {61712} {Delivery Status}{Advance shipping} {Profit Margin}{0.1690} {Shipping Mode}{Standard Class} {Market}{LATAM}
           - Step 1: Delivery Status: **Advance shipping** is considered a proactive and positive delivery method. The Delivery Rating is **Good**.
           - Step 2: Profit Margin: **0.1690** is positive but low, indicating an **Average** profit margin.
           - Step 3: Shipping Mode: **Standard Class** is reliable, resulting in a **Good** rating.
           - Step 4: Market: **LATAM** market conditions are moderate, so the Market Rating is **Average**.
           - Final Output: Supplier: {61712} {Delivery Status}{Advance shipping} {Delivery Rating}{Good} {Profit Margin}{0.1690} {Profit Margin Rating}{Average} {Shipping Mode}{Standard Class} {Shipping Rating}{Good} {Market}{LATAM} {Market Rating}{Average} Overall Score: {Good}.

        2. Supplier: {75198} {Delivery Status}{Advance shipping} {Profit Margin}{0.2930} {Shipping Mode}{Standard Class} {Market}{USCA}
           - Step 1: Delivery Status: **Advance shipping** is a good indicator of a reliable supplier, so the Delivery Rating is **Good**.
           - Step 2: Profit Margin: **0.2930** is slightly higher than the previous example but still low. The Profit Margin Rating is **Average**.
           - Step 3: Shipping Mode: **Standard Class** is reliable, giving the Shipping Rating a **Good** rating.
           - Step 4: Market: **USCA** is a strong market with good infrastructure and logistics, resulting in a **Good** Market Rating.
           - Final Output: Supplier: {75198} {Delivery Status}{Advance shipping} {Delivery Rating}{Good} {Profit Margin}{0.2930} {Profit Margin Rating}{Average} {Shipping Mode}{Standard Class} {Shipping Rating}{Good} {Market}{USCA} {Market Rating}{Good} Overall Score: {Good}.

        **Output Format**:
        Supplier: {ID} {Delivery Status}{Criterion} {Delivery Rating}{Rating} {Profit Margin}{Value} {Profit Margin Rating}{Rating} {Shipping Mode}{Criterion} {Shipping Rating}{Rating} {Market}{Criterion} {Market Rating}{Rating} Overall Score: {Rating}.
        '''
        },
        {"role": "user", "content": question}
    ]

    print("答: ", end='', flush=True)
    assistant_message = chat_with_gpt3_5(conversation)
    print("\n")


    with open(' ', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Question', 'Answer'])
        writer.writerow({'Question': question, 'Answer': assistant_message})
