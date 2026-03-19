import streamlit as st
import pandas as pd
import plotly.express as px

# _____ Load data _____
path = r"C:\Users\HARMIN\.cache\kagglehub\datasets\grandmaster07\student-exam-performance-dataset-analysis\versions\1\StudentPerformanceFactors.csv"

df = pd.read_csv(path)

df = df[df["Exam_Score"] <= 100]

print(f"Rows after cleaning: {df.shape[0]}")

st.set_page_config(page_title= "Student Performance Analysis", page_icon= "🎓", layout= "wide")

st.title("Student Performance Analysis Dashboard")
st.caption(f"Analyzing {df.shape[0]} real students 📊")


st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", df.shape[0])
col2.metric("Avg Score", f"{df["Exam_Score"].mean():.1f}")
col3.metric("Highest Score", df["Exam_Score"].max())
col4.metric("Lowest Score", df["Exam_Score"].min())

st.divider()

# Sidebar
st.sidebar.title("🎛️ Filters")

gender_filter = st.sidebar.selectbox(
    "Gender", ["All", "Male", "Female"])

school_filter = st.sidebar.selectbox(
    "School Type", ["All", "Private", "Public"])

motivation_filter = st.sidebar.selectbox(
    "Motivation Level", ["All", "High", "Medium", "Low"])

score_range = st.sidebar.slider(
    "Score Range", 55, 100, (55, 100))

# Filter logic
if gender_filter != "All":
    df = df[df["Gender"] == gender_filter]

if school_filter != "All":
    df = df[df["School_Type"] == school_filter]

if motivation_filter != "All":
    df = df[df["Motivation_Level"] == motivation_filter]

df = df[(df["Exam_Score"] >= score_range[0]) & 
        (df["Exam_Score"] <= score_range[1])]


tab1, tab2, tab3 = st.tabs([
    "📊 Score Analysis", 
    "🔍 Factor Analysis", 
    "📋 Raw Data"
])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.histogram(
            df, x="Exam_Score",
            title="Score Distribution",
            color_discrete_sequence=["#636EFA"])
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.box(
            df, x="Motivation_Level", y="Exam_Score",
            color="Motivation_Level",
            title="Score by Motivation Level")
        st.plotly_chart(fig2, use_container_width=True)
    
    fig3 = px.bar(
        df.groupby("Family_Income")["Exam_Score"].mean().reset_index(),
        x="Family_Income", y="Exam_Score",
        color="Family_Income",
        title="Average Score by Family Income")
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        fig4 = px.scatter(
            df, x="Hours_Studied", y="Exam_Score",
            color="Gender", opacity=0.5,
            title="Hours Studied vs Exam Score")
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        fig5 = px.scatter(
            df, x="Attendance", y="Exam_Score",
            color="School_Type", opacity=0.5,
            title="Attendance vs Exam Score")
        st.plotly_chart(fig5, use_container_width=True)
    
    fig6 = px.bar(
        df.groupby("Internet_Access")["Exam_Score"].mean().reset_index(),
        x="Internet_Access", y="Exam_Score",
        color="Internet_Access",
        title="Score by Internet Access")
    st.plotly_chart(fig6, use_container_width=True)

with tab3:
    st.subheader(f"Showing {df.shape[0]} students")
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Filtered Data",
        csv, "students.csv", "text/csv")

st.divider()

# INSIGHTS SECTION
st.subheader("🔍 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    top_motivation = df.groupby("Motivation_Level")["Exam_Score"].mean().idxmax()
    st.info(f"💡 **Best Motivation Level**\n\n{top_motivation} motivation students score highest!")

with col2:
    top_income = df.groupby("Family_Income")["Exam_Score"].mean().idxmax()
    st.info(f"💰 **Income Impact**\n\n{top_income} income students perform best!")

with col3:
    top_school = df.groupby("School_Type")["Exam_Score"].mean().idxmax()
    st.info(f"🏫 **School Type**\n\n{top_school} school students score higher!")

st.divider()

# CORRELATION INSIGHT
st.subheader("📈 What affects scores the most?")

corr = df[["Hours_Studied", "Attendance", 
           "Sleep_Hours", "Previous_Scores",
           "Exam_Score"]].corr()["Exam_Score"].drop("Exam_Score")

fig_corr = px.bar(
    x=corr.index,
    y=corr.values,
    title="Correlation with Exam Score",
    color=corr.values,
    color_continuous_scale="RdYlGn",
    labels={"x": "Factor", "y": "Correlation"}
)
st.plotly_chart(fig_corr, use_container_width=True)

st.divider()

st.caption("Built with ❤️ using Streamlit, Plotly & Pandas | Data: Kaggle")

