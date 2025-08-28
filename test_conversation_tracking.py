#!/usr/bin/env python3
"""
Test script for conversation tracking functionality
This tests the core tracking without requiring MCP packages
"""

import os
import sys
import time
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_conversation_tracking():
    """Test the conversation tracking functionality"""
    print("🧪 Testing Conversation Tracking System...")
    
    try:
        # Test 1: Import the logger
        print("📦 Testing imports...")
        from interaction_logger import logger
        print("✅ Interaction logger imported successfully")
        
        # Test 2: Test session creation
        print("🔑 Testing session creation...")
        session_id = logger.get_or_create_session()
        print(f"✅ Session created: {session_id}")
        
        # Test 3: Test client request logging
        print("📝 Testing client request logging...")
        logger.log_client_request("What's the weather like?")
        print("✅ Client request logged successfully")
        
        # Test 4: Test agent response logging
        print("🤖 Testing agent response logging...")
        logger.log_agent_response("The weather is sunny and warm.")
        print("✅ Agent response logged successfully")
        
        # Test 5: Test conversation turn logging
        print("🔄 Testing conversation turn logging...")
        logger.log_conversation_turn(
            client_request="What's the weather like?",
            agent_response="The weather is sunny and warm."
        )
        print("✅ Conversation turn logged successfully")
        
        # Test 6: Test custom interaction logging
        print("📊 Testing custom interaction logging...")
        logger.log_interaction(
            interaction_type='test_interaction',
            client_request="Test request",
            agent_response="Test response",
            metadata={'test': True, 'timestamp': datetime.utcnow().isoformat()}
        )
        print("✅ Custom interaction logged successfully")
        
        # Test 7: Test error logging
        print("❌ Testing error logging...")
        logger.log_interaction(
            interaction_type='test_error',
            error_message="This is a test error",
            status='error'
        )
        print("✅ Error logged successfully")
        
        print("\n🎉 All tests passed! Conversation tracking is working correctly.")
        print(f"📊 Session ID: {session_id}")
        print("💡 The system is now ready to track client-agent conversations automatically.")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        from config import Config
        print("✅ Configuration imported successfully")
        
        print(f"🌍 Environment: {Config.ENVIRONMENT}")
        print(f"📊 Background Monitoring: {Config.ENABLE_BACKGROUND_MONITORING}")
        print(f"⏱️ Monitoring Interval: {Config.MONITORING_INTERVAL_SECONDS} seconds")
        print(f"🔍 Automatic Metadata: {Config.ENABLE_AUTOMATIC_METADATA}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Conversation Tracking Tests...\n")
    
    config_ok = test_configuration()
    tracking_ok = test_conversation_tracking()
    
    print("\n" + "="*50)
    if config_ok and tracking_ok:
        print("🎯 ALL TESTS PASSED!")
        print("✅ Configuration: Working")
        print("✅ Conversation Tracking: Working")
        print("\n💡 Your MCP server is ready to track conversations automatically!")
    else:
        print("❌ SOME TESTS FAILED!")
        if not config_ok:
            print("❌ Configuration: Failed")
        if not tracking_ok:
            print("❌ Conversation Tracking: Failed")
        print("\n🔧 Please check the error messages above and fix any issues.")
    
    print("="*50)
