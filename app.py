#%%writefile app.py
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

st.title("Data Cleaning Tool")

# File Upload
uploaded_file = st.file_uploader("Upload your dataset (CSV/Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("Preview of the Dataset:")
    st.dataframe(df)

    # Cleaning Options
    st.header("Cleaning Options")

    # Handle Missing Values
    missing_option = st.selectbox("Handle Missing Values", ["None", "Drop Rows", "Drop Columns", "Fill with Mean", "Fill with Median", "Fill with Mode"])
    if missing_option == "Drop Rows":
        df = df.dropna()
    elif missing_option == "Drop Columns":
        df = df.dropna(axis=1)
    elif missing_option == "Fill with Mean":
        df = df.fillna(df.mean())
    elif missing_option == "Fill with Median":
        df = df.fillna(df.median())
    elif missing_option == "Fill with Mode":
        df = df.fillna(df.mode().iloc[0])

    # Remove Duplicates
    if st.button("Remove Duplicates"):
        df = df.drop_duplicates()

    # Rename Columns
    st.header("Rename Columns")
    for col in df.columns:
        new_name = st.text_input(f"Rename {col}", col)
        if new_name:
            df = df.rename(columns={col: new_name})

    # Reorder Columns
    column_order = st.multiselect("Reorder Columns", df.columns.tolist(), df.columns.tolist())
    if column_order:
        df = df[column_order]

    # Show Summary Statistics
    if st.checkbox("Show Summary Statistics"):
        st.write(df.describe())

    # Missing Value Heatmap
    if st.checkbox("Show Missing Value Heatmap"):
        fig, ax = plt.subplots()
        sns.heatmap(df.isnull(), cbar=False, ax=ax)
        st.pyplot(fig)

    # Correlation Matrix
   # if st.checkbox("Show Correlation Matrix"):
        
        # label_encoders = {}
        # for column in df.select_dtypes(include=['object']).columns:
        #     le = LabelEncoder()
        #     df[column] = le.fit_transform(df[column])
        #     label_encoders[column] = le  # Save the encoder for future use


        # corr = df.corr()
        # st.write(corr)
        # fig, ax = plt.subplots()
        # sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        # st.pyplot(fig)

    # Export Cleaned Data
    if st.button("Download Cleaned Data"):
        cleaned_file = df.to_csv(index=False)
        st.download_button("Download CSV", data=cleaned_file, file_name="cleaned_data.csv", mime="text/csv")
