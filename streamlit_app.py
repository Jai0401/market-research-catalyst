import streamlit as st
import os
import subprocess
import markdown2
import pdfkit

# Title and description
st.title("Multi-Agent Project Frontend")
st.write("This app runs the multi-agent system, displays outputs in markdown format, and allows downloads as PDF or Markdown.")

# Sidebar: Option to run the pipeline
if st.sidebar.button("Run Pipeline"):
    st.sidebar.write("Running pipeline (this might take a moment)...")
    result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    st.sidebar.text_area("Pipeline Output", result.stdout)
    if result.returncode == 0:
        st.sidebar.success("Pipeline completed successfully!")
    else:
        st.sidebar.error("Pipeline failed:\n" + result.stderr)

# Sidebar: Select which output file to view
st.sidebar.markdown("## View Output Files")
output_options = {
    "Final Proposal": "final_proposal.md",
    "Use Cases": "use_cases.md",
    "Resource Links": "resource_links.md"
}
selected_label = st.sidebar.selectbox("Select an output file", list(output_options.keys()))
selected_file = output_options[selected_label]
file_path = os.path.join("output", selected_file)

# Read and display the file if it exists
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    st.markdown(f"### {selected_label}", unsafe_allow_html=True)
    st.markdown(content, unsafe_allow_html=True)
    
    # Provide download button for the markdown file
    st.download_button(
        label="Download Markdown",
        data=content,
        file_name=selected_file,
        mime="text/markdown"
    )
    
    # Convert markdown to PDF and provide download button
    try:
        # Convert markdown to HTML
        html_content = markdown2.markdown(content)
        # Convert HTML to PDF (requires wkhtmltopdf installed)
        pdf_data = pdfkit.from_string(html_content, False)
        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name=selected_file.replace(".md", ".pdf"),
            mime="application/pdf"
        )
    except Exception as e:
        st.error("PDF conversion not available. Please ensure pdfkit and wkhtmltopdf are installed. Error: " + str(e))
else:
    st.error(f"File {selected_file} not found in the 'output' directory.")
