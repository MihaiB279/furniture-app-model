def evaluation(furniture, positions, budget):
    budget_furniture = 0
    for i in range(len(positions)):
        furniture_add = furniture[i][positions[i]]
        budget_furniture = budget_furniture + float(furniture_add['Price'])
    score = abs(budget - budget_furniture)
    return score
