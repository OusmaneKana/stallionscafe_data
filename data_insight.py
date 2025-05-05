# app.py
import streamlit as st
from data_processing import process_attendance_data, get_summary, get_popular_meals, get_student_summary
from mongo_connection import get_meal_attendance_data, get_meal_plan_data
from datetime import datetime, timedelta

def get_current_week_dates():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    return start_of_week.date(), end_of_week.date()

current_week_start, current_week_end = get_current_week_dates()


# Load data
st.title("Weekly Meal Attendance Summary")

# Fetch data from MongoDB
attendance_data = get_meal_attendance_data()
meal_plan_data = get_meal_plan_data()



# Check if data is available
if not attendance_data.empty:
    # Process data
    attendance_data = process_attendance_data(attendance_data)

    # Filters
    student_ids = attendance_data['student_id'].unique()
    meals = attendance_data['meal_name'].unique()
    date_range = [attendance_data['punch_time'].min().date(), attendance_data['punch_time'].max().date()]

    selected_student = st.selectbox("Select Student ID", options=['All'] + list(student_ids))
    selected_meal = st.selectbox("Select Meal", options=['All'] + list(meals))
    # selected_date_range = st.date_input("Select Date Range", value=date_range, min_value=date_range[0], max_value=date_range[1])
    selected_start_date = st.date_input("Select Start Date", value=current_week_start)
    selected_end_date = st.date_input("Select End Date", value=current_week_end)

    


    # Apply filters
    filtered_data = attendance_data.copy()
    if selected_student != 'All':
        filtered_data = filtered_data[filtered_data['student_id'] == selected_student]
    if selected_meal != 'All':
        filtered_data = filtered_data[filtered_data['meal_name'] == selected_meal]
    filtered_data = filtered_data[
        (filtered_data['punch_time'].dt.date >= selected_start_date) &
        (filtered_data['punch_time'].dt.date <= selected_end_date)
    ]

    #Summary Data
    popular_meals_df = get_popular_meals(filtered_data)

    student_summary_df = get_student_summary(filtered_data)

    student_summary_df['student_id'] = student_summary_df['student_id'].astype(str)
    meal_plan_data['_id'] = meal_plan_data['_id'].astype(str)

    student_summary_df = student_summary_df.merge(
    meal_plan_data[['_id', 'first_name', 'last_name']],
    left_on='student_id',
    right_on='_id',
    how='left'
        ).drop(columns=['_id'])  # optionally drop '_id' after merge

    print(student_summary_df)

    #Display

    left, middle, right = st.columns(3)

    # Summary
    st.header("Detailed Insight")
    
  
    left.metric("Total Meals",len(filtered_data))

    max_meal_name = popular_meals_df.loc[popular_meals_df['count'].idxmax(), 'meal_name']
    max_meal_count = popular_meals_df['count'].max()
    middle.metric("Most Popular Meal",max_meal_name )

    max_meal_attendance_student_id = student_summary_df.loc[student_summary_df['meals_attended'].idxmax(), 'student_id']
    max_attendance = student_summary_df['meals_attended'].max()
    right.metric("Highest Student Attendance", int(max_attendance))




    # # Show the filtered data
    # st.subheader("Filtered Data")
    # st.write(filtered_data)


    left, right = st.columns(2)

    # Summary Tables
    st.subheader("Summary by Student and Meal")
    summary_df = get_summary(filtered_data)
   
    st.write(summary_df)

    right.subheader("Meals Count")
    
    right.write(popular_meals_df)

    left.subheader("Student Meal Attendance Count")
    
    left.write(student_summary_df)

    # Visualization
    if st.checkbox("Show Visualizations"):
        
        st.subheader("Most Popular Meals")
        st.bar_chart(popular_meals_df.set_index('meal_name'))
else:
    st.write("No data available.")
