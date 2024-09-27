# data_processing.py
import pandas as pd

def process_meal_data(df):
    df['punch_time'] = pd.to_datetime(df['punch_time'], unit='s')
    df['date'] = df['punch_time'].dt.date
    df['time'] = df['punch_time'].dt.strftime('%I:%M %p')
    df['student_id'] = df['student_id'].astype(str)

    # Delete 
    df = df.drop('_id', axis=1)

    df = df.reset_index(drop=True)

    return df

def get_summary(df):
    summary = df.groupby(['student_id', 'meal_name']).size().reset_index(name='count')
    return summary

def get_popular_meals(df):
    popular_meals = df['meal_name'].value_counts().reset_index()
    popular_meals.columns = ['meal_name', 'count']
    return popular_meals

def get_student_summary(df):
    student_summary = df['student_id'].value_counts().reset_index()
    student_summary.columns = ['student_id', 'meals_attended']
    return student_summary
