from collections import Counter
from .models import Like,FoodPost
from django.db.models import Q
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


def get_favorite_category(user):
    liked_posts = Like.objects.filter(liked_by=user)
    categories = [post.post.cat for post in liked_posts]
    favorite_category = Counter(categories).most_common(1)[0][0] if categories else None
    return favorite_category

def recommended_posts(user):
    fav_cat=get_favorite_category(user)
    firstly = FoodPost.objects.filter(cat=fav_cat)
    if user.profile.goal == 'Сушка':
        query = Q(cat='похудение') | Q(cat="спортпит")
        secondly = FoodPost.objects.filter(query)
    elif user.profile.goal == 'Баланс':
        query = Q(cat='здоровье') | Q(cat="анти-Эйджинг")
        secondly = FoodPost.objects.filter(query)
    
    elif user.profile.goal == 'Похудение':
        query = Q(cat='похудение') | Q(cat="веган")
        secondly = FoodPost.objects.filter(query)
    
    elif user.profile.goal == 'Набор':
        query = Q(cat='спортпит') | Q(cat="здоровье") | Q(cat="здоровье")
        secondly = FoodPost.objects.filter(query)
    else:
        secondly = FoodPost.objects.order_by('likes')
    
    thirdly = FoodPost.objects.filter(cat='здоровье')

    final = firstly | secondly | thirdly

    return final
    


