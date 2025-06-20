import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Login Credentials ---
USER_CREDENTIALS = {"Rameen": "1234"}

def login(username, password):
    return USER_CREDENTIALS.get(username) == password

# --- CSV Loading and Cleaning ---
def load_csv(file):
    try:
        df = pd.read_csv(file)

        if 'Total Revenue' in df.columns:
            if df['Total Revenue'].dtype == 'object':
                df['Total Revenue'] = df['Total Revenue'].str.replace(',', '', regex=True).astype(float)

        if 'Gross Profit' in df.columns:
            if df['Gross Profit'].dtype == 'object':
                df['Gross Profit'] = df['Gross Profit'].str.replace('%', '', regex=True).astype(float)

        return df

    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# --- Dataset Summary ---
def analyze_data(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": df.isnull().sum().sum(),
        "summary": df.describe()
    }

# --- Plot Graphs ---
def plot_graphs(df):
    st.subheader("📊 Data Visualizations")

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns to visualize.")
        return

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    corr = df[numeric_cols].corr()
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax1)
    st.pyplot(fig1)

    # Histogram
    st.subheader("Histogram")
    selected_hist_col = st.selectbox("Choose column for histogram", numeric_cols, key='hist')
    if selected_hist_col:
        fig2, ax2 = plt.subplots()
        sns.histplot(df[selected_hist_col], kde=True, ax=ax2)
        ax2.set_title(f'Histogram of {selected_hist_col}')
        st.pyplot(fig2)

    # Scatter Plot
    if len(numeric_cols) >= 2:
        st.subheader("Scatter Plot")
        col1 = st.selectbox("X-axis", numeric_cols, key='x')
        col2 = st.selectbox("Y-axis", numeric_cols, key='y')
        fig3, ax3 = plt.subplots()
        sns.scatterplot(data=df, x=col1, y=col2, ax=ax3)
        ax3.set_title(f'{col1} vs {col2}')
        st.pyplot(fig3)

# --- Main App ---
def main():
    st.set_page_config(page_title="Fundamentals Analyzer", layout="wide")
    st.title("🔐 Login + NYSE Fundamentals CSV Analyzer")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.session_state.authenticated = True
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    else:
        st.sidebar.success("✅ Logged in as Rameen")
        st.header("📂 Upload and Analyze `fundamentals.csv`")

        uploaded_file = st.file_uploader("Upload fundamentals.csv", type=["csv"])

        if uploaded_file is not None:
            df = load_csv(uploaded_file)

            if df is not None:
                st.subheader("📄 Data Preview")
                st.dataframe(df.head())

                st.subheader("📈 Dataset Summary")
                stats = analyze_data(df)
                st.write(f"*Total Rows:* {stats['rows']}")
                st.write(f"*Total Columns:* {stats['columns']}")
                st.write(f"*Missing Values:* {stats['missing_values']}")
                st.dataframe(stats["summary"])

                plot_graphs(df)

# --- Run App ---
if __name__ == "__main__":
    main()




