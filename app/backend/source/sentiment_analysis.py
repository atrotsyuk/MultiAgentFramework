from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd

def get_sentiment_nltk(df):
    nltk.download('vader_lexicon')

    sia = SentimentIntensityAnalyzer()

    df['sentiment'] = df['answer'].apply(lambda x: sia.polarity_scores(x))
    df = pd.concat([df.drop(['sentiment'], axis=1), df['sentiment'].apply(pd.Series)], axis=1)
    return df


from edsl import QuestionFreeText
def get_sentiment_LLM(df, model):
    sentiment_q = QuestionFreeText(
        question_text = """
You are a political discourse analyst. 
Analyze the **sentiment** of this statement:
"{{ statement }}"
        """
    )
