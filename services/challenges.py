import random, openpyxl

def search_challenges():
    challenges = []
    wb = openpyxl.load_workbook('challenges.xlsx')
    sheet = wb['Sheet1']

    for row in range(1, sheet.max_row + 1):
        
        if sheet['A' + str(row)].value is None:
            continue

        challenge = sheet['A' + str(row)].value
        carbon = sheet['B' + str(row)].value
        water = sheet['C' + str(row)].value
        money = sheet['D' + str(row)].value

        data = {'challenge':challenge, 'carbon':carbon, 'water':water, 'money':money}
        challenges.append(data)

    num = random.randint(2, len(challenges))
    return challenges[num-1]
