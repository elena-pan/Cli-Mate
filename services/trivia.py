import random, openpyxl

def search_trivia():
    questions = []
    wb = openpyxl.load_workbook('trivia.xlsx')
    sheet = wb['Sheet1']

    for row in range(1, sheet.max_row + 1):
        
        if sheet['A' + str(row)].value is None:
            continue

        question = sheet['A' + str(row)].value
        solution = sheet['B' + str(row)].value
        explanation = sheet['C' + str(row)].value

        data = {'question':question, 'solution':solution, 'explanation':explanation}
        questions.append(data)

    num = random.randint(2, len(questions))
    return questions[num-1]
