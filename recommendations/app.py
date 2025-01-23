import pandas as pd
import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import random
from sentiment_label import analyze_sentiment

# Updated dictionary without duplicates
reference_details = {
    'Wellness': [
        ('spa', 'spa treatments'),
        ('massage', 'massage services'),
        ('fitness', 'fitness center')
    ],
    'Entertainment': [
        ('karaoke', 'karaoke nights'),
        ('dj', 'DJ sets'),
        ('theater', 'theater performances')
    ],
    'Dining': [
        ('restaurant', 'restaurant dining'),
        ('bar', 'bar/lounge'),
        ('breakfast', 'breakfast options')
    ],
    'Social Activities': [
        ('board_games', 'board game nights'),
        ('social_events', 'social events'),
        ('pub_crawl', 'pub crawls')
    ]
}

# Load dataset
data = pd.read_csv("mydataset.csv")  # Replace with your dataset path
print(data.head())

reshaped_data = pd.melt(
    data,
    id_vars=['Review', 'Rating', 'reviewed_by', 'user_email'],
    value_vars=['Wellness', 'Entertainment', 'Dining', 'Social Activities'],
    var_name='category',
    value_name='activities'
)
activities_data = reshaped_data.groupby('category')['activities'].unique().to_dict()

# Generate user data
def generate_user_data(data, num_users=100, num_days=30):
    random.seed(42)
    user_data = []
    start_date = datetime.now() - timedelta(days=num_days)
    data_subset = data.head(num_users)
    user_info = data_subset[['reviewed_by', 'user_email']].drop_duplicates()
    user_dict = user_info.to_dict(orient='records')

    for user_details in user_dict:
        name = user_details['reviewed_by']
        email = user_details['user_email']

        for category, activities in activities_data.items():
            for activity in activities:
                if random.random() > 0.3: 
                    user_data.append({
                        'name': name,
                        'category': category,
                        'activity': activity,
                        'rating': random.randint(1, 5),
                        'time_spent': random.randint(30, 180),
                        'email': email
                    })

    return pd.DataFrame(user_data)

user_data_df = generate_user_data(data, num_users=200, num_days=30)


def build_user_profiles(data):
    user_profiles = data.pivot_table(
        index='name',
        columns='activity',
        values='rating',
        aggfunc='mean'
    ).fillna(0)

    time_spent_profile = data.pivot_table(
        index='name',
        columns='activity',
        values='time_spent',
        aggfunc='mean'
    ).fillna(0)

    time_spent_profile = time_spent_profile / time_spent_profile.max()
    user_profiles = (user_profiles * 0.7) + (time_spent_profile * 0.3)
    similarity_matrix = cosine_similarity(user_profiles)
    return similarity_matrix, user_profiles

similarity_matrix, user_profiles = build_user_profiles(user_data_df)


def get_similar_users(data, user_id, n=5, similarity_matrix=None):
    if similarity_matrix is None:
        similarity_matrix, user_profiles = build_user_profiles(data)

    user_idx = user_profiles.index.get_loc(user_id)
    user_similarities = similarity_matrix[user_idx]
    similar_user_indices = user_similarities.argsort()[::-1][1:n+1]
    similar_users = user_profiles.index[similar_user_indices]
    return similar_users

def get_recommendations(data, name, category=None, n=5):
    similar_users = get_similar_users(data, name)
    similar_users_data = data[data['name'].isin(similar_users)]

    if category:
        similar_users_data = similar_users_data[
            similar_users_data['category'] == category
        ]

    recommendations = similar_users_data.groupby('activity').agg({
        'rating': 'mean',
        'time_spent': 'mean'
    }).sort_values('rating', ascending=False)

    user_activities = set(data[data['name'] == name]['activity'])
    new_activities = recommendations[~recommendations.index.isin(user_activities)]
    return new_activities.head(n)


# Streamlit app
def main():
    st.title("The Grand Hotel Recommendations System")

    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False
    if "recommendations_generated" not in st.session_state:
        st.session_state.recommendations_generated = False

    user_name = st.text_input("Enter your name:")
    selected_category = st.selectbox("Select Category", 
                                     ['Wellness', 'Entertainment', 'Dining', 'Social Activities'])

    if st.button("Get Recommendations"):
        if user_name:
            try:
                recommendations = get_recommendations(user_data_df, user_name, category=selected_category)
                st.session_state.recommendations_generated = True
                st.session_state.recommendations = recommendations
            except KeyError:
                st.error("User not found in the dataset.")

    if st.session_state.recommendations_generated:
        st.header(f"Recommendations for {user_name} in {selected_category}")
        recommendations = st.session_state.recommendations

        if not recommendations.empty:
            st.write("**Here are some recommended activities for you:**")
            for index, row in recommendations.iterrows():
                st.write(f"- Try **{index}**! It's a great option with an average rating of {row['rating']:.1f} "
                         f"and users typically spend around {row['time_spent']:.0f} minutes enjoying it.")

            feedback = st.text_area("Please share your feedback about your recent experience:", height=100)
            if st.button("Submit Feedback"):
                if feedback:
                    sentiment = analyze_sentiment(feedback)
                    st.session_state.feedback_submitted = True
                    st.session_state.feedback = feedback
                    st.session_state.sentiment = sentiment

        else:
            st.write("No recommendations found for the selected category.")

    if st.session_state.feedback_submitted:
        sentiment = st.session_state.sentiment
        if sentiment == "positive":
            st.success("We're glad you enjoyed your experience! Thanks for sharing your feedback.")
        elif sentiment == "negative":
            st.error("We're sorry to hear you had a negative experience. "
                     "Please tell us more about how we can improve.")
        else:
            st.info("Thanks for your feedback!")

if __name__ == "__main__":
    main()
