import streamlit as st
from pipeline.pipeline import AnimeRecommenderPipeline
from dotenv import load_dotenv
import base64
import os
import re

# Set Streamlit page config
st.set_page_config(
    page_title="AnimeSensei - Your AI Guide to Anime",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment variables
load_dotenv()

# Set background image and apply styling
def set_background():
    # Load and encode the background image
    try:
        with open(os.path.join("assets", "bg.png"), "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        encoded_image = ""  # Fallback if image not found
    
    # Create CSS with background image
    css_with_bg = f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles with Background Image */
    .stApp {{
        background-image: url('data:image/png;base64,{encoded_image}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
        min-height: 100vh;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(248, 250, 252, 0.03));
        pointer-events: none;
        z-index: 0;
    }}
    
    .main-container {{
        position: relative;
        z-index: 1;
    }}"""
    
    # Add the rest of the CSS
    css_rest = """
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Main container */
    .main-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Main container */
    .main-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 3rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
        margin-bottom: 0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Remove default Streamlit margins */
    .element-container {
        margin: 0 !important;
    }
    
    .stMarkdown {
        margin-bottom: 0 !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0 !important;
    }
    
    .search-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Input styling */
    .stTextInput > div > div {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 0.75rem 1.25rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div:focus-within {
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.25);
    }
    
    .stTextInput input {
        color: #000000;
        font-weight: 500;
        background: transparent !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(0, 0, 0, 0.6);
        font-style: italic;
    }
    
    .stTextInput label {
        font-weight: 600;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 0.5rem;
        background: none !important;
        padding: 0 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Results container */
    .results-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        margin-top: 1rem;
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .results-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 1.5rem;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(1px 1px 2px rgba(0, 0, 0, 0.3));
    }
    
    .results-content {
        font-size: 1.1rem;
        line-height: 1.8;
        padding: 1.5rem;
        color: #000000;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        text-shadow: none;
    }
    
    /* Loading spinner */
    .stSpinner {
        text-align: center;
    }
    
    /* Error styling */
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(248, 113, 113, 0.05));
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Example tags */
    .example-tags {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .example-tag {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        opacity: 0.8;
        transition: opacity 0.3s ease;
        cursor: pointer;
    }
    
    .example-tag:hover {
        opacity: 1;
        transform: translateY(-1px);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .header-container,
        .results-container {
            padding: 1.5rem;
        }
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .header-container {
        animation: fadeInUp 0.8s ease-out;
    }
    
    .results-container {
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    </style>
    </style>
    """
    
    # Combine and apply the CSS
    st.markdown(css_with_bg + css_rest, unsafe_allow_html=True)

# Cache pipeline initialization
@st.cache_resource
def init_pipeline():
    return AnimeRecommenderPipeline(csv_path="data/anime_updated.csv")

# Cache pipeline initialization
@st.cache_resource
def init_pipeline():
    return AnimeRecommenderPipeline(csv_path="data/anime_updated.csv")

# Apply background and custom styling
set_background()

# Initialize pipeline
pipeline = init_pipeline()

# Main content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="header-container">
    <h1 class="main-title">🌸 AnimeSensei</h1>
    <p class="subtitle">Your AI-Powered Journey Through the World of Anime</p>
</div>
""", unsafe_allow_html=True)

# Input field
query = st.text_input(
    "",
    placeholder="e.g., Romantic slice of life with beautiful animation, Dark fantasy with complex characters, Comedy anime for beginners...",
    key="query",
    help="Describe the type of anime you're looking for - genre, mood, themes, or specific preferences"
)

# Example tags
st.markdown("""
<div class="example-tags">
    <span class="example-tag">🌸 Romance & Drama</span>
    <span class="example-tag">⚔️ Action & Adventure</span>
    <span class="example-tag">😂 Comedy & Slice of Life</span>
    <span class="example-tag">🌟 Fantasy & Supernatural</span>
    <span class="example-tag">🤖 Sci-Fi & Mecha</span>
    <span class="example-tag">😱 Horror & Thriller</span>
</div>
""", unsafe_allow_html=True)

# Results section
if query:
    with st.spinner("🎭 Analyzing your preferences and finding perfect anime matches..."):
        try:
            response = pipeline.recommend(query)
            if response:
                st.markdown('<div class="results-container">', unsafe_allow_html=True)
                st.markdown('<h2 class="results-title">✨ Your Personalized Recommendations</h2>', unsafe_allow_html=True)
                # Format the response to make certain labels bold and add line breaks
                formatted_response = response
                
                # First, normalize line breaks and remove extra spaces
                formatted_response = re.sub(r'\n\s*\n\s*\n+', '\n\n', formatted_response)
                
                # Handle titles and sections
                # Function to process each anime entry
                def format_anime_entry(match):
                    title = match.group(1)
                    content = match.group(2)
                    # Remove "Title:" if present and format title with gradient
                    title = title.replace('Title:', '').strip()
                    return f'<strong style="font-weight: 600; font-size: 1.8rem; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; filter: drop-shadow(1px 1px 2px rgba(0, 0, 0, 0.3));">{title}</strong><span style="font-size: 1rem; font-style: italic;">{content}</span>'
                
                # Format each anime entry
                formatted_response = re.sub(
                    r'(\d+\.\s+\*\*.*?\*\*)(.*?)(?=(?:\d+\.|$))',
                    format_anime_entry,
                    formatted_response,
                    flags=re.DOTALL
                )
                
                # Remove remaining markdown bold markers
                formatted_response = formatted_response.replace('**', '')
                
                # Format section headers (both with and without colon)
                formatted_response = formatted_response.replace(
                    "Plot Summary:",
                    '<br><strong style="font-weight: 700; font-size: 1.1rem;">Plot Summary:</strong>'
                )
                formatted_response = formatted_response.replace(
                    "Why it matches your preferences:",
                    '<br><strong style="font-weight: 700; font-size: 1.1rem;">Why it matches your preferences:</strong>'
                )
                formatted_response = re.sub(
                    r'Why it matches the user\'s preferences',
                    '<br><strong style="font-weight: 700; font-size: 1.1rem;">Why it matches the user\'s preferences</strong>',
                    formatted_response
                )
                
                # Convert remaining newlines to HTML breaks with consistent spacing
                formatted_response = formatted_response.strip()
                formatted_response = re.sub(r'\n\s*\n', '<br><br>', formatted_response)
                formatted_response = formatted_response.replace('\n', '<br>')
                
                st.markdown(f'<div class="results-content">{formatted_response}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("🙈 Hmm, I couldn't find any recommendations. Try describing your preferences differently!")
        except Exception as e:
            st.error(f"🚫 Oops! Something went wrong while generating recommendations: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; opacity: 0.7;">
    <p style="color: #64748b; font-size: 0.9rem;">
        🌟 Discover your next favorite anime with AI-powered recommendations
    </p>
</div>
""", unsafe_allow_html=True)