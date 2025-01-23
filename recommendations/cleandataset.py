import pandas as pd
import numpy as np
import faker
import random
from collections import defaultdict

data = pd.read_csv(r"tripadvisor_hotel_reviews.csv")
print(data.head())
print(data.isnull().sum())
fake = faker.Faker()
data['reviewed_by'] = [fake.name() for _ in range(len(data))]


email_counts = defaultdict(int)

def generate_email(name):
    if pd.notnull(name):  
        clean_name = name.lower().replace(" ", ".") 
        email_counts[clean_name] += 1 
        return f"{clean_name}{email_counts[clean_name]}@ex.com"
    return "None@ex.com"  

data['user_email'] = data['reviewed_by'].apply(generate_email)
print(data.head())


preference_columns = [ 'Wellness','Entertainment','Dining','Social Activities']
for column in preference_columns:
    data[column] = 'None'
print("DONE")

preference_details = {
    'Wellness': [
        ('spa', 'spa treatments'), 
        ('massage', 'massage services'), 
        ('fitness', 'fitness center') 
    ],
    'Entertainment': [
        ('live_music', 'live music'), 
        ('dj', 'DJ sets'), 
        ('karaoke', 'karaoke nights') 
    ],
    'Dining': [
        ('restaurant', 'restaurant dining'), 
        ('bar', 'bar/lounge'), 
        ('breakfast', 'breakfast options') 
    ],
    'Social Activities': [
        ('live_music', 'live music'), 
        ('social_events', 'social events'), 
        ('group_activities', 'group activities') 
    ]
}


def add_preferences(row):
    for column, keywords in preference_details.items():
        
        for keyword, detail in keywords:
            if keyword in str(row['Review']).lower() :
                row[column] = detail  
                break
       
        if row[column] == 'None':
            row[column] = 'Not Specified'
    return row

data = data.apply(add_preferences, axis=1)





data.to_csv("mydataset.csv", index=False)

df= pd.read_csv("mydataset.csv")

print(df.columns)
print(df.head())


