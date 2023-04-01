import streamlit as st
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

    age = st.slider('How old are you?', 1, 11, 5)
    st.write("I'm ", age, 'years old')



st.write(add_radio)

def Covered_call(Strike_Distance,Trigger_Limit,Accumulated_Stock_Limit,freq):
    
    df=pd.read_csv(f"stock_mtm_SPY_OTM_{Strike_Distance}.csv")
    df = df.loc[(df["Trigger_limit"]==Trigger_Limit)& (df["Accumulated_limit"]==Accumulated_Stock_Limit)]
    

    # set the style and color palette
    sns.set_style('whitegrid')
    sns.set_palette('Dark2')

    # create sample data
    data = {'Date': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01', '2022-06-01', '2022-07-01', '2022-08-01', '2022-09-01', '2022-10-01', '2022-11-01', '2022-12-01'],
            'Realized_Returns': [0.02, -0.01, 0.03, -0.02, 0.05, 0.01, 0.02, -0.03, 0.04, 0.01, -0.02, 0.03],
            'Unrealized_Returns': [0.01, -0.02, 0.05, -0.03, 0.04, 0.03, 0.02, -0.01, 0.05, -0.02, 0.01, -0.03]}
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # create a function to resample the data
    def resample_data(df, freq):
        if freq == 'daily':
            return df
        elif freq == 'monthly':
            return df.resample('M').sum()
        elif freq == 'yearly':
            return df.resample('Y').sum()

    # set the frequency of the bar chart
    
    
    # resample the data
    df_resampled = resample_data(df, freq)

    # create a stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    df_resampled.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Returns', fontsize=12)
    ax.set_title(f'Realized and Unrealized Returns ({freq} frequency)', fontsize=16, fontweight='bold')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    ax.legend(fontsize=12)
    plt.show()
    st.pyplot(fig)


    # create a line chart with shaded regions
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_resampled.index, df_resampled['Realized_Returns'], label='Realized Returns')
    ax.plot(df_resampled.index, df_resampled['Unrealized_Returns'], label='Unrealized Returns')
    ax.fill_between(df_resampled.index, df_resampled['Realized_Returns'], df_resampled['Unrealized_Returns'], where=df_resampled['Realized_Returns'] > df_resampled['Unrealized_Returns'], interpolate=True, alpha=0.25, color='green')
    ax.fill_between(df_resampled.index, df_resampled['Realized_Returns'], df_resampled['Unrealized_Returns'], where=df_resampled['Realized_Returns'] < df_resampled['Unrealized_Returns'], interpolate=True, alpha=0.25, color='red')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Returns', fontsize=12)
    ax.set_title('Realized and Unrealized Returns', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.show()
    st.pyplot(fig)

Strike_Distance=1
Trigger_Limit=1
Accumulated_Stock_Limit=3
freq = 'monthly'
Covered_call(Strike_Distance,Trigger_Limit,Accumulated_Stock_Limit,freq)