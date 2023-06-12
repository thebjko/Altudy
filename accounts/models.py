from django.db import models
from django.contrib.auth.models import AbstractUser

emoji_dict = {
    0: '🥚',
    1: '🐣',
    2: '🐥',
    3: '🦎',
    4: '🦕',
    5: '🦖',
}

class User(AbstractUser):
    experience = models.PositiveIntegerField(default=0)

    def get_level(self):
        if self.experience >= 1000:
            return 5
        elif self.experience >= 500:
            return 4
        elif self.experience >= 200:
            return 3
        elif self.experience >= 90:
            return 2
        elif self.experience >= 30:
            return 1
        elif self.experience >= 0:
            return 0
        else:
            return ''

    def get_level(self):
        level = 0
        exp_thresholds = [0, 30, 90, 200, 500, 1000]
        
        for i, threshold in enumerate(exp_thresholds):
            if self.experience >= threshold:
                level = i
        
        return level
    
    def emoji_username(self):
        level = self.get_level()
        emoji = emoji_dict.get(level, '')
        return f'{emoji}{self.username}'

    def emoji(self):
        level = self.get_level()
        emoji = emoji_dict.get(level, '')
        return emoji
    
    def get_progress_percentage(self):
        level = self.get_level()
        current_exp = self.experience
        next_level_exp = self.get_next_level_exp(level)
        
        if level == 5:
            return 100
        else:
            progress_percentage = (current_exp / next_level_exp) * 100
            return progress_percentage
        

    def get_experience_from_level(self):
        level = self.get_level()
        prev_level_exp = self.get_next_level_exp(level -1)
        current_level_exp = self.experience - prev_level_exp
        return current_level_exp


    def get_next_level_exp(self, level):
        exp_thresholds = [0, 30, 90, 200, 500, 1000]

        if level >= 0 and level < len(exp_thresholds) - 1:
            return exp_thresholds[level + 1] - exp_thresholds[level]

        return 0