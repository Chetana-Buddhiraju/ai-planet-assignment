# app.py
import streamlit as st
import os
from orchestrator import run_analysis
from config import Config

# Page configuration
st.set_page_config(
    page_title="AI Planet - GenAI Use Case Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🚀 AI Planet - GenAI Use Case Generator")
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key validation
        try:
            Config.validate_keys()
            st.success("✅ All API keys configured")
        except ValueError as e:
            st.error(f"❌ {e}")
            st.info("Please set your API keys in the .env file")
            return
        
        st.markdown("---")
        st.markdown("### 📋 How to use:")
        st.markdown("""
        1. Enter a company name or industry
        2. Click 'Generate Use Cases'
        3. Wait for the analysis to complete
        4. Review the prioritized use cases
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔍 Company/Industry Analysis")
        company = st.text_input(
            "Enter company name or industry:",
            placeholder="e.g., Tesla, Healthcare, Fintech",
            help="Enter the name of a company or industry you want to analyze for AI use cases"
        )
        
        if st.button("🚀 Generate Use Cases", type="primary", use_container_width=True):
            if not company:
                st.warning("⚠️ Please enter a company name or industry.")
            else:
                with st.spinner('🔄 Running analysis... This may take a few minutes.'):
                    try:
                        # Run the analysis
                        prioritized_usecases = run_analysis(company)
                        
                        if prioritized_usecases:
                            st.success(f"✅ Analysis complete! Found {len(prioritized_usecases)} use cases for {company}")
                            
                            # Display results
                            display_results(prioritized_usecases)
                        else:
                            st.warning("⚠️ Could not generate use cases. Please check the logs for errors.")
                            
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        st.info("Please check your API keys and try again.")
    
    with col2:
        st.header("📊 Quick Stats")
        if 'prioritized_usecases' in locals():
            st.metric("Use Cases Generated", len(prioritized_usecases))
            if prioritized_usecases:
                high_impact = len([uc for uc in prioritized_usecases if uc.get('impact', '').lower() == 'high'])
                st.metric("High Impact Cases", high_impact)
        else:
            st.info("Run an analysis to see statistics")

def display_results(prioritized_usecases):
    """Display the analysis results in a formatted way"""
    
    st.markdown("---")
    st.header("📋 Prioritized Use Cases")
    
    for i, uc in enumerate(prioritized_usecases):
        with st.expander(f"#{i+1} {uc.get('title', 'Untitled Use Case')} (Score: {uc.get('core_score', 'N/A'):.2f})"):
            
            # Basic information
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**📝 Description:** {uc.get('description', 'N/A')}")
                st.markdown(f"**�� Business Impact:** {uc.get('impact', 'N/A')}")
            
            with col2:
                st.markdown(f"**⚙️ Complexity:** {uc.get('complexity', 'N/A')}")
                st.markdown(f"**🎯 Core Score:** {uc.get('core_score', 'N/A'):.2f}")
            
            # Data sources
            st.markdown(f"**📊 Required Data Sources:** {uc.get('data sources', 'N/A')}")
            
            # Relevant resources
            if uc.get('datasets'):
                st.markdown("**🔗 Relevant Resources:**")
                for dataset in uc['datasets']:
                    title = dataset.get('title', 'Link')
                    url = dataset.get('url', '#')
                    notes = dataset.get('notes', '')
                    st.markdown(f"- [{title}]({url}) ({notes})")
            else:
                st.info("No relevant resources found for this use case")
    
    # Download button for the markdown report
    st.markdown("---")
    st.markdown("### 📥 Download Report")
    
    # Generate markdown content for download
    markdown_content = generate_markdown_report(prioritized_usecases)
    
    st.download_button(
        label="📄 Download Markdown Report",
        data=markdown_content,
        file_name=f"ai_usecases_report.md",
        mime="text/markdown"
    )

def generate_markdown_report(use_cases):
    """Generate markdown content for download"""
    markdown_output = "# Prioritized AI/GenAI Use Case Proposal\n\n"

    for i, uc in enumerate(use_cases):
        markdown_output += f"## {i+1}. {uc.get('title', 'Untitled Use Case')}\n\n"
        markdown_output += f"**Description:** {uc.get('description', 'N/A')}\n\n"
        markdown_output += f"**Required Data Sources:** {uc.get('data sources', 'N/A')}\n\n"
        markdown_output += f"**Expected Business Impact:** {uc.get('impact', 'N/A')} | **Estimated Complexity:** {uc.get('complexity', 'N/A')}\n\n"
        markdown_output += f"**Core Score:** {uc.get('core_score', 'N/A'):.2f}\n\n"

        if uc.get('datasets'):
            markdown_output += "**Relevant Resources:**\n"
            for dataset in uc['datasets']:
                title = dataset.get('title', 'Link')
                url = dataset.get('url', '#')
                notes = dataset.get('notes', '')
                markdown_output += f"- [{title}]({url}) ({notes})\n"
            markdown_output += "\n"

        markdown_output += "---\n\n"

    return markdown_output

if __name__ == "__main__":
    main()