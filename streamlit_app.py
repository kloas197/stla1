import streamlit as st
from datetime import datetime, timedelta
import os
import pandas as pd

def main():
    
    path = ''
    file_head = 'VSS'
    
    st.set_page_config(layout="wide")
    
    st.title("Valuations Scorecard")
    
    with st.sidebar:
        st.header("About the Scorecard")
        st.write("Restricted Version 1.0")
        st.write("This is a restricted version of the app, which is limited to loading only pre-calculated data.")

    st.header("Credit Scorecard - Valuations Summary")

    today_weekday = datetime.today().weekday()
    if  0 < today_weekday < 6:
        day_delta = 1
    elif today_weekday == 0:
        day_delta = 3
    else:
        day_delta = 2
    the_date = (datetime.today()-timedelta(days=day_delta)).strftime('%Y-%m-%d')

    with st.form(key='my_form'):
        user_input = st.text_input("Enter a date (e.g., YYYY-MM-DD):", key='text_input',value=the_date)

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if user_input:            
            if is_valid_date_format(user_input, '%Y-%m-%d') is False:
                st.warning("Please enter a valid date.")
               
            else:
                the_date = user_input
                file_path = path + file_head + ' [' + the_date.replace('-','') + '].pkl'
            
                if os.path.exists(file_path) is False:
                    st.warning(f"The scorecard for'{the_date}' has not previously been generated.")
                else:
                    df = load_precalc_scorecard(file_path)                              
                    styled_df = style_format(df, list(set(df.columns) - set(['ticker', 'description'])),['change'],['OAS Score', 'YTW Score', 'OAS MOM Score', 'Total'],['Total'])
                    st.dataframe(styled_df)
                    st.success(f"Loaded Scorecard for: {the_date}")
            
        else:
            st.warning("Please enter some text before submitting.")


def is_valid_date_format(date_string, date_format):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False

def load_precalc_scorecard(file_path):
    c = pd.read_pickle(file_path)  
    return c

def style_format(df, num_cols,hneg_cols,score_cols,b_cols):
    df.index.name = None
    styled_df = df.style.format('{:.2f}', subset=num_cols).apply(style_highlight_negative, subset=hneg_cols).apply(style_highlight_score_color, subset=score_cols).apply(style_bold,subset=b_cols)
    return styled_df

def style_highlight_negative(s):
    return ['color: red;' if v < 0 else '' for v in s]

def style_highlight_score_color(s):
    def func(v):
        if v >=4.2:
            return 'background-color: green;'
        elif v>=3.4:
            return 'background-color: lightgreen;'
        elif v>=2.6:
            return 'background-color: white;'
        elif v>=1.8:
            return 'background-color: pink;'
        else:
            return 'background-color: red;'
    
    return [func(v) for v in s]

def style_bold(s):
    return ['font-weight: bold;' if v >=0 else '' for v in s]

if __name__ == '__main__':
    main()
