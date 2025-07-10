"""
Simple test script for Project Finder
Run this to test your API key and basic functionality
"""

import os
import sys
import time

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Google GenerativeAI imported successfully")
    except ImportError as e:
        print(f"❌ Google GenerativeAI import failed: {e}")
        return False
    
    return True

def test_api_key():
    """Test API key configuration"""
    print("\nTesting API key...")
    
    # Check environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("✅ API key found in environment variables")
        return api_key
    
    # Check secrets file
    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if api_key:
            print("✅ API key found in Streamlit secrets")
            return api_key
    except:
        pass
    
    print("⚠️  No API key found in environment or secrets")
    print("   You'll need to enter it manually in the app")
    return None

def test_gemini_connection(api_key):
    """Test connection to Gemini API"""
    if not api_key:
        print("⏭️  Skipping Gemini API test (no API key)")
        return
    
    print("\nTesting Gemini API connection...")
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Simple test query
        response = model.generate_content("Say 'Hello, Project Finder!' in exactly those words.")
        if response and response.text:
            print("✅ Gemini API connection successful")
            print(f"   Response: {response.text.strip()}")
        else:
            print("❌ Gemini API returned empty response")
    except Exception as e:
        print(f"❌ Gemini API connection failed: {e}")

def test_streamlit_run():
    """Test that Streamlit can find and parse the main app"""
    print("\nTesting Streamlit app...")
    try:
        # Import the main app
        import app
        print("✅ Main app.py imported successfully")
        
        # Check if main function exists
        if hasattr(app, 'main'):
            print("✅ Main function found")
        else:
            print("❌ Main function not found")
        
        # Check if GeminiService class exists
        if hasattr(app, 'GeminiService'):
            print("✅ GeminiService class found")
        else:
            print("❌ GeminiService class not found")
            
    except Exception as e:
        print(f"❌ App import failed: {e}")

def main():
    print("🚀 Project Finder - System Test")
    print("=" * 40)
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ Import test failed. Please install requirements:")
        print("   pip install -r requirements.txt")
        return
    
    # Test 2: API Key
    api_key = test_api_key()
    
    # Test 3: Gemini API
    test_gemini_connection(api_key)
    
    # Test 4: Streamlit app
    test_streamlit_run()
    
    print("\n" + "=" * 40)
    print("🎯 Test Summary:")
    print("   If all tests passed, you can run: streamlit run app.py")
    print("   If API key test failed, configure it before running the app")
    print("   If any imports failed, install missing packages")

if __name__ == "__main__":
    main()
