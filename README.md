# Grand Hotel Recommendations System

## Overview
The Grand Hotel Recommendations System is a comprehensive web-based platform designed to enhance guest experiences by providing personalized activity recommendations, collecting and analyzing feedback, and ensuring prompt management responses to guest concerns. The system leverages machine learning algorithms and APIs to analyze guest preferences and sentiment, ensuring a seamless and personalized experience.

---

## Dataset
The system is based on the **Trip Advisor Hotel Reviews dataset**, which contains 20,000 hotel reviews. The dataset is sourced from Kaggle: [Trip Advisor Hotel Reviews Dataset](https://www.kaggle.com/datasets/andrewmvd/trip-advisor-hotel-reviews).

---

## Features

### 1. Personalized Recommendations
- **User Profile Matching**:
  - Guest preferences and historical activity data are stored in a database.
  - Similarity between users is calculated using the **cosine similarity algorithm**, identifying users with overlapping preferences and behaviors.

- **Logic**:
  - Each user is represented as a vector of activity preferences and ratings.
  - Cosine similarity is computed as:
    \[
    \text{similarity}(A, B) = \frac{\text{dot}(A, B)}{\|A\| \|B\|}
    \]
  - Activities highly rated or frequently engaged in by similar users are recommended.

- **Output**:
  - A ranked list of activities based on the aggregated ratings and time spent by similar users.

### 2. Feedback Collection and Sentiment Analysis
- **Feedback Collection**:
  - Guests submit feedback via a form, which is stored in the database.

- **Sentiment Analysis**:
  - Sentiment analysis is performed using the OpenAI API to classify feedback as positive, neutral, or negative.

- **Implementation Details**:
  - The `analyze_sentiment` function sends the feedback text to the OpenAI API for analysis.
  - A retry mechanism (using the `tenacity` library) ensures robust handling of failed API calls, with exponential backoff and up to three retries.
  - To avoid exceeding API rate limits, a delay is introduced between requests.

- **Logic**:
  - Feedback text is sent to the OpenAI API with a tailored prompt for sentiment analysis.
  - The API returns a sentiment label (e.g., "positive," "neutral," or "negative"), which is stored alongside the feedback for further action.

- **Category Detection**:
  - Keywords in the feedback are matched to predefined categories (e.g., "spa" for Wellness, "live music" for Entertainment).
  - Tokenization and keyword mapping are performed using a dictionary or machine-learning classifier.

- **Output**:
  - Sentiment labels and detected categories are stored in the database for further analysis and recommendations.

### 3. Notification Mechanisms
- **Slack Alerts**:
  - Negative feedback triggers a Slack notification via a webhook.
  - The notification includes:
    - Feedback text.
    - Sentiment label.
    - Detected categories.

- **Email Alerts**:
  - Emails are sent using SMTP or third-party APIs (e.g., SendGrid) and include:
    - Guest name and feedback.
    - Sentiment analysis results.
    - Suggested actions based on the feedback.

### 4. Recommendation Algorithm
- **Steps**:
  1. Retrieve guest preferences and activity history from the database.
  2. Identify users with similar preferences using the cosine similarity algorithm.
  3. Aggregate data for each activity, calculating:
     - Average rating by similar users.
     - Average time spent by similar users.
  4. Rank activities based on aggregated ratings and engagement.
  5. Filter out activities already experienced by the guest.
  6. Display recommendations in a user-friendly format (e.g., cards or lists).

---

## Dataset Preparation
- **Initial Dataset**:
  - The original dataset contains 20,000 reviews and ratings.

- **Enhancements**:
  1. **Fake User Information**:
     - A `reviewed_by` column was added with random names generated using the `Faker` library.
  2. **Unique User Emails**:
     - A `user_email` column was added with unique email addresses for each user.
  3. **Preference Columns**:
     - Added columns: `Wellness`, `Entertainment`, `Dining`, and `Social Activities`, initialized to `None`.
  4. **Defining Keywords**:
     - Keywords were mapped to categories, such as:
       - Wellness: "spa," "massage," "fitness."
       - Entertainment: "live music," "karaoke."
       - Dining: "restaurant," "breakfast."
       - Social Activities: "group activities," "events."
  5. **Classifying Reviews**:
     - Reviews were analyzed for keywords, updating the relevant columns with detected preferences or marking them as "Not Specified."
  6. **Saving Enhanced Dataset**:
     - The processed dataset was saved as `mydataset.csv`.

---

## User Interface
### 1. Slack Notifications
- Real-time alerts for negative feedback, providing actionable insights to management.

### 2. Email Notifications
- Detailed summaries of guest feedback and sentiment analysis results.

---

## Future Enhancements
- **Advanced Sentiment Analysis**:
  - Incorporate transformer-based models like BERT or GPT for more nuanced sentiment classification.

- **Real-Time Feedback Processing**:
  - Use message queues (e.g., RabbitMQ, Kafka) for real-time feedback analysis.

- **Improved Recommendation Engine**:
  - Replace cosine similarity with collaborative filtering or neural networks for enhanced accuracy.

---

## Contact
For any inquiries or issues, please contact the development team at `support@grandhotel.com`.

