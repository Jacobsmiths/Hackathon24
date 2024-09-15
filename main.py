from numpy import ndarray
import seaborn as sn
import pandas as pd
import streamlit as st
import sqlite3
from matplotlib import pyplot as plt

# prints header to the webapge
st.header("Upload an SQLite file")

# Input field for file path
file_path1 = st.text_input("Enter the path to your SQLite file (e.g., C:/path/to/your/file.db)")
file_path2 = st.text_input("Enter the optional second path file (if you are cross comparing data)")

# if file path1 is not empty and file path two is empty
if file_path1 != '' and file_path2 == '':

    # links sql to a connector and creates cursor object to execute table reading
    con = sqlite3.connect(file_path1)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # gets the table 
    table = cur.fetchall()[0]

    # gets the tables name
    table_name = table[0]

    #converts the table into a dataframe
    df1 = pd.read_sql_query("SELECT * FROM " + table_name, con)

    # closes connector
    con.close()

    # finds unique values from the components column and stores them in list unique_components
    unique_components = ndarray.tolist(df1['ComponentName'].unique())
    unique_components.insert(0, 'None')

    # ============== Single File Graph Selection ==============
    # prints Graph Selection
    st.header("Graph Selection")

    # Creates selection box of graph types and variable selection and filter
    graphType = st.selectbox("What type of graph do you want", ('Line Plot', 'Histogram', 'Bar Plot', 'Scatter Plot'), key=1)
    x_var = st.selectbox("Select X-axis variable", df1.columns, key=2)
    y_var = st.selectbox("Select y-axis variable", df1.columns, key=3)
    filter = st.selectbox("Do you want to filter?", unique_components)

    # filters the dataframe based on filter
    if filter != 'None':
        df1 = df1[df1['ComponentName'] == filter]

    # creates graph and adds to it depending on selection
    plt.figure(figsize=(12, 6))

    if graphType == "Line Plot":
        sn.lineplot(data=df1, x=x_var, y=y_var, errorbar=("se", 2))

    elif graphType == "Bar Plot":
        sn.barplot(data=df1, x=x_var, y=y_var)

    elif graphType == "Scatter Plot":
        sn.scatterplot(data=df1, x=x_var, y=y_var)

    elif graphType == "Histogram":
        sn.histplot(data=df1, x=x_var, bins=30)

    # if button is pressed, display graph
    if st.button("Generate Graph", key=10):
        plt.xticks(rotation=45)
        st.pyplot(plt)



# if file path 1 and file path 2 have paths
elif file_path1!='' and file_path2 != '':

    # links sql to a connector and creates cursor object to execute table reading
    con = sqlite3.connect(file_path1)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # gets the table 
    table = cur.fetchall()[0]

    # gets the tables name
    table_name = table[0]

    #converts the table into a dataframe
    df1 = pd.read_sql_query("SELECT * FROM " + table_name, con)

    # closes connection
    con.close()

    # does the same thing again with file 2 and stores data in df2
    con = sqlite3.connect(file_path2)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table = cur.fetchall()[0]
    table_name = table[0]
    df2 = pd.read_sql_query("SELECT * FROM " + table_name, con)
    con.close()

    # ============ Graph Selection  With 2 Files ==============
    # prints graph selection header
    st.header("Graph Selection")

    # creates graph selection box
    graphType = st.selectbox("What type of graph do you want", ('Line Plot', 'Histogram', 'Bar Plot', 'Scatter Plot'), key=8)

    # chooses x and y variabels from file 1 and 2
    st.write("From File 1:")
    x_var1 = st.selectbox("Select X-axis variable", df1.columns, key=4)
    y_var1 = st.selectbox("Select y-axis variable", df1.columns, key=5)

    st.write("From File 2:")
    x_var2 = st.selectbox("Select X-axis variable", df1.columns, key=6)
    y_var2 = st.selectbox("Select y-axis variable", df1.columns, key=7)

    # gets unique components of component name for files 1 and 2
    unique_components = ndarray.tolist(df1['ComponentName'].unique())
    unique_components.insert(0, 'None')

    unique_components = ndarray.tolist(df2['ComponentName'].unique())
    unique_components.insert(0, 'None')

    # creates filter selection box
    filter1 = st.selectbox("Do you want to filter data in file1?", unique_components)
    filter2 = st.selectbox("Do you want to filter data in file2?", unique_components)

    # filters if filters arent None
    if filter1 != 'None':
        df1 = df1[df1['ComponentName'] == filter1]
    
    if filter2 != 'None':
        df2 = df2[df2['ComponentName'] == filter2]
    
    # Choose comparison method: Overlay or Side-by-Side
    comparison_method = st.radio("Choose comparison method", ("Overlay", "Side-by-Side"))

    # CASE 1: Overlay the Plots
    if comparison_method == "Overlay":
        st.subheader("Overlay Plot")

        # creates plot with dimensions 12 and 6
        plt.figure(figsize=(12, 6))

        # Creates graphs based on selected Graph type
        if graphType == "Line Plot":
            sn.lineplot(data=df1, x=x_var1, y=y_var1, color='blue')
            sn.lineplot(data=df2, x=x_var2, y=y_var2, color='red')

        elif graphType == "Bar Plot":
            sn.barplot(data=df1, x=x_var1, y=y_var1)
            sn.barplot(data=df2, x=x_var2, y=y_var2)

        elif graphType == "Scatter Plot":
            sn.scatterplot(data=df1, x=x_var1, y=y_var1)
            sn.scatterplot(data=df2, x=x_var2, y=y_var2)

        elif graphType == "Histogram":
            sn.histplot(data=df1, x=x_var1, bins=30)
            sn.histplot(data=df1, x=x_var2, bins=30)

        # generates graph when button is pressed
        if st.button("Generate Graph", key=10):
            plt.xticks(rotation=45) # rotates x axis labels
            st.pyplot(plt)

    # CASE 2: Side-by-Side Subplots
    elif comparison_method == "Side-by-Side":
        st.subheader("Side-by-Side Comparison")

        # creates a figure and subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

        # creates graphs based on selected graph type
        if graphType == "Line Plot":
            sn.lineplot(data=df1, x=x_var1, y=y_var1, ax=ax1)
            ax1.set_title('Graph 1')
            sn.lineplot(data=df2, x=x_var2, y=y_var2, ax=ax2)
            ax2.set_title("Graph 2")

        elif graphType == "Bar Plot":
            sn.barplot(data=df1, x=x_var1, y=y_var1, ax=ax1)
            ax1.set_title("Graph 1")
            sn.barplot(data=df2, x=x_var2, y=y_var2, ax=ax2)
            ax2.set_title("Graph 2")

        elif graphType == "Scatter Plot":
            sn.scatterplot(data=df1, x=x_var1, y=y_var1, ax=ax1)
            ax1.set_title("Graph 1")
            sn.scatterplot(data=df2, x=x_var2, y=y_var2, ax=ax2)
            ax2.set_title("Graph 2")

        elif graphType == "Histogram":
            sn.histplot(data=df1, x=x_var1, bins=30, ax=ax1)
            ax1.set_title("Graph 1")
            sn.histplot(data=df1, x=x_var2, bins=30, ax=ax1)
            ax2.set_title("Graph 2")
        
        # generates graph when pressed
        if st.button("Generate Graph", key=9):
            plt.xticks(rotation=45) 
            st.pyplot(fig)
        



    
