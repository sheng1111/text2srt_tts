#!/usr/bin/env python3
"""
Main entry point for Streamlit Cloud deployment.
This file serves as a compatibility layer between Streamlit Cloud and the local app structure.
"""

import os
import sys
import streamlit as st

# Add the app directory to Python path for module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "app")
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import and run the main GUI application
try:
    # Import the GUI module
    from app.ui import gui

    # The GUI module will execute automatically when imported
    # since it contains the main Streamlit application code

except ImportError as e:
    st.error(f"""
    Failed to import the application modules: {e}

    This error typically occurs when the module structure is not recognized.
    Please ensure all necessary files are present in the deployment.
    """)
    st.stop()
except Exception as e:
    st.error(f"""
    An unexpected error occurred while starting the application: {e}

    Please check the logs for more detailed error information.
    """)
    st.stop()
