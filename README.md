

# The Grand Hotel Recommendation System

## Overview
This project implements a user-based recommendation system that suggests activities to users based on their preferences, ratings, and similarities with other users. The system is built using **Python**, **Pandas**, **Streamlit**, and other supporting libraries. It includes features like generating personalized recommendations, analyzing user feedback sentiment, and tracking user preferences.

---

## Features
1. **Activity Recommendation**  
   - Personalized activity recommendations for users based on their preferences and past interactions.  
   - Recommendations are categorized into:
     - Wellness
     - Entertainment
     - Dining
     - Social Activities  

2. **Streamlit Web Interface**  
   - An interactive front-end where users can input their preferences and receive recommendations.

3. **User Similarity**  
   - Calculates similarity between users using **Cosine Similarity** for better recommendations.

4. **Dynamic User Data Generation**  
   - Generate synthetic user data for testing and evaluation.



## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/repository-name.git
   cd repository-name
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your dataset:
   - Replace `mydataset.csv` with your dataset file in the root directory.

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

---

## How to Use
1. **Input Details**:  
   - Enter your name and select a category of interest (e.g., Wellness, Dining, etc.) on the web interface.

2. **Get Recommendations**:  
   - Click on the "Get Recommendations" button to view personalized suggestions.

3. **Provide Feedback**:  
   - Share feedback about your experience, which will be analyzed for sentiment.

4. **View Recommendations**:  
   - See a list of suggested activities along with average ratings and time spent by other users.


## Example Dataset
The dataset should have the following columns:  
- `Review`: Text review by the user.
- `Rating`: Rating given by the user (1-5).
- `reviewed_by`: User's name.
- `user_email`: User's email.
- Categories of interest (e.g., `Wellness`, `Dining`, etc.).


