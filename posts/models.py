from django.db import models
from authentification.models import User
import re
import logging
from django.core.cache import cache
import requests
from googletrans import Translator
class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prefers_organic = models.BooleanField(default=True)
    prefers_low_fat = models.BooleanField(default=True)
    prefers_sugar_free = models.BooleanField(default=True)
    prefers_high_protein = models.BooleanField(default=True)

    
class FoodPost(models.Model):
    title = models.CharField(max_length=100)
    composition = models.TextField(max_length=500)
    weight = models.IntegerField(default=0)
    proteins = models.IntegerField(default=0, blank=True)
    fats = models.IntegerField(default=0, blank=True)
    carbohydrates = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ben_koef = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts')
    comments = models.ManyToManyField(User, through='Comment', related_name='comments')
    CAT_CHOICES = (
    ('похудение', 'Похудение'),
    ('спортпит', 'Спортивное питание'),
    ('веган', 'Веганы и Вегетарианцы'),
    ('здоровье', 'Полезно для здоровья'),
    ('анти-Эйджинг', 'Анти-Эйджинг'),
    ('семья', 'Семейное Питание'),
    ('мед', 'Питание при Медицинских Состояниях'),)

    cat = models.CharField(max_length=40, choices=CAT_CHOICES, default='здоровье')
    sugar = models.PositiveIntegerField(default=0)
    calories = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title + " " +str(self.id)
    
    def calculate_usefulness(self, user=None):
        title_keywords = {
            r'\b(органический|organic)\b': 10,
            r'\b(обезжиренный|low fat)\b': 5,
            r'\b(без сахара|sugar-free)\b': 8,
            r'\b(много белков|high protein)\b': 12,
            r'\b(низкокалорийный|low calorie)\b': 7,
            r'\b(без глютена|gluten-free)\b': 6,
            r'\b(веганский|vegan)\b': 8,
            r'\b(натуральный|natural)\b': 5,
            r'\b(низкий гликемический индекс|low glycemic index)\b': 9,
            r'\b(без лактозы|lactose-free)\b': 7
        }

        composition_keywords = {
            r'\b(сахар|sugar)\b': -5,
            r'\b(клетчатка|fiber)\b': 5,
            r'\b(витамины|vitamins)\b': 5,
            r'\b(минералы|minerals)\b': 5,
            r'\b(искусственный|artificial)\b': -8,
            r'\b(консерванты|preservatives)\b': -6,
            r'\b(трансжиры|trans fats)\b': -10,
            r'\b(натрий|sodium)\b': -4,
            r'\b(антиоксиданты|antioxidants)\b': 7,
            r'\b(омега-3|omega-3)\b': 8,
            r'\b(натуральные ингредиенты|natural ingredients)\b': 6,
            r'\b(низкое содержание углеводов|low carb)\b': 5
        }

        nutrient_weights = {
            'белки': 2, 'proteins': 2,
            'жиры': -1 if self.fats > 10 else 1, 'fats': -1 if self.fats > 10 else 1,
            'углеводы': 1 if self.carbohydrates < 30 else -1, 'carbohydrates': 1 if self.carbohydrates < 30 else -1,
            'клетчатка': 5, 'fiber': 5,
            'натрий': -0.1, 'sodium': -0.1,
            'витамины': 3, 'vitamins': 3,
            'минералы': 3, 'minerals': 3,
            'антиоксиданты': 4, 'antioxidants': 4,
            'омега-3': 4, 'omega_3': 4
        }

        category_adjustments = {
            'похудение': 1.2,
            'спортпит': 1.1,
            'веган': 1.0,
            'здоровье': 1.0,
            'анти-Эйджинг': 1.1,
            'семья': 1.0,
            'мед': 1.2,
        }

        # Initial usefulness coefficient
        usefulness = 0

        # Process title keywords with regex
        for pattern, score in title_keywords.items():
            if re.search(pattern, self.title.lower()):
                usefulness += score

        # Process composition keywords with regex
        for pattern, score in composition_keywords.items():
            if re.search(pattern, self.composition.lower()):
                usefulness += score

        # Process nutrients with respect to product weight
        total_weight = self.weight if self.weight > 0 else 1  # Prevent division by zero
        usefulness += (self.proteins * nutrient_weights['белки']) / total_weight
        usefulness += (self.fats * nutrient_weights['жиры']) / total_weight
        usefulness += (self.carbohydrates * nutrient_weights['углеводы']) / total_weight

        # Adjust usefulness based on the category
        usefulness *= category_adjustments.get(self.cat, 1.0)

        # Adjust for user preferences if available
        if user:
            try:
                preferences = user.userpreferences
                if preferences.prefers_organic and 'organic' in self.title.lower():
                    usefulness *= 1.1
                if preferences.prefers_low_fat and 'low fat' in self.title.lower():
                    usefulness *= 1.1
                if preferences.prefers_sugar_free and 'sugar-free' in self.title.lower():
                    usefulness *= 1.1
                if preferences.prefers_high_protein and 'high protein' in self.title.lower():
                    usefulness *= 1.1
            except UserPreferences.DoesNotExist:
                pass  # If user preferences do not exist, continue without adjustment

        # Normalize the usefulness score to a range of 1 to 10
        min_score = 0  
        max_score = 200  # Adjusted based on expanded keyword and nutrient impact
        normalized_usefulness = 1 + 9 * (usefulness - min_score) / (max_score - min_score)
        normalized_usefulness = max(1, min(10, normalized_usefulness))  # Ensure range is between 1 and 10

        return round(normalized_usefulness, 2)


    def calculate_vits(self):
        translator = Translator()
        try:
            # Translate the title from Russian to English
            english_title = translator.translate(self.title, src='ru', dest='en').text
            print(f"Translated title: {english_title}")
        except Exception as e:
            print(f"Error during translation: {e}")
            english_title = self.title  # Fallback to the original title

        url = f"https://api.calorieninjas.com/v1/nutrition?query={english_title}"
        headers = {
            'Accept': 'application/json',
            'x-api-key': 'ge6pl8bAyYTpG/+SH4NnDg==VChXCiPZGmmu3aC4'  # Replace with your actual API key
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            if 'items' in data and len(data['items']) > 0:
    
                total_proteins = 0
                total_fats = 0
                total_carbohydrates = 0
                total_sugar = 0
                total_calories = 0
                
               
                for item in data['items']:
                    proteins = item.get('protein_g', 0)
                    fats = item.get('fat_total_g', 0)
                    carbohydrates = item.get('carbohydrates_total_g', 0)
                    sugar = item.get('sugar_g', 0)
                    calories = item.get('calories', 0)

                    # You can process each item here, for example, print or accumulate totals
                    print(f"Item: {item['name']}, Proteins: {proteins}g, Fats: {fats}g, Carbohydrates: {carbohydrates}g, Sugar: {sugar}g, Calories: {calories}kcal")
                    
                    
                    total_proteins += proteins
                    total_fats += fats
                    total_carbohydrates += carbohydrates
                    total_sugar += sugar
                    total_calories += calories

                # Print or process the totals as needed
               
            else:
                raise ValueError("No items found in response")


        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching nutrition data: {e}")
            proteins = fats = carbohydrates = sugar = calories = 0

        output = {
            'proteins': total_proteins*(self.weight/100),
            'fats': total_fats*(self.weight/100),
            'carbohydrates': total_carbohydrates*(self.weight/100),
            'sugar': total_sugar*(self.weight/100),
            'calories': total_calories*(self.weight/100)
        }
        return output

    def save(self, *args, **kwargs):
    # Fetch nutrition data if not already present
        if not self.proteins or not self.fats or not self.carbohydrates or not self.sugar or not self.calories:
            fetched_data = self.calculate_vits()
            self.proteins = fetched_data['proteins']
            self.fats = fetched_data['fats']
            self.carbohydrates = fetched_data['carbohydrates']
            self.sugar = fetched_data['sugar']
            self.calories = fetched_data['calories']

        # Calculate usefulness before saving
        self.ben_koef = self.calculate_usefulness()
        super().save(*args, **kwargs)
        
        # Cache the usefulness score and track history
        self.cache_usefulness_score()
        self.track_usefulness_history()

    
    def cache_usefulness_score(self):
        cache_key = f'foodpost_{self.id}_usefulness'
        cache.set(cache_key, self.ben_koef, timeout=60*60)
    
    @staticmethod
    def get_cached_usefulness(post_id):
        cache_key = f'foodpost_{post_id}_usefulness'
        return cache.get(cache_key)

    def track_usefulness_history(self):
        UsefulnessHistory.objects.create(food_post=self, usefulness_score=self.ben_koef)

class UsefulnessHistory(models.Model):
    food_post = models.ForeignKey(FoodPost, on_delete=models.CASCADE)
    usefulness_score = models.FloatField()
    calculated_at = models.DateTimeField(auto_now_add=True)
    
class ImagePost(models.Model):
    post = models.ForeignKey(FoodPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')

class Like(models.Model):
    post = models.ForeignKey(FoodPost, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(FoodPost, on_delete=models.CASCADE)
    message = models.CharField(max_length=550)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Bookmark(models.Model):
    post = models.ForeignKey(FoodPost, on_delete=models.CASCADE)
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
