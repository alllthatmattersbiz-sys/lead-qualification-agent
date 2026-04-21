import streamlit as st
from sources.hackernews import search_hackernews_ai_jobs
from sources.github import search_github_hiring_issues
from processors.claude_qualifier import batch_qualify_leads
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Lead Qualifier",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 AI Automation Lead Qualifier")
st.write("Find, qualify, and engage with AI/Automation opportunities from HackerNews & GitHub")

# Initialize session state
if 'raw_leads' not in st.session_state:
    st.session_state.raw_leads = []
if 'qualified_leads' not in st.session_state:
    st.session_state.qualified_leads = []

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("📍 Select Sources")
    selected_sources = st.multiselect(
        "Which sources to search?",
        ["HackerNews", "GitHub"],
        default=["HackerNews", "GitHub"],
        key="source_selector"
    )
    
    st.divider()
    
    st.subheader("🤖 Qualify How Many Leads?")
    num_leads_to_qualify = st.slider(
        "Number of leads to qualify (1-10):",
        1, 10, 1,
        key="qualify_count",
        help="Choose how many leads Claude will analyze"
    )
    
    st.info(f"📊 You will qualify the first **{num_leads_to_qualify}** leads with Claude")
    
    st.divider()
    
    st.subheader("🎯 Filter Display")
    min_score_filter = st.slider(
        "Show leads with score >= ",
        0, 10, 0,
        key="score_filter"
    )

# Main content area
st.divider()

# Step 1: Search
st.header("Step 1: Search for Leads")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Search Sources", key="search_btn", use_container_width=True):
        if not selected_sources:
            st.error("❌ Please select at least one source!")
        else:
            all_leads = []
            
            with st.spinner("Searching selected sources..."):
                if "HackerNews" in selected_sources:
                    hn_leads = search_hackernews_ai_jobs()
                    all_leads.extend(hn_leads)
                    st.success(f"✅ HackerNews: {len(hn_leads)} leads found")
                
                if "GitHub" in selected_sources:
                    github_leads = search_github_hiring_issues()
                    all_leads.extend(github_leads)
                    st.success(f"✅ GitHub: {len(github_leads)} leads found")
            
            st.session_state.raw_leads = all_leads
            st.success(f"✅ **Total: {len(all_leads)} leads found!**")

with col2:
    if st.session_state.raw_leads:
        st.info(f"📊 {len(st.session_state.raw_leads)} raw leads ready to qualify")

# Display raw leads if available
if st.session_state.raw_leads and not st.session_state.qualified_leads:
    st.subheader("📋 Raw Leads (Before Qualification)")
    
    raw_df = pd.DataFrame([
        {
            'Author': lead['author'],
            'Source': lead['source'],
            'Title': lead['title'][:50],
            'Keywords': lead['keywords_matched']
        }
        for lead in st.session_state.raw_leads
    ])
    
    st.dataframe(raw_df, use_container_width=True)

st.divider()

# Step 2: Qualify with Claude
st.header(f"Step 2: Qualify with Claude (First {num_leads_to_qualify} Lead{'s' if num_leads_to_qualify > 1 else ''})")

if st.session_state.raw_leads:
    if st.button(f"🤖 Qualify {num_leads_to_qualify} Lead{'s' if num_leads_to_qualify > 1 else ''} with Claude", key="qualify_btn", use_container_width=True):
        with st.spinner(f"🤔 Claude is analyzing {num_leads_to_qualify} lead{'s' if num_leads_to_qualify > 1 else ''}..."):
            # Qualify the specified number of leads
            leads_to_qualify = st.session_state.raw_leads[:num_leads_to_qualify]
            qualified = batch_qualify_leads(leads_to_qualify)
            st.session_state.qualified_leads = qualified
        
        st.success(f"✅ Qualified {len(qualified)} lead{'s' if len(qualified) > 1 else ''}!")
else:
    st.info("👆 Search for leads first!")

st.divider()

# Step 3: Display ALL Raw Leads
if st.session_state.raw_leads:
    st.header("Step 3: All Leads Found")
    
    raw_df = pd.DataFrame([
        {
            'Author': lead['author'],
            'Source': lead['source'],
            'Title': lead['title'][:60],
            'Keywords': lead['keywords_matched']
        }
        for lead in st.session_state.raw_leads
    ])
    
    st.dataframe(raw_df, use_container_width=True)
    st.info(f"📊 Total leads found: {len(st.session_state.raw_leads)}")

st.divider()

# Step 4: Display Qualified Results
if st.session_state.qualified_leads:
    st.header(f"Step 4: Claude Analysis ({len(st.session_state.qualified_leads)} Lead{'s' if len(st.session_state.qualified_leads) > 1 else ''})")
    
    # Filter by score
    filtered_qualified = [l for l in st.session_state.qualified_leads if l.get('score', 0) >= min_score_filter]
    
    if not filtered_qualified:
        st.warning(f"No leads match the score filter (>= {min_score_filter})")
    else:
        for idx, lead in enumerate(filtered_qualified):
            score = lead.get('score', '?')
            is_qualified = lead.get('is_qualified', False)
            status = "✅ QUALIFIED" if is_qualified else "❌ NOT QUALIFIED"
            
            with st.expander(f"**[{score}/10]** {lead['author']} - {status}", expanded=(idx == 0)):
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.metric("Score", f"{score}/10")
                    st.metric("Status", "✅ Qualified" if is_qualified else "❌ Not Qualified")
                    st.metric("Source", lead['source'])
                
                with col_right:
                    st.metric("Company", lead.get('company_name', 'Unknown'))
                    st.metric("Budget", lead.get('budget_signal', 'N/A'))
                    st.metric("Timeline", lead.get('timeline', 'N/A'))
                
                st.divider()
                
                st.subheader("📌 Opportunity")
                st.write(lead.get('opportunity', 'N/A'))
                
                st.subheader("📝 Analysis")
                st.write(lead.get('explanation', 'N/A'))
                
                st.divider()
                
                st.subheader("📧 Email Draft")
                st.write(f"**Subject:** {lead.get('email_subject', 'N/A')}")
                st.text_area(
                    "Email:",
                    value=lead.get('email_opening', 'N/A'),
                    height=120,
                    disabled=True,
                    key=f"email_draft_{idx}"
                )
                
                st.divider()
                st.markdown(f"🔗 [View Original]({lead['hn_link']})")

# Step 5: Save to Google Sheets
if st.session_state.qualified_leads:
    st.divider()
    st.header("Step 5: Save to Google Sheets")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save to Google Sheets", key="save_sheets_btn", use_container_width=True):
            from processors.sheets_handler import save_leads_to_sheets, get_sheet_url
            
            with st.spinner("Saving to Google Sheets..."):
                success = save_leads_to_sheets(st.session_state.qualified_leads)
            
            if success:
                st.success("✅ Leads saved to Google Sheets!")
                sheet_url = get_sheet_url()
                if sheet_url:
                    st.markdown(f"🔗 [Open Google Sheet]({sheet_url})")
            else:
                st.error("❌ Failed to save to Google Sheets. Check your GOOGLE_SHEET_ID in .env")
    
    with col2:
        st.info("💡 Leads are appended to your Google Sheet with date, score, email drafts, and more!")

# Footer
st.divider()
st.caption("🚀 AI Lead Qualifier | Find, Qualify & Engage with AI/Automation Opportunities")