#!/usr/bin/env python3
"""
Simple Context Management UI
A clean, user-friendly interface for managing our context system
"""

import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our context system
try:
    from context_manager import SeamlessContextManager
    CONTEXT_SYSTEM_AVAILABLE = True
except ImportError as e:
    st.error(f"Context system not available: {e}")
    st.info("💡 Make sure all dependencies are installed: pip install -r requirements_ui.txt")
    CONTEXT_SYSTEM_AVAILABLE = False

try:
    from models_local import get_database_url, get_session_factory
    MODELS_AVAILABLE = True
except ImportError as e:
    st.warning(f"Models not available: {e}")
    MODELS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Context Manager",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Global font size increase and better contrast */
    * {
        font-size: 18px !important;
        line-height: 1.7 !important;
    }
    
    /* Force ALL backgrounds to be dark/colored - ULTIMATE OVERRIDE */
    html, body, #root, .stApp, .main, .main .block-container,
    [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] *,
    [data-testid="stSidebar"], [data-testid="stSidebar"] *,
    .stApp > div, .stApp > div *,
    .main > div, .main > div * {
        background: linear-gradient(135deg, #0f172a, #1e293b) !important;
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    
    /* Main header with better contrast */
    .main-header {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem !important;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0;
        text-shadow: none;
    }
    
    /* Section headers with better contrast */
    .section-header {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem !important;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid #475569;
    }
    
    /* Metric cards with dark theme and better contrast */
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        border: 1px solid #475569 !important;
        border-radius: 16px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        color: #f8fafc !important;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.4);
        border-color: #64748b;
        background: linear-gradient(135deg, #334155, #475569) !important;
    }
    
    /* Status indicators with better contrast */
    .status-success { 
        background: linear-gradient(135deg, #059669, #047857);
        color: white !important;
        padding: 0.75rem 1.5rem;
        border-radius: 16px;
        font-weight: 600;
        font-size: 18px !important;
        box-shadow: 0 3px 10px rgba(5, 150, 105, 0.3);
        border: 1px solid #047857;
    }
    
    .status-warning { 
        background: linear-gradient(135deg, #d97706, #b45309);
        color: white !important;
        padding: 0.75rem 1.5rem;
        border-radius: 16px;
        font-weight: 600;
        font-size: 18px !important;
        box-shadow: 0 3px 10px rgba(217, 119, 6, 0.3);
        border: 1px solid #b45309;
    }
    
    .status-error { 
        background: linear-gradient(135deg, #dc2626, #b91c1c);
        color: white !important;
        padding: 0.75rem 1.5rem;
        border-radius: 16px;
        font-weight: 600;
        font-size: 18px !important;
        box-shadow: 0 3px 10px rgba(220, 38, 38, 0.3);
        border: 1px solid #b91c1c;
    }
    
    /* COMPREHENSIVE SIDEBAR STYLING - Dark theme with subtle accents */
    .sidebar, .sidebar .sidebar-content, 
    [data-testid="stSidebar"], [data-testid="stSidebar"] *,
    .css-1d391kg, .css-1d391kg *,
    .css-1cypcdb, .css-1cypcdb *,
    .css-17eq0hr, .css-17eq0hr * {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }
    
    /* Force ALL sidebar text to be readable with larger fonts */
    .sidebar *, .sidebar .sidebar-content *, 
    [data-testid="stSidebar"] *, 
    .css-1d391kg *, .css-1cypcdb *, .css-17eq0hr * {
        color: #f8fafc !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        background-color: transparent !important;
    }
    
    /* Force sidebar navigation elements with better styling */
    .sidebar .sidebar-nav, .sidebar .sidebar-nav *,
    .sidebar .sidebar-nav a, .sidebar .sidebar-nav button {
        color: #f8fafc !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #334155, #475569) !important;
        border: 1px solid #64748b !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.25rem !important;
        margin: 0.5rem 0 !important;
        text-decoration: none !important;
    }
    
    .sidebar .sidebar-nav a:hover, .sidebar .sidebar-nav button:hover {
        background: linear-gradient(135deg, #475569, #64748b) !important;
        color: #f8fafc !important;
        transform: translateX(3px) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Main app styling - DARK THEME */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b) !important;
        min-height: 100vh;
    }
    
    .main .block-container {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        border-radius: 20px;
        border: 1px solid #475569 !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        margin: 2rem;
        padding: 2.5rem;
    }
    
    /* Force better contrast for all content with larger fonts */
    .main .block-container * {
        color: #f8fafc !important;
        font-size: 18px !important;
    }
    
    /* Override any Streamlit default colors */
    .stMarkdown, .stText, .stDataFrame, .stPlotlyChart {
        color: #f8fafc !important;
        font-size: 18px !important;
    }
    
    /* Tabs with better styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.95);
        border-radius: 16px;
        padding: 0.75rem;
        border: 1px solid #475569;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #cbd5e1 !important;
        background: transparent;
        border-radius: 12px;
        margin: 0.25rem;
        transition: all 0.3s ease;
        border: 1px solid transparent;
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.25rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #475569, #64748b) !important;
        color: #f8fafc !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
        border-color: #64748b !important;
    }
    
    /* Force ALL text to be large, light, and readable */
    * {
        color: #f8fafc !important;
        font-size: 18px !important;
        line-height: 1.7 !important;
    }
    
    /* Force ALL backgrounds to be dark */
    body, html, .stApp, .main, .main .block-container, .sidebar, .sidebar .sidebar-content {
        background: linear-gradient(135deg, #0f172a, #1e293b) !important;
        background-color: #0f172a !important;
    }
    
    /* Force Streamlit sidebar to be dark - COMPREHENSIVE TARGETING */
    [data-testid="stSidebar"], [data-testid="stSidebar"] *,
    .css-1d391kg, .css-1d391kg *,
    .css-1cypcdb, .css-1cypcdb *,
    .css-17eq0hr, .css-17eq0hr *,
    .css-1v0mbdj, .css-1v0mbdj *,
    .css-1lcbmhc, .css-1lcbmhc *,
    .css-1wivap2, .css-1wivap2 *,
    .css-1p05t8e, .css-1p05t8e *,
    .css-1r6slb0, .css-1r6slb0 *,
    .css-1y4p8zc, .css-1y4p8zc * {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        background-color: #1e293b !important;
        color: #f8fafc !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    /* Force ALL sidebar-like elements to be dark */
    div[class*="sidebar"], div[class*="nav"], div[class*="menu"] {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }
    
    /* Force all text containers with maximum readability */
    div, p, span, label, strong, em, b, i, a, li, td, th {
        color: #f8fafc !important;
        font-size: 18px !important;
        line-height: 1.7 !important;
        font-weight: 500 !important;
    }
    
    /* Force all Streamlit components with maximum readability */
    .stMarkdown, .stMarkdown *, .stText, .stText *, 
    .stDataFrame, .stDataFrame *, .stPlotlyChart, .stPlotlyChart *,
    .stMetric, .stMetric *, .stAlert, .stAlert *,
    .streamlit-expanderHeader, .streamlit-expanderContent,
    .stSelectbox, .stSelectbox *, .stTextArea, .stTextArea *,
    .stSlider, .stSlider *, .stCheckbox, .stCheckbox *,
    .stTable, .stTable *, .stButton, .stButton * {
        color: #f8fafc !important;
        font-size: 18px !important;
        line-height: 1.7 !important;
        font-weight: 500 !important;
    }
    
    /* Fix metrics with better contrast and larger text */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        color: #f8fafc !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        border: 1px solid #475569 !important;
        margin: 1rem 0 !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="metric-container"] * {
        color: #f8fafc !important;
        font-size: 18px !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #f8fafc !important;
        font-weight: bold !important;
        font-size: 2rem !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-label"] {
        font-size: 20px !important;
        font-weight: 600 !important;
    }
    
    /* Fix all headers aggressively with better contrast */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f8fafc !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
        font-size: 24px !important;
    }
    
    h1 { font-size: 32px !important; }
    h2 { font-size: 28px !important; }
    h3 { font-size: 24px !important; }
    
    /* Fix info/warning/error boxes with better contrast */
    [data-testid="stAlert"] {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        font-size: 18px !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="stAlert"] * {
        color: #f8fafc !important;
        font-size: 18px !important;
    }
    
    /* Fix expanders with better contrast */
    [data-testid="expanderHeader"] {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 16px !important;
        font-weight: bold !important;
        padding: 1rem !important;
        font-size: 20px !important;
    }
    
    [data-testid="expanderHeader"] * {
        color: #f8fafc !important;
        font-size: 20px !important;
    }
    
    [data-testid="expanderContent"] {
        background: linear-gradient(135deg, #334155, #475569) !important;
        border: 1px solid #64748b !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        color: #f8fafc !important;
        font-size: 18px !important;
    }
    
    /* Fix selectboxes and text areas with better contrast */
    .stSelectbox > div > div,
    .stTextArea textarea,
    .stTextInput input {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        padding: 1rem !important;
    }
    
    .stSelectbox > div > div:hover,
    .stTextArea textarea:hover,
    .stTextInput input:hover {
        border-color: #64748b !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Fix buttons with better styling */
    .stButton > button {
        background: linear-gradient(135deg, #475569, #64748b) !important;
        color: #f8fafc !important;
        border: 1px solid #64748b !important;
        border-radius: 16px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 1rem 2rem !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4) !important;
        border-color: #94a3b8 !important;
        background: linear-gradient(135deg, #64748b, #94a3b8) !important;
    }
    
    /* Fix tables with MUCH BETTER contrast - NO MORE BLUE BORDERS */
    .stTable {
        background: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stTable table {
        font-size: 18px !important;
        width: 100% !important;
    }
    
    .stTable th {
        background: #334155 !important;
        color: #f8fafc !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        padding: 1.5rem !important;
        border-bottom: 2px solid #475569 !important;
        text-align: left !important;
    }
    
    .stTable td {
        background: #1e293b !important;
        color: #f8fafc !important;
        font-size: 18px !important;
        padding: 1.5rem !important;
        border-bottom: 1px solid #334155 !important;
        line-height: 1.6 !important;
    }
    
    .stTable tr:hover td {
        background: #334155 !important;
        color: #f8fafc !important;
    }
    
    /* Fix checkboxes and sliders */
    .stCheckbox > label {
        color: #f8fafc !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #475569, #64748b) !important;
    }
    
    /* Custom component styling - NO MORE BLUE BORDERS */
    .prompt-comparison {
        background: linear-gradient(135deg, #334155, #475569) !important;
        border: 1px solid #64748b;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        color: #f8fafc;
        font-size: 18px;
    }
    
    .original-prompt {
        background: linear-gradient(135deg, #451a03, #78350f) !important;
        border: 1px solid #d97706;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        color: #f8fafc;
        font-size: 18px;
    }
    
    .enhanced-prompt {
        background: linear-gradient(135deg, #1e3a8a, #3730a3) !important;
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        color: #f8fafc;
        font-size: 18px;
    }
    
    .context-details {
        background: linear-gradient(135deg, #334155, #475569) !important;
        border: 1px solid #64748b;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        color: #f8fafc;
        font-size: 18px;
    }
    
    .pipeline-step {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        border-left: 3px solid #64748b;
        color: #f8fafc;
        font-size: 18px;
    }
    
    .pipeline-step:hover {
        transform: translateX(3px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.4);
        border-color: #94a3b8;
        background: linear-gradient(135deg, #334155, #475569) !important;
    }
    
    /* Enhanced text styling */
    .enhanced-text {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 20px !important;
    }
    
    /* Fix any remaining Streamlit elements */
    .stMarkdown p {
        font-size: 18px !important;
        line-height: 1.7 !important;
        color: #f8fafc !important;
        margin-bottom: 1rem !important;
    }
    
    .stMarkdown code {
        background: #0f172a !important;
        color: #f8fafc !important;
        padding: 0.5rem !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        border: 1px solid #475569 !important;
    }
    
    /* Plotly chart improvements */
    .js-plotly-plot {
        border: 1px solid #475569 !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        background: linear-gradient(135deg, #1e293b, #334155) !important;
    }
    
    /* ULTIMATE CHART/GRAPH FIX - Make all charts visible on dark theme */
    /* Plotly charts */
    .plotly-graph-div, .plotly-graph-div *,
    .js-plotly-plot, .js-plotly-plot *,
    [data-testid="stPlotlyChart"], [data-testid="stPlotlyChart"] * {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #475569 !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Force chart backgrounds to be white for visibility */
    .plotly-graph-div svg, .js-plotly-plot svg,
    [data-testid="stPlotlyChart"] svg {
        background: #ffffff !important;
        color: #0f172a !important;
    }
    
    /* Chart text elements */
    .plotly-graph-div text, .js-plotly-plot text,
    [data-testid="stPlotlyChart"] text {
        fill: #0f172a !important;
        color: #0f172a !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    
    /* Chart axes and labels */
    .plotly-graph-div .xtick text, .plotly-graph-div .ytick text,
    .js-plotly-plot .xtick text, .js-plotly-plot .ytick text,
    [data-testid="stPlotlyChart"] .xtick text, [data-testid="stPlotlyChart"] .ytick text {
        fill: #0f172a !important;
        color: #0f172a !important;
        font-size: 12px !important;
    }
    
    /* Chart titles */
    .plotly-graph-div .gtitle, .js-plotly-plot .gtitle,
    [data-testid="stPlotlyChart"] .gtitle {
        fill: #0f172a !important;
        color: #0f172a !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Chart legends */
    .plotly-graph-div .legend, .js-plotly-plot .legend,
    [data-testid="stPlotlyChart"] .legend {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #475569 !important;
    }
    
    /* Chart legend text */
    .plotly-graph-div .legend text, .js-plotly-plot .legend text,
    [data-testid="stPlotlyChart"] .legend text {
        fill: #0f172a !important;
        color: #0f172a !important;
    }
    
    /* Chart grid lines */
    .plotly-graph-div .gridlayer, .js-plotly-plot .gridlayer,
    [data-testid="stPlotlyChart"] .gridlayer {
        background: #ffffff !important;
    }
    
    /* Chart hover elements */
    .plotly-graph-div .hoverlayer, .js-plotly-plot .hoverlayer,
    [data-testid="stPlotlyChart"] .hoverlayer {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #0f172a !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        font-size: 12px !important;
    }
    
    /* Force all chart containers to be visible */
    div[class*="plotly"], div[class*="Plotly"],
    div[class*="chart"], div[class*="Chart"],
    div[class*="graph"], div[class*="Graph"] {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #475569 !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Force chart text to be readable */
    div[class*="plotly"] *, div[class*="Plotly"] *,
    div[class*="chart"] *, div[class*="Chart"] *,
    div[class*="graph"] *, div[class*="Graph"] * {
        color: #0f172a !important;
        font-size: 14px !important;
    }
    
    /* Streamlit specific chart containers */
    [data-testid="stPlotlyChart"], [data-testid="stPlotlyChart"] *,
    [data-testid="stChart"], [data-testid="stChart"] *,
    [data-testid="stGraph"], [data-testid="stGraph"] * {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #475569 !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Force chart text in Streamlit containers */
    [data-testid="stPlotlyChart"] text, [data-testid="stChart"] text, [data-testid="stGraph"] text {
        fill: #0f172a !important;
        color: #0f172a !important;
        font-size: 14px !important;
    }
    
    /* Chart axes labels */
    [data-testid="stPlotlyChart"] .xtick text, [data-testid="stPlotlyChart"] .ytick text,
    [data-testid="stChart"] .xtick text, [data-testid="stChart"] .ytick text,
    [data-testid="stGraph"] .xtick text, [data-testid="stGraph"] .ytick text {
        fill: #0f172a !important;
        color: #0f172a !important;
        font-size: 12px !important;
    }
    
    /* Chart titles in Streamlit */
    [data-testid="stPlotlyChart"] .gtitle, [data-testid="stChart"] .gtitle, [data-testid="stGraph"] .gtitle {
        fill: #0f172a !important;
        color: #0f172a !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Chart legends in Streamlit */
    [data-testid="stPlotlyChart"] .legend, [data-testid="stChart"] .legend, [data-testid="stGraph"] .legend {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #475569 !important;
    }
    
    /* Chart legend text in Streamlit */
    [data-testid="stPlotlyChart"] .legend text, [data-testid="stChart"] .legend text, [data-testid="stGraph"] .legend text {
        fill: #0f172a !important;
        color: #0f172a !important;
    }
    
    /* Chart hover elements in Streamlit */
    [data-testid="stPlotlyChart"] .hoverlayer, [data-testid="stChart"] .hoverlayer, [data-testid="stGraph"] .hoverlayer {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #0f172a !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        font-size: 12px !important;
    }
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        * {
            font-size: 20px !important;
        }
        
        .main-header {
            font-size: 2.5rem !important;
        }
        
        .section-header {
            font-size: 1.8rem !important;
        }
    }
    
    /* Force chart text to be visible */
    .js-plotly-plot text, .plotly-graph-div text, [data-testid="stPlotlyChart"] text {
        fill: #000000 !important;
        color: #000000 !important;
    }
</style>

<script>
// Force dark theme on ALL elements
function forceDarkTheme() {
    // Force dark backgrounds everywhere
    const allElements = document.querySelectorAll('*');
    allElements.forEach(el => {
        if (el.tagName && !['SCRIPT', 'STYLE'].includes(el.tagName)) {
            // Force dark background
            el.style.setProperty('background', 'linear-gradient(135deg, #0f172a, #1e293b)', 'important');
            el.style.setProperty('background-color', '#0f172a', 'important');
            
            // Force light text
            el.style.setProperty('color', '#f8fafc', 'important');
            
            // Force larger fonts
            el.style.setProperty('font-size', '18px', 'important');
        }
    });
    
    // Force specific Streamlit containers
    const streamlitContainers = document.querySelectorAll('[data-testid]');
    streamlitContainers.forEach(el => {
        el.style.setProperty('background', 'linear-gradient(135deg, #1e293b, #334155)', 'important');
        el.style.setProperty('color', '#f8fafc', 'important');
    });
    
    // Force main app background
    const stApp = document.querySelector('.stApp');
    if (stApp) {
        stApp.style.setProperty('background', 'linear-gradient(135deg, #0f172a, #1e293b)', 'important');
    }
    
    // Force sidebar background
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.setProperty('background', 'linear-gradient(135deg, #1e293b, #334155)', 'important');
    }
    
    // Force main container background
    const mainContainer = document.querySelector('.main .block-container');
    if (mainContainer) {
        mainContainer.style.setProperty('background', 'linear-gradient(135deg, #1e293b, #334155)', 'important');
    }
}

// Run immediately and continuously
forceDarkTheme();
setInterval(forceDarkTheme, 500);

// Also run on DOM changes
const observer = new MutationObserver(forceDarkTheme);
observer.observe(document.body, { childList: true, subtree: true });

// Run when page loads
document.addEventListener('DOMContentLoaded', forceDarkTheme);
window.addEventListener('load', forceDarkTheme);
</script>
""", unsafe_allow_html=True)

def init_database_connection():
    """Initialize database connection"""
    try:
        db_path = Path("./data/agent_tracker_local.db")
        if not db_path.exists():
            st.warning("Database not found. Please ensure the context system is running.")
            return None
        
        conn = sqlite3.connect(str(db_path))
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

def get_system_stats(conn):
    """Get system statistics from database"""
    if not conn:
        return {}
    
    try:
        # Basic counts
        interactions_count = pd.read_sql("SELECT COUNT(*) as count FROM agent_interactions", conn).iloc[0]['count']
        sessions_count = pd.read_sql("SELECT COUNT(*) as count FROM sessions", conn).iloc[0]['count']
        contexts_count = pd.read_sql("SELECT COUNT(*) as count FROM conversation_contexts", conn).iloc[0]['count']
        
        # Recent activity
        recent_interactions = pd.read_sql("""
            SELECT COUNT(*) as count FROM agent_interactions 
            WHERE timestamp > datetime('now', '-1 hour')
        """, conn).iloc[0]['count']
        
        # Error rate
        error_count = pd.read_sql("""
            SELECT COUNT(*) as count FROM agent_interactions 
            WHERE status = 'error'
        """, conn).iloc[0]['count']
        
        return {
            'total_interactions': interactions_count,
            'total_sessions': sessions_count,
            'total_contexts': contexts_count,
            'recent_activity': recent_interactions,
            'error_rate': error_count
        }
    except Exception as e:
        st.error(f"Error getting stats: {e}")
        return {}

def get_recent_interactions(conn, limit=10):
    """Get recent interactions"""
    if not conn:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                id, timestamp, session_id, interaction_type, 
                status, execution_time_ms,
                LENGTH(prompt) as prompt_length,
                LENGTH(response) as response_length
            FROM agent_interactions 
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        return pd.read_sql(query, conn, params=(limit,))
    except Exception as e:
        st.error(f"Error getting interactions: {e}")
        return pd.DataFrame()

def get_session_summary(conn):
    """Get session summary"""
    if not conn:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                id, user_id, started_at, last_activity, 
                total_interactions,
                current_context_id
            FROM sessions 
            ORDER BY last_activity DESC
        """
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error getting sessions: {e}")
        return pd.DataFrame()

def get_context_summary(conn):
    """Get context summary"""
    if not conn:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                id, session_id, context_type, created_at, 
                relevance_score, usage_count, last_used
            FROM conversation_contexts 
            ORDER BY created_at DESC
        """
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error getting contexts: {e}")
        return pd.DataFrame()

def get_prompt_data(conn, limit=20):
    """Get detailed prompt data including original and enhanced versions"""
    if not conn:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                id, timestamp, session_id, interaction_type, 
                prompt as original_prompt, response, full_content,
                context_summary, semantic_keywords, topic_category,
                context_relevance_score, parameters, meta_data,
                conversation_context
            FROM agent_interactions 
            WHERE prompt IS NOT NULL AND prompt != ''
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        return pd.read_sql(query, conn, params=(limit,))
    except Exception as e:
        st.error(f"Error getting prompt data: {e}")
        return pd.DataFrame()

def get_context_injection_details(conn, interaction_id):
    """Get detailed context injection information for a specific interaction"""
    if not conn:
        return {}
    
    try:
        # Get the interaction details
        query = """
            SELECT 
                prompt, response, full_content, context_summary,
                semantic_keywords, topic_category, context_relevance_score,
                conversation_context, meta_data, parameters
            FROM agent_interactions 
            WHERE id = ?
        """
        result = pd.read_sql(query, conn, params=(interaction_id,))
        
        if result.empty:
            return {}
        
        interaction = result.iloc[0]
        
        # Get related context objects
        context_query = """
            SELECT 
                context_summary, semantic_context, key_topics,
                user_preferences, project_context, context_type,
                relevance_score, usage_count
            FROM conversation_contexts 
            WHERE id IN (
                SELECT context_id FROM conversation_contexts 
                WHERE related_interactions LIKE '%' || ? || '%'
            )
        """
        contexts = pd.read_sql(context_query, conn, params=(interaction_id,))
        
        return {
            'interaction': interaction.to_dict(),
            'related_contexts': contexts.to_dict('records') if not contexts.empty else []
        }
    except Exception as e:
        st.error(f"Error getting context injection details: {e}")
        return {}

def simulate_prompt_enhancement(original_prompt, session_id=None):
    """Simulate how a prompt would be enhanced with context injection"""
    # This is a simulation - in real usage, you'd call the actual context injection system
    enhanced_prompt = f"""=== ENHANCED PROMPT GENERATED BY CONTEXT SYSTEM ===

USER MESSAGE: {original_prompt}

=== CONTEXT INJECTION ===

CONVERSATION SUMMARY:
Current conversation state: Active session with context-aware interactions. Recent topics: Context management, prompt enhancement, UI development.

ACTION HISTORY:
Recent actions: User requested prompt visibility features, exploring context injection system, analyzing conversation data.

TECH STACK:
Python 3.x, SQLite database, MCP (Model Context Protocol), Streamlit UI, SQLAlchemy ORM, Context injection system.

PROJECT PLANS & OBJECTIVES:
1. Build powerful conversation tracking system ✅
2. Implement context-aware prompt processing ✅
3. Create intelligent memory management system ✅
4. Add full prompt visibility to UI 🔄
5. Enhance real-time context injection 🔄

USER PREFERENCES:
- Prefer local SQLite over PostgreSQL for development
- Focus on conversation context and memory
- Want full visibility into prompt processing
- Prefer simple yet powerful solutions

AGENT METADATA:
- System: MCP Conversation Intelligence
- Capabilities: Context injection, conversation tracking, prompt enhancement
- Status: Active with enhanced context awareness

=== INSTRUCTIONS ===
Please respond to the user's message above, taking into account:
1. The current conversation context and recent interactions
2. The specific actions and steps taken so far
3. The technical stack and capabilities available
4. The project goals and objectives
5. The user's stated preferences and requirements
6. The agent's capabilities and current state

Provide a comprehensive, context-aware response that builds upon our conversation history.
=== END ENHANCED PROMPT ==="""
    
    return enhanced_prompt

def show_prompt_visibility(conn):
    """Show prompt visibility and context injection details"""
    st.markdown('<div class="section-header">🔍 Prompt Visibility & Context Injection</div>', unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Prompt Overview", 
        "🔄 Live Enhancement", 
        "📋 Detailed Analysis",
        "🧠 Context Pipeline"
    ])
    
    with tab1:
        st.markdown('<div class="section-header">📊 Prompt Processing Overview</div>', unsafe_allow_html=True)
        
        # Filters
        st.markdown("**Configure your view:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            prompt_limit = st.slider("Show last N prompts", 10, 100, 20)
        with col2:
            show_enhanced = st.checkbox("Show enhanced prompts", True)
        with col3:
            show_context = st.checkbox("Show context details", True)
        
        # Get prompt data
        prompts = get_prompt_data(conn, prompt_limit)
        
        if prompts.empty:
            st.info("No prompts found in the database")
            return
        
        # Display prompts with enhancement simulation
        for _, prompt_row in prompts.iterrows():
            with st.expander(f"📝 {prompt_row['interaction_type']} - {prompt_row['timestamp']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Original Prompt:**")
                    st.markdown(f'<div class="original-prompt">{prompt_row["original_prompt"]}</div>', unsafe_allow_html=True)
                    
                    if show_context and prompt_row['context_summary']:
                        st.markdown("**Context Summary:**")
                        st.info(prompt_row['context_summary'])
                
                with col2:
                    if show_enhanced:
                        st.markdown("**Enhanced Prompt:**")
                        enhanced = simulate_prompt_enhancement(prompt_row['original_prompt'])
                        st.markdown(f'<div class="enhanced-prompt">{enhanced}</div>', unsafe_allow_html=True)
                    
                    if show_context and prompt_row['semantic_keywords']:
                        st.markdown("**Semantic Keywords:**")
                        try:
                            keywords = json.loads(prompt_row['semantic_keywords']) if prompt_row['semantic_keywords'] else []
                            if keywords:
                                st.write(", ".join(keywords))
                        except:
                            st.write(prompt_row['semantic_keywords'])
                
                # Additional metadata
                if show_context:
                    col3, col4, col5 = st.columns(3)
                    with col3:
                        st.metric("Relevance Score", f"{prompt_row['context_relevance_score']:.2f}" if prompt_row['context_relevance_score'] else "N/A")
                    with col4:
                        st.metric("Topic Category", prompt_row['topic_category'] or "N/A")
                    with col5:
                        st.metric("Prompt Length", len(prompt_row['original_prompt']))
    
    with tab2:
        st.markdown('<div class="section-header">🔄 Live Prompt Enhancement</div>', unsafe_allow_html=True)
        
        # Input for testing prompt enhancement
        test_prompt = st.text_area(
            "Enter a test prompt to see how it would be enhanced:",
            placeholder="Type your prompt here to see real-time context injection...",
            height=100
        )
        
        if test_prompt:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original Prompt:**")
                st.markdown(f'<div class="original-prompt">{test_prompt}</div>', unsafe_allow_html=True)
                
                # Prompt analysis
                st.markdown("**Prompt Analysis:**")
                st.metric("Length", len(test_prompt))
                st.metric("Words", len(test_prompt.split()))
                
                # Simulate topic detection
                topics = []
                if any(word in test_prompt.lower() for word in ['database', 'sql', 'query']):
                    topics.append("Database")
                if any(word in test_prompt.lower() for word in ['ui', 'interface', 'frontend']):
                    topics.append("User Interface")
                if any(word in test_prompt.lower() for word in ['context', 'memory', 'conversation']):
                    topics.append("Context Management")
                if any(word in test_prompt.lower() for word in ['mcp', 'agent', 'tool']):
                    topics.append("MCP System")
                
                if topics:
                    st.markdown("**Detected Topics:**")
                    for topic in topics:
                        st.write(f"• {topic}")
            
            with col2:
                st.markdown("**Enhanced Prompt:**")
                enhanced = simulate_prompt_enhancement(test_prompt)
                st.markdown(f'<div class="enhanced-prompt">{enhanced}</div>', unsafe_allow_html=True)
                
                # Enhancement metrics
                st.markdown("**Enhancement Metrics:**")
                st.metric("Original Length", len(test_prompt))
                st.metric("Enhanced Length", len(enhanced))
                st.metric("Enhancement Ratio", f"{len(enhanced)/len(test_prompt):.1f}x")
    
    with tab3:
        st.markdown('<div class="section-header">📋 Detailed Context Analysis</div>', unsafe_allow_html=True)
        
        # Select interaction for detailed analysis
        if not prompts.empty:
            selected_interaction = st.selectbox(
                "Select interaction for detailed analysis:",
                prompts['id'].tolist(),
                format_func=lambda x: f"ID {x} - {prompts[prompts['id']==x]['timestamp'].iloc[0]}"
            )
            
            if selected_interaction:
                details = get_context_injection_details(conn, selected_interaction)
                
                if details:
                    interaction = details['interaction']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Interaction Details:**")
                        st.json(interaction)
                    
                    with col2:
                        st.markdown("**Related Contexts:**")
                        if details['related_contexts']:
                            for ctx in details['related_contexts']:
                                with st.expander(f"Context: {ctx.get('context_type', 'Unknown')}", expanded=False):
                                    st.write(f"**Summary:** {ctx.get('context_summary', 'N/A')}")
                                    st.write(f"**Relevance:** {ctx.get('relevance_score', 'N/A')}")
                                    st.write(f"**Usage Count:** {ctx.get('usage_count', 'N/A')}")
                        else:
                            st.info("No related contexts found")
                else:
                    st.warning("Could not retrieve details for this interaction")
    
    with tab4:
        st.markdown('<div class="section-header">🧠 Context Injection Pipeline</div>', unsafe_allow_html=True)
        
        st.markdown("""
        ### How Context Injection Works
        
        The context injection system follows this pipeline to enhance your prompts:
        """)
        
        pipeline_steps = [
            {
                "step": "1. Prompt Reception",
                "description": "User prompt is received and logged",
                "details": "Original prompt is stored with metadata (timestamp, session, type)"
            },
            {
                "step": "2. Context Analysis",
                "description": "System analyzes conversation history and context",
                "details": "Identifies relevant topics, user preferences, and project context"
            },
            {
                "step": "3. Context Selection",
                "description": "Most relevant context is selected based on scoring",
                "details": "Uses relevance scores, recency, and topic matching"
            },
            {
                "step": "4. Context Injection",
                "description": "Selected context is injected into the original prompt",
                "details": "Creates enhanced prompt with conversation summary, tech stack, and preferences"
            },
            {
                "step": "5. Enhanced Response",
                "description": "AI processes the enhanced prompt",
                "details": "Response is context-aware and builds on conversation history"
            },
            {
                "step": "6. Context Update",
                "description": "New interaction updates context system",
                "details": "Learns from this interaction for future context injection"
            }
        ]
        
        for step in pipeline_steps:
            st.markdown(f"""
            <div class="pipeline-step">
                <strong>{step['step']}</strong><br>
                <em>{step['description']}</em><br>
                {step['details']}
            </div>
            """, unsafe_allow_html=True)
        
        # Show current system status
        st.markdown('<div class="section-header">🔧 Current System Status</div>', unsafe_allow_html=True)
        
        if CONTEXT_SYSTEM_AVAILABLE:
            try:
                context_manager = SeamlessContextManager(auto_start=False)
                st.success("✅ Context injection system is available")
                
                # Show available context systems
                st.markdown("**Available Context Systems:**")
                for system_name, system_info in context_manager.context_systems.items():
                    status_icon = "🟢" if system_info['status'] == 'available' else "🔴"
                    st.write(f"{status_icon} **{system_name}**: {system_info['status']}")
                    
                    if system_info['capabilities']:
                        st.write(f"   Capabilities: {', '.join(system_info['capabilities'])}")
            except Exception as e:
                st.error(f"❌ Context system error: {e}")
        else:
            st.error("❌ Context injection system is not available")

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🧠 Context Manager</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Dashboard", "Interactions", "Sessions", "Contexts", "Prompt Visibility", "System Status"]
    )
    
    # Initialize database connection
    conn = init_database_connection()
    
    if page == "Dashboard":
        show_dashboard(conn)
    elif page == "Interactions":
        show_interactions(conn)
    elif page == "Sessions":
        show_sessions(conn)
    elif page == "Contexts":
        show_contexts(conn)
    elif page == "Prompt Visibility":
        show_prompt_visibility(conn)
    elif page == "System Status":
        show_system_status(conn)

def show_dashboard(conn):
    """Show main dashboard"""
    st.markdown('<div class="section-header">📊 System Overview</div>', unsafe_allow_html=True)
    
    # Get system stats
    stats = get_system_stats(conn)
    
    if not stats:
        st.warning("Unable to load system statistics")
        return
    
    # Metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Interactions", stats.get('total_interactions', 0))
    
    with col2:
        st.metric("Active Sessions", stats.get('total_sessions', 0))
    
    with col3:
        st.metric("Context Objects", stats.get('total_contexts', 0))
    
    with col4:
        st.metric("Recent Activity (1h)", stats.get('recent_activity', 0))
    
    with col5:
        error_rate = stats.get('error_rate', 0)
        st.metric("Errors", error_rate, delta=None, delta_color="inverse")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">📈 Activity Timeline</div>', unsafe_allow_html=True)
        if conn:
            try:
                # Get hourly activity for last 24 hours
                query = """
                    SELECT 
                        strftime('%H', timestamp) as hour,
                        COUNT(*) as count
                    FROM agent_interactions 
                    WHERE timestamp > datetime('now', '-1 day')
                    GROUP BY hour
                    ORDER BY hour
                """
                hourly_data = pd.read_sql(query, conn)
                
                if not hourly_data.empty:
                    fig = px.bar(hourly_data, x='hour', y='count', 
                               title="Interactions by Hour (Last 24h)")
                    # Fix chart colors for dark theme visibility
                    fig.update_traces(marker_color='#60a5fa', marker_line_color='#f8fafc', marker_line_width=1)
                    fig.update_layout(
                        plot_bgcolor='#1e293b',
                        paper_bgcolor='#1e293b',
                        font=dict(color='#f8fafc', size=14),
                        xaxis=dict(gridcolor='#475569', zerolinecolor='#64748b', color='#f8fafc'),
                        yaxis=dict(gridcolor='#475569', zerolinecolor='#64748b', color='#f8fafc'),
                        title=dict(color='#f8fafc')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No recent activity data available")
            except Exception as e:
                st.error(f"Error loading activity data: {e}")
    
    with col2:
        st.markdown('<div class="section-header">🔍 Interaction Types</div>', unsafe_allow_html=True)
        if conn:
            try:
                query = """
                    SELECT interaction_type, COUNT(*) as count
                    FROM agent_interactions 
                    GROUP BY interaction_type
                """
                type_data = pd.read_sql(query, conn)
                
                if not type_data.empty:
                    fig = px.pie(type_data, values='count', names='interaction_type',
                               title="Interaction Type Distribution")
                    # Fix chart colors for dark theme visibility
                    fig.update_traces(marker_colors=['#60a5fa', '#a78bfa', '#34d399', '#f87171'])
                    fig.update_layout(
                        plot_bgcolor='#1e293b',
                        paper_bgcolor='#1e293b',
                        font=dict(color='#f8fafc', size=14),
                        title=dict(color='#f8fafc')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No interaction type data available")
            except Exception as e:
                st.error(f"Error loading type data: {e}")

def show_interactions(conn):
    """Show interactions management"""
    st.markdown('<div class="section-header">💬 Interactions</div>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        interaction_type = st.selectbox(
            "Interaction Type",
            ["All", "client_request", "agent_response", "conversation_turn", "error"]
        )
    
    with col2:
        status_filter = st.selectbox(
            "Status",
            ["All", "success", "error", "timeout"]
        )
    
    with col3:
        limit = st.slider("Show last N interactions", 10, 100, 20)
    
    # Get interactions
    interactions = get_recent_interactions(conn, limit)
    
    if interactions.empty:
        st.info("No interactions found")
        return
    
    # Apply filters
    if interaction_type != "All":
        interactions = interactions[interactions['interaction_type'] == interaction_type]
    
    if status_filter != "All":
        interactions = interactions[interactions['status'] == status_filter]
    
    # Display interactions
    st.subheader(f"📋 Recent Interactions ({len(interactions)} found)")
    
    # Format timestamp
    interactions['timestamp'] = pd.to_datetime(interactions['timestamp'])
    interactions['timestamp'] = interactions['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Display as table
    st.dataframe(
        interactions,
        use_container_width=True,
        hide_index=True
    )
    
    # Export option
    if st.button("📥 Export to CSV"):
        csv = interactions.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"interactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def show_sessions(conn):
    """Show sessions management"""
    st.header("🔄 Sessions")
    
    sessions = get_session_summary(conn)
    
    if sessions.empty:
        st.info("No sessions found")
        return
    
    # Format timestamps
    sessions['started_at'] = pd.to_datetime(sessions['started_at'])
    sessions['last_activity'] = pd.to_datetime(sessions['last_activity'])
    sessions['started_at'] = sessions['started_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    sessions['last_activity'] = sessions['last_activity'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Display sessions
    st.subheader(f"📋 Active Sessions ({len(sessions)} total)")
    
    st.dataframe(
        sessions,
        use_container_width=True,
        hide_index=True
    )
    
    # Session details
    if st.checkbox("Show session details"):
        selected_session = st.selectbox(
            "Select session to view details:",
            sessions['id'].tolist()
        )
        
        if selected_session and conn:
            try:
                # Get session interactions
                query = """
                    SELECT id, timestamp, interaction_type, status, prompt, response
                    FROM agent_interactions 
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 10
                """
                session_interactions = pd.read_sql(query, conn, params=(selected_session,))
                
                if not session_interactions.empty:
                    st.subheader(f"Session: {selected_session}")
                    st.dataframe(session_interactions, use_container_width=True)
                else:
                    st.info("No interactions found for this session")
            except Exception as e:
                st.error(f"Error loading session details: {e}")

def show_contexts(conn):
    """Show contexts management"""
    st.header("🧠 Contexts")
    
    contexts = get_context_summary(conn)
    
    if contexts.empty:
        st.info("No contexts found")
        return
    
    # Format timestamps
    contexts['created_at'] = pd.to_datetime(contexts['created_at'])
    contexts['last_used'] = pd.to_datetime(contexts['last_used'])
    contexts['created_at'] = contexts['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    contexts['last_used'] = contexts['last_used'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Display contexts
    st.subheader(f"📋 Context Objects ({len(contexts)} total)")
    
    st.dataframe(
        contexts,
        use_container_width=True,
        hide_index=True
    )
    
    # Context analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Context Usage")
        if not contexts.empty:
            fig = px.histogram(contexts, x='usage_count', 
                             title="Context Usage Distribution",
                             nbins=10)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Relevance Scores")
        if not contexts.empty:
            fig = px.box(contexts, y='relevance_score', 
                        title="Context Relevance Distribution")
            st.plotly_chart(fig, use_container_width=True)

def show_system_status(conn):
    """Show system status and health"""
    st.header("⚙️ System Status")
    
    # Context system status
    st.subheader("🧠 Context System")
    
    if CONTEXT_SYSTEM_AVAILABLE:
        st.success("✅ Context system is available")
        
        # Try to initialize context manager
        try:
            with st.spinner("Initializing context manager..."):
                context_manager = SeamlessContextManager(auto_start=False)
                st.success("✅ Context manager initialized successfully")
                
                # Show system capabilities
                st.subheader("🔧 Available Capabilities")
                for system_name, system_info in context_manager.context_systems.items():
                    status_color = "🟢" if system_info['status'] == 'available' else "🔴"
                    st.write(f"{status_color} **{system_name}**: {system_info['status']}")
                    
                    if system_info['capabilities']:
                        st.write(f"   Capabilities: {', '.join(system_info['capabilities'])}")
                
        except Exception as e:
            st.error(f"❌ Failed to initialize context manager: {e}")
    else:
        st.error("❌ Context system is not available")
    
    # Database status
    st.subheader("🗄️ Database Status")
    
    if conn:
        st.success("✅ Database connection successful")
        
        # Test queries
        try:
            # Test basic queries
            test_interactions = pd.read_sql("SELECT COUNT(*) as count FROM agent_interactions", conn)
            test_sessions = pd.read_sql("SELECT COUNT(*) as count FROM sessions", conn)
            test_contexts = pd.read_sql("SELECT COUNT(*) as count FROM conversation_contexts", conn)
            
            st.write(f"✅ Interactions table: {test_interactions.iloc[0]['count']} records")
            st.write(f"✅ Sessions table: {test_sessions.iloc[0]['count']} records")
            st.write(f"✅ Contexts table: {test_contexts.iloc[0]['count']} records")
            
        except Exception as e:
            st.error(f"❌ Database test failed: {e}")
    else:
        st.error("❌ Database connection failed")
    
    # System info
    st.subheader("ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Python Version**: {sys.version}")
        st.write(f"**Working Directory**: {os.getcwd()}")
        if MODELS_AVAILABLE:
            st.write(f"**Database Path**: {get_database_url()}")
        else:
            st.write("**Database Path**: N/A (models not available)")
    
    with col2:
        st.write(f"**Current Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Streamlit Version**: {st.__version__}")
        st.write(f"**Pandas Version**: {pd.__version__}")

if __name__ == "__main__":
    main()
