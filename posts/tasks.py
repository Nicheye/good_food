def calculate_usefulness(post):
    # Ключевые слова в названии и их весовые коэффициенты
    title_keywords = {
        'органический': 10,
        'обезжиренный': 5,
        'без сахара': 8,
        'много белков': 12,
        
    }

    # Слова в составе и их весовые коэффициенты
    composition_keywords = {
        'сахар': -5,
        'клетчатка': 5,
        'витамины': 5,
        'минералы': 5,
        'искусственный': -8,
        'консерванты': -6,
    }

    # Весовые коэффициенты для БЖУ
    nutrient_weights = {
        'белки': 2,
        'жиры': -1 if post.fats > 10 else 1,
        'углеводы': 1 if post.carbohydrates < 30 else -1,
    }

    # Начальный коэффициент полезности
    usefulness = 0

    # Учет ключевых слов в названии
    for word, score in title_keywords.items():
        if word in post.title.lower():
            usefulness += score

    # Учет состава продукта
    for word, score in composition_keywords.items():
        if word in post.composition.lower():
            usefulness += score

    # Учет содержания БЖУ с учетом веса продукта
    total_weight = post.weight if post.weight > 0 else 1  # Предотвращаем деление на ноль
    usefulness += (post.proteins * nutrient_weights['белки']) / total_weight
    usefulness += (post.fats * nutrient_weights['жиры']) / total_weight
    usefulness += (post.carbohydrates * nutrient_weights['углеводы']) / total_weight

    
    min_score = 0  
    max_score = 100
    normalized_usefulness = 1 + 9 * (usefulness - min_score) / (max_score - min_score)
    normalized_usefulness = max(1, min(10, normalized_usefulness))  # Ограничение диапазона от 1 до 10

    return round(normalized_usefulness, 2)



