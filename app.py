import streamlit as st
import os
from summarizer import TextSummarizer
import time

# Configure page
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)

# Initialize session state
if 'summarizer' not in st.session_state:
    st.session_state.summarizer = None

def initialize_summarizer():
    """Initialize the text summarizer with API key"""
    try:
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            st.error("⚠️ Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
            return None
        
        summarizer = TextSummarizer(api_key)
        return summarizer
    except Exception as e:
        st.error(f"❌ Failed to initialize summarizer: {str(e)}")
        return None

def main():
    # Header
    st.title("🤖 AI Text Summarizer")
    st.markdown("Powered by Google Gemini 1.5 Flash & LangChain")
    st.divider()
    
    # Initialize summarizer if not already done
    if st.session_state.summarizer is None:
        with st.spinner("Initializing AI model..."):
            st.session_state.summarizer = initialize_summarizer()
    
    if st.session_state.summarizer is None:
        st.stop()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Summarization style
        summary_style = st.selectbox(
            "Summary Style",
            ["Brief", "Detailed", "Bullet Points"],
            help="Choose the style of summary you want"
        )
        
        # Summary length
        summary_length = st.slider(
            "Summary Length",
            min_value=50,
            max_value=500,
            value=150,
            step=25,
            help="Approximate number of words in the summary"
        )
        
        # Language
        language = st.selectbox(
            "Output Language",
            ["English", "Spanish", "French", "German", "Italian"],
            help="Language for the summary output"
        )
        
        st.divider()
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Paste text directly or upload a text file
        - Longer texts work better for summarization
        - Try different styles for various use cases
        - Brief: Quick overview
        - Detailed: Comprehensive summary
        - Bullet Points: Key points listed
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📄 Input Text")
        
        # Text input options
        input_method = st.radio(
            "Choose input method:",
            ["Type/Paste Text", "Upload File"],
            horizontal=True
        )
        
        input_text = ""
        
        if input_method == "Type/Paste Text":
            input_text = st.text_area(
                "Enter text to summarize:",
                height=300,
                placeholder="Paste your text here..."
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload a text file",
                type=['txt', 'md'],
                help="Upload a .txt or .md file"
            )
            
            if uploaded_file is not None:
                try:
                    input_text = str(uploaded_file.read(), "utf-8")
                    st.text_area(
                        "File content preview:",
                        value=input_text[:500] + "..." if len(input_text) > 500 else input_text,
                        height=200,
                        disabled=True
                    )
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        # Text statistics
        if input_text:
            word_count = len(input_text.split())
            char_count = len(input_text)
            st.info(f"📊 Text Stats: {word_count} words, {char_count} characters")
    
    with col2:
        st.header("✨ Generated Summary")
        
        # Summary button
        if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
            if not input_text or len(input_text.strip()) < 50:
                st.warning("⚠️ Please provide at least 50 characters of text for summarization.")
            else:
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Update progress
                    progress_bar.progress(25)
                    status_text.text("🔄 Preparing text...")
                    time.sleep(0.5)
                    
                    progress_bar.progress(50)
                    status_text.text("🤖 Sending to AI model...")
                    time.sleep(0.5)
                    
                    progress_bar.progress(75)
                    status_text.text("✨ Generating summary...")
                    
                    # Generate summary
                    summary = st.session_state.summarizer.summarize_text(
                        text=input_text,
                        style=summary_style.lower(),
                        max_words=summary_length,
                        language=language.lower()
                    )
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Summary generated!")
                    time.sleep(0.5)
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Display summary
                    st.success("Summary generated successfully!")
                    st.text_area(
                        "Generated Summary:",
                        value=summary,
                        height=300,
                        disabled=True
                    )
                    
                    # Summary statistics
                    summary_words = len(summary.split())
                    summary_chars = len(summary)
                    compression_ratio = round((1 - summary_words / word_count) * 100, 1) if word_count > 0 else 0
                    
                    st.info(f"📈 Summary Stats: {summary_words} words, {summary_chars} characters ({compression_ratio}% compression)")
                    
                    # Download button
                    st.download_button(
                        label="💾 Download Summary",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Error generating summary: {str(e)}")
                    st.info("💡 Please check your API key and try again.")
        
        # Placeholder when no summary is generated
        else:
            st.info("👆 Enter text and click 'Generate Summary' to see results here.")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit, LangChain & Google Gemini 1.5 Flash</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
