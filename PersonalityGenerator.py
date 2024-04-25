import random


class ComprehensivePersonality:
    def __init__(self):
        self.big_five_traits = {
            'Openness to experience': (0, 10),
            'Conscientiousness': (0, 10),
            'Extraversion': (0, 10),
            'Agreeableness': (0, 10),
            'Neuroticism': (0, 10)
        }
        self.music_genres = ["pop", "rock", "country", "jazz", "classical"]
        self.hobbies = ["reading", "playing sports", "drawing", "traveling", "coding"]
        self.talk_tones = ["angsty", "happy", "neutral", "positive", "ironic"]
        self.book_genres = ["fantasy", "biography", "mystery", "poetry", "history"]
        self.movie_genres = ["action", "horror", "romance", "drama", "science fiction"]
        self.political_inclinations = ["conservative", "liberal", "libertarian", "socialist", "moderate"]

    def generate_profile(self):
        profile = {
            "Big Five Traits": {trait: random.randint(range_[0], range_[1]) for trait, range_ in self.big_five_traits.items()},
            "Music Preference": random.choice(self.music_genres),
            "Hobby": random.choice(self.hobbies),
            "Talk Tone": random.choice(self.talk_tones),
            "Book Preference": random.choice(self.book_genres),
            "Movie Preference": random.choice(self.movie_genres),
            "Political Inclination": random.choice(self.political_inclinations)
        }
        return profile


class ExpandedComprehensivePersonality(ComprehensivePersonality):
    def __init__(self):
        super().__init__()
        self.cuisine_types = ["Italian", "Chinese", "Mexican", "Indian", "Thai", "French"]
        self.exercise_preferences = ["Yoga", "Running", "Weightlifting", "Swimming", "Cycling", "Dancing"]
        self.travel_preferences = ["Beach", "City", "Countryside", "Mountains", "Desert", "Forest"]
        self.learning_styles = ["Visual", "Aural", "Verbal", "Physical", "Logical", "Social", "Solitary"]
        self.fashion_styles = ["Casual", "Classic", "Trendy", "Grungy", "Bohemian", "Athletic"]
        self.social_media_platforms = ["Facebook", "Instagram", "Twitter", "Snapchat", "Reddit", "LinkedIn"]
        self.times_of_day = ["Morning", "Afternoon", "Evening", "Night"]
        self.climates = ["Tropical", "Dry", "Temperate", "Continental", "Polar"]
        self.financial_attitudes = ["Saver", "Spender", "Investor", "Generous", "Frugal", "Indifferent"]

    def generate_profile(self):
        profile = super().generate_profile()
        profile.update({
            "Favorite Cuisine": random.choice(self.cuisine_types),
            "Exercise Preference": random.choice(self.exercise_preferences),
            "Travel Preference": random.choice(self.travel_preferences),
            "Learning Style": random.choice(self.learning_styles),
            "Fashion Style": random.choice(self.fashion_styles),
            "Social Media Preference": random.choice(self.social_media_platforms),
            "Preferred Time of Day": random.choice(self.times_of_day),
            "Preferred Climate": random.choice(self.climates),
            "Financial Attitude": random.choice(self.financial_attitudes)
        })
        return profile


class RoleBasedPersonality(ExpandedComprehensivePersonality):
    def __init__(self):
        super().__init__()
        self.roles = ["The Hero", "The Mother", "The Child", "The Wise Old Man", "The Trickster", "The Villain","The Lover","The Scapegoat"]

    def generate_profile(self):
        role = random.choice(self.roles)
        profile = super().generate_profile()

        if role == "The Hero":
            profile["Big Five Traits"]["Extraversion"] += 2
            profile["Big Five Traits"]["Conscientiousness"] += 2
        elif role == "The Mother":
            profile["Big Five Traits"]["Agreeableness"] += 2
        elif role == "The Child":
            profile["Big Five Traits"]["Neuroticism"] -= 2
        elif role == "The Wise Old Man":
            profile["Big Five Traits"]["Openness to experience"] += 2
        elif role == "The Trickster":
            profile["Big Five Traits"]["Conscientiousness"] -= 2
        elif role == "The Villain":
            profile["Big Five Traits"]["Agreeableness"] -= 2
        elif role == "The Lover":
            profile["Big Five Traits"]["Extraversion"] += 2
        elif role == "The Scapegoat":
            profile["Big Five Traits"]["Neuroticism"] += 2

        profile["Role"] = role
        
        return profile

if __name__ == "__main__":
    role_based_personality_instance = RoleBasedPersonality()
    role_based_personality_profile = role_based_personality_instance.generate_profile()

    # Print the generated profile
    for k, v in role_based_personality_profile.items():
        print(f"{k}: {v}")
        
    # Extract individual traits
    big_five_traits = role_based_personality_profile['Big Five Traits']
    political_inclination = role_based_personality_profile['Political Inclination']

    # You can now use these individual traits as you wish.
    print(big_five_traits)
    print(political_inclination)