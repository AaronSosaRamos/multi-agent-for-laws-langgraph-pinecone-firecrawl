import streamlit as st
import json
from graph.graph import app

# Streamlit UI for Multi-Agent for Laws
def main():
    st.set_page_config(page_title="Multi-Agent for Laws", layout="wide", initial_sidebar_state="expanded")
    st.title("⚖️ Multi-Agent for Laws Dashboard")
    st.markdown("### Professional UI for Legal Analysis with LangGraph, Firecrawl, and Pinecone")

    # Initialize session state
    if "result" not in st.session_state:
        st.session_state.result = None

    # Sidebar inputs
    st.sidebar.header("🔍 Input Settings")
    url = st.sidebar.text_input("🌐 Legal Document URL", "https://law.stanford.edu/stanford-lawyer/articles/artificial-intelligence-and-the-law/")
    legal_question = st.sidebar.text_area("✍️ Legal Question", "How can I create Artificial Intelligence with the appropriate Laws?")
    lang = st.sidebar.selectbox("🌍 Language", ["es", "en", "fr", "de", "zh"], index=0)

    # Process Request
    if st.sidebar.button("🚀 Analyze Laws"):
        with st.spinner("Analyzing legal context with Multi-Agent system..."):
            try:
                inputs = {
                    "url": url,
                    "legal_question": legal_question,
                    "lang": lang,
                }

                # Run the app
                result = app.invoke(inputs)

                # Store the result in session state
                st.session_state.result = result

            except Exception as e:
                st.error(f"Error processing request: {e}")
                st.session_state.result = None

    # Display results if available
    if st.session_state.result:
        display_results(st.session_state.result)

# Display results in Markdown and JSON format
def display_results(result):
    st.markdown("### 📜 Legal Analysis Results")

    # Legal Summary Output
    st.markdown("#### 📝 Legal Summary Output")
    legal_summary = result.get("legal_summary_output", {})
    st.markdown(f"**Context**: {legal_summary.get('context', 'N/A')}")

    st.markdown("**Parties Involved:**")
    for party in legal_summary.get("parties", []):
        st.markdown(f"- **Name**: {party.get('name', 'N/A')} | **Role**: {party.get('role', 'N/A')} | **Contact Info**: {party.get('contact_info', 'N/A')} | **Legal Representative**: {party.get('legal_representative', 'N/A')} | **Stake**: {party.get('stake', 'N/A')}")

    st.markdown("**Relevant Dates:**")
    for date in legal_summary.get("relevant_dates", []):
        st.markdown(f"- **Event**: {date.get('event', 'N/A')} | **Date**: {date.get('date', 'N/A')}")

    st.markdown(f"**Summary Length**: {legal_summary.get('summary_length', 'N/A')} words")
    st.markdown(f"**Jurisdiction**: {legal_summary.get('jurisdiction', 'N/A')}")
    st.markdown(f"**Keywords**: {', '.join(legal_summary.get('keywords', []))}")

    # Law Content Analysis Output
    st.markdown("#### 📖 Law Content Analysis Output")
    law_content = result.get("law_content_analysis_output", {})
    st.markdown(f"**Document ID**: {law_content.get('document_id', 'N/A')}")
    st.markdown(f"**Document Type**: {law_content.get('document_type', 'N/A')}")
    st.markdown("**Sections to Analyze:**")
    for section in law_content.get("sections_to_analyze", []):
        st.markdown(f"- **Title**: {section.get('title', 'N/A')} | **Content**: {section.get('content', 'N/A')} | **Reference**: {section.get('reference', 'N/A')}")

    st.markdown(f"**Legal Issues**: {', '.join(law_content.get('legal_issues', []))}")
    st.markdown(f"**Applicable Laws**: {', '.join(law_content.get('applicable_laws', []))}")
    st.markdown(f"**Analysis Depth**: {law_content.get('analysis_depth', 'N/A')}")

    # Legal Actions Suggestions Output
    st.markdown("#### 💡 Legal Actions Suggestions Output")
    legal_actions_suggestions = result.get("legal_actions_suggestions_output", {})
    st.markdown(f"**Scenario**: {legal_actions_suggestions.get('scenario', 'N/A')}")

    st.markdown("**Goals:**")
    for goal in legal_actions_suggestions.get("goals", []):
        st.markdown(f"- {goal}")

    st.markdown("**Risks:**")
    for risk in legal_actions_suggestions.get("risks", []):
        st.markdown(f"- **Type**: {risk.get('type', 'N/A')} | **Severity**: {risk.get('severity', 'N/A')} | **Mitigation Suggestions**: {', '.join(risk.get('mitigation_suggestions', []))}")

    st.markdown(f"**Resources**: {', '.join(legal_actions_suggestions.get('resources', []))}")
    st.markdown(f"**Previous Attempts**: {', '.join(legal_actions_suggestions.get('previous_attempts', []))}")
    st.markdown(f"**Timeline**: {legal_actions_suggestions.get('timeline', 'N/A')}")
    st.markdown(f"**Constraints**: {', '.join(legal_actions_suggestions.get('constraints', []))}")

    # Legal Actions Evaluation Output
    st.markdown("#### 🧾 Legal Actions Evaluation Output")
    legal_actions_evaluation = result.get("legal_actions_evaluation_output", {})
    st.markdown("**Actions:**")
    for action in legal_actions_evaluation.get("actions", []):
        st.markdown(f"- {action}")

    st.markdown(f"**Evaluation Criteria**: {', '.join(legal_actions_evaluation.get('evaluation_criteria', []))}")

    st.markdown("**Risks:**")
    for risk in legal_actions_evaluation.get("risks", []):
        st.markdown(f"- **Type**: {risk.get('type', 'N/A')} | **Severity**: {risk.get('severity', 'N/A')} | **Mitigation Suggestions**: {', '.join(risk.get('mitigation_suggestions', []))}")

    st.markdown("**Outcomes:**")
    for outcome in legal_actions_evaluation.get("outcomes", []):
        st.markdown(f"- **Description**: {outcome.get('description', 'N/A')} | **Likelihood**: {outcome.get('likelihood', 'N/A')} | **Benefits**: {', '.join(outcome.get('benefits', []))} | **Dependencies**: {', '.join(outcome.get('dependencies', []))}")

    st.markdown(f"**Legal Compliance**: {', '.join(legal_actions_evaluation.get('legal_compliance', []))}")
    st.markdown(f"**Stakeholder Impact**: {', '.join(legal_actions_evaluation.get('stakeholder_impact', []))}")
    st.markdown(f"**Prioritization**: {', '.join(legal_actions_evaluation.get('prioritization', []))}")

    # Additional Attributes
    are_legal_actions_correct = result.get("are_legal_actions_correct", "N/A")
    final_decision = result.get("final_decision", "N/A")

    st.markdown(f"#### ✅ Are Legal Actions Correct: {are_legal_actions_correct}")
    st.markdown(f"#### 🏛️ Final Decision: {final_decision}")

    # Download buttons for JSON and Markdown
    st.markdown("### 💾 Download Results")

    # JSON output
    filtered_data = {key: value for key, value in result.items() if key != 'context'}
    json_result = json.dumps(filtered_data, indent=2)
    st.download_button(
        label="💾 Download JSON",
        data=json_result,
        file_name="legal_analysis.json",
        mime="application/json",
        key="json_download_button"
    )

    # Markdown output
    md_result = convert_to_markdown(result)
    st.download_button(
        label="📜 Download Markdown",
        data=md_result,
        file_name="legal_analysis.md",
        mime="text/markdown",
        key="markdown_download_button"
    )

# Convert result to Markdown format
def convert_to_markdown(result):
    markdown_lines = []

    # Legal Summary Output
    markdown_lines.append("# Legal Summary Output")
    legal_summary = result.get("legal_summary_output", {})
    markdown_lines.append(f"**Context**: {legal_summary.get('context', 'N/A')}")
    markdown_lines.append("**Parties Involved:**")
    for party in legal_summary.get("parties", []):
        markdown_lines.append(f"- **Name**: {party.get('name', 'N/A')} | **Role**: {party.get('role', 'N/A')} | **Contact Info**: {party.get('contact_info', 'N/A')} | **Legal Representative**: {party.get('legal_representative', 'N/A')} | **Stake**: {party.get('stake', 'N/A')}")

    markdown_lines.append("**Relevant Dates:**")
    for date in legal_summary.get("relevant_dates", []):
        markdown_lines.append(f"- **Event**: {date.get('event', 'N/A')} | **Date**: {date.get('date', 'N/A')}")

    markdown_lines.append(f"**Summary Length**: {legal_summary.get('summary_length', 'N/A')} words")
    markdown_lines.append(f"**Jurisdiction**: {legal_summary.get('jurisdiction', 'N/A')}")
    markdown_lines.append(f"**Keywords**: {', '.join(legal_summary.get('keywords', []))}")

    # Law Content Analysis Output
    markdown_lines.append("\n# Law Content Analysis Output")
    law_content = result.get("law_content_analysis_output", {})
    markdown_lines.append(f"**Document ID**: {law_content.get('document_id', 'N/A')}")
    markdown_lines.append(f"**Document Type**: {law_content.get('document_type', 'N/A')}")
    markdown_lines.append("**Sections to Analyze:**")
    for section in law_content.get("sections_to_analyze", []):
        markdown_lines.append(f"- **Title**: {section.get('title', 'N/A')} | **Content**: {section.get('content', 'N/A')} | **Reference**: {section.get('reference', 'N/A')}")

    markdown_lines.append(f"**Legal Issues**: {', '.join(law_content.get('legal_issues', []))}")
    markdown_lines.append(f"**Applicable Laws**: {', '.join(law_content.get('applicable_laws', []))}")
    markdown_lines.append(f"**Analysis Depth**: {law_content.get('analysis_depth', 'N/A')}")

    # Legal Actions Suggestions Output
    markdown_lines.append("\n# Legal Actions Suggestions Output")
    legal_actions_suggestions = result.get("legal_actions_suggestions_output", {})
    markdown_lines.append(f"**Scenario**: {legal_actions_suggestions.get('scenario', 'N/A')}")

    markdown_lines.append("**Goals:**")
    for goal in legal_actions_suggestions.get("goals", []):
        markdown_lines.append(f"- {goal}")

    markdown_lines.append("**Risks:**")
    for risk in legal_actions_suggestions.get("risks", []):
        markdown_lines.append(f"- **Type**: {risk.get('type', 'N/A')} | **Severity**: {risk.get('severity', 'N/A')} | **Mitigation Suggestions**: {', '.join(risk.get('mitigation_suggestions', []))}")

    markdown_lines.append(f"**Resources**: {', '.join(legal_actions_suggestions.get('resources', []))}")
    markdown_lines.append(f"**Previous Attempts**: {', '.join(legal_actions_suggestions.get('previous_attempts', []))}")
    markdown_lines.append(f"**Timeline**: {legal_actions_suggestions.get('timeline', 'N/A')}")
    markdown_lines.append(f"**Constraints**: {', '.join(legal_actions_suggestions.get('constraints', []))}")

    # Legal Actions Evaluation Output
    markdown_lines.append("\n# Legal Actions Evaluation Output")
    legal_actions_evaluation = result.get("legal_actions_evaluation_output", {})
    markdown_lines.append("**Actions:**")
    for action in legal_actions_evaluation.get("actions", []):
        markdown_lines.append(f"- {action}")

    markdown_lines.append(f"**Evaluation Criteria**: {', '.join(legal_actions_evaluation.get('evaluation_criteria', []))}")

    markdown_lines.append("**Risks:**")
    for risk in legal_actions_evaluation.get("risks", []):
        markdown_lines.append(f"- **Type**: {risk.get('type', 'N/A')} | **Severity**: {risk.get('severity', 'N/A')} | **Mitigation Suggestions**: {', '.join(risk.get('mitigation_suggestions', []))}")

    markdown_lines.append("**Outcomes:**")
    for outcome in legal_actions_evaluation.get("outcomes", []):
        markdown_lines.append(f"- **Description**: {outcome.get('description', 'N/A')} | **Likelihood**: {outcome.get('likelihood', 'N/A')} | **Benefits**: {', '.join(outcome.get('benefits', []))} | **Dependencies**: {', '.join(outcome.get('dependencies', []))}")

    markdown_lines.append(f"**Legal Compliance**: {', '.join(legal_actions_evaluation.get('legal_compliance', []))}")
    markdown_lines.append(f"**Stakeholder Impact**: {', '.join(legal_actions_evaluation.get('stakeholder_impact', []))}")
    markdown_lines.append(f"**Prioritization**: {', '.join(legal_actions_evaluation.get('prioritization', []))}")

    # Additional Attributes
    are_legal_actions_correct = result.get("are_legal_actions_correct", "N/A")
    final_decision = result.get("final_decision", "N/A")

    markdown_lines.append("\n# Additional Information")
    markdown_lines.append(f"Are Legal Actions Correct: {are_legal_actions_correct}")
    markdown_lines.append(f"Final Decision: {final_decision}")

    return "\n".join(markdown_lines)

if __name__ == "__main__":
    main()
