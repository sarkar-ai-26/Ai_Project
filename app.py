import streamlit as st
import google.generativeai as genai
import os

# Set page config
st.set_page_config(
    page_title="AI Solutions Ideas Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
    }
    
    .hero {
        background: linear-gradient(135deg, #1f4037 0%, #99f2c8 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .hero h1 {
        color: white !important;
        font-weight: 700;
        margin-bottom: 10px;
        font-size: 3rem;
    }
    
    .hero p {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #1f4037 0%, #1f4037 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        color: #99f2c8;
        border: 1px solid #99f2c8;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero">
        <h1>🚀 AI Solutions Ideas Generator</h1>
        <p>Discover high-impact AI startup opportunities tailored to specific industries and problem types.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings & Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API Key here")
    
    available_models = ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest", "gemini-pro"]
    if api_key:
        try:
            genai.configure(api_key=api_key.strip())
            fetched = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if fetched:
                available_models = fetched
        except Exception:
            pass

    model_choice = st.selectbox(
        "Select Model",
        available_models
    )

    st.markdown("---")
    
    st.header("🎯 Parameters")
    industry = st.selectbox(
        "Select Industry",
        ["Healthcare & Medical", "Automobile & Transport", "Multimedia & Entertainment", "Beauty & Cosmetics", "Agriculture & Farming", "Finance & Banking", "Education", "Retail & E-commerce", "Custom"]
    )
    
    if industry == "Custom":
        custom_industry = st.text_input("Enter Custom Industry")
        final_industry = custom_industry
    else:
        final_industry = industry
        
    problem_type = st.selectbox(
        "Type of Problem",
        ["Workflow Inefficiency", "High Cost", "Accuracy & Errors", "Customer Experience", "Data Analysis & Insights", "Personalization"]
    )
    
    num_ideas = st.slider("Number of Ideas", min_value=1, max_value=5, value=3)

# Main Area
st.subheader("💡 Generate Opportunities")
st.write("Click below to analyze the market and generate precise, two-liner problems and AI solutions.")

if st.button("Generate AI Venture Ideas"):
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        
    if not api_key:
        st.error("⚠️ Please provide a Gemini API Key in the sidebar to continue.")
    else:
        try:
            genai.configure(api_key=api_key.strip())
            # Use the model selected from the sidebar
            model = genai.GenerativeModel(model_choice)
            
            prompt = f'''
            Act as a highly experienced technical founder and Problem-Solution scout.
            My goal is to find startup ideas where base LLM models (with mild fine-tuning or RAG) can solve real gaps.
            
            Industry: {final_industry}
            Problem Focus: {problem_type}
            
            Please output exactly {num_ideas} ideas. 
            For each idea, provide exactly two components, each being a short 1-2 sentence paragraph:
            - Problem: [Describe the gap/problem]
            - Solution: [Describe the AI solution using base/fine-tuned LLM]
            
            Format as Markdown, bolding "Problem:" and "Solution:". Add a creative title for each idea (e.g. ### 1. Intelligent Triage).
            Do not output anything else. 
            '''
            
            with st.spinner("Analyzing market gaps and generating solutions..."):
                response = model.generate_content(prompt)
                
            st.success("Generation Complete!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
