import pandas as pd
import numpy as np


def calculate_demographic_data(print_data=True):
    # Read data from file
    path = 'adult.data.csv'
    df = pd.read_csv(path, header = 0)
    df = df.fillna(0)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = pd.Series(df['race'].value_counts())

    # What is the average age of men?
    table = pd.pivot_table(df, values = 'age', columns=['sex'], aggfunc=np.mean)
    average_age_men = round(table['Male']['age'], 2)

    # What is the percentage of people who have a Bachelor's degree?
    educ = df['education'].value_counts()
    percentage_bachelors = round(educ['Bachelors']/educ.sum()*100, 2)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = educ['Bachelors'] + educ['Masters'] + educ['Doctorate']
    lower_education = educ.sum() - higher_education

    # percentage with salary >50K
    salaries = pd.pivot_table(df, values= 'age' ,columns=['salary'], index=['education'] , aggfunc='count')
    salaries = salaries.fillna(0)
    higher_education_salaries = salaries['>50K']['Bachelors'] + salaries['>50K']['Masters'] + salaries['>50K']['Doctorate']
    lower_education_salaries = salaries['>50K'].sum() - higher_education_salaries
    
    higher_education_rich = round(higher_education_salaries/(salaries['>50K'].sum() + salaries['<=50K'].sum())*100, 2)
    lower_education_rich = round(lower_education_salaries/(salaries['>50K'].sum() + salaries['<=50K'].sum())*100, 2)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    count_workers_per_hour = pd.pivot_table(df, values= 'age' ,columns=['salary'], index=['hours-per-week'] , aggfunc='count')

    num_min_workers = count_workers_per_hour['>50K'][1]

    rich_percentage = round(num_min_workers/32561 * 100, 3)

    # What country has the highest percentage of people that earn >50K?
    countries_with_higher_salaries = pd.pivot_table(df, values= 'age' ,columns=['salary'], index=['native-country'] , aggfunc='count')
    countries_with_higher_salaries = countries_with_higher_salaries.fillna(0)

    percent_countries_with_higher_salaries = pd.DataFrame(countries_with_higher_salaries, columns = ['% <=50K', '% >50K'])

    percent_countries_with_higher_salaries['% <=50K'] = countries_with_higher_salaries['<=50K']/(countries_with_higher_salaries['<=50K'] + countries_with_higher_salaries['>50K']) * 100
    percent_countries_with_higher_salaries['% >50K'] = countries_with_higher_salaries['>50K']/(countries_with_higher_salaries['<=50K'] + countries_with_higher_salaries['>50K']) * 100

    highest_earning_country = percent_countries_with_higher_salaries['% >50K'].idxmax()
    highest_earning_country_percentage = round(percent_countries_with_higher_salaries['% >50K'].max(), 1)

    # Identify the most popular occupation for those who earn >50K in India.
    occupation_per_country = pd.pivot_table(df, values= 'age' ,columns=['native-country'], index=['occupation'] , aggfunc='count')
    occupation_per_country = occupation_per_country.fillna(0)
    
    top_IN_occupation = occupation_per_country['India'].idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

calculate_demographic_data()