import streamlit as st
import subprocess
from datetime import datetime
import os

# Streamlit page config
st.set_page_config(page_title="Nmap Scanner", page_icon="🛡️", layout="centered")

st.title("🛡️ Nmap Port Scanner")
st.subheader("Securely scan open ports on a server or device.")

# Input field
target = st.text_input("🔍 Enter IP Address or Domain to Scan:")

if st.button("🚀 Start Scan"):
    if target:
        with st.spinner('Scanning in progress...'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"nmap_result_{timestamp}.txt"

            try:
                # Run Nmap
                result = subprocess.run(
                    ["nmap", "-Pn", "-T4", target],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    st.success("✅ Scan Completed Successfully!")

                    # Show output
                    st.text_area("📋 Nmap Scan Result:", result.stdout, height=400)

                    # Save result to file
                    with open(output_filename, "w", encoding="utf-8") as f:
                        f.write(result.stdout)

                    # Allow download
                    with open(output_filename, "rb") as f:
                        st.download_button(
                            label="📥 Download Scan Report",
                            data=f,
                            file_name=output_filename,
                            mime="text/plain"
                        )
                else:
                    st.error("❌ Nmap Scan Failed!")
                    st.text(result.stderr)

            except FileNotFoundError:
                st.error("⚠️ Error: Nmap is not installed or not found in system PATH.")
            except Exception as e:
                st.error(f"⚡ Unexpected Error: {e}")
    else:
        st.warning("⚠️ Please enter a valid IP address or hostname.")
