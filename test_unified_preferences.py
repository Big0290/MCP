#!/usr/bin/env python3
"""
🧪 Test Unified Preference System

This script tests the unified preference system to ensure it provides
consistent data across all systems and eliminates the duplication issue.
"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_unified_preference_manager():
    """Test the unified preference manager directly"""
    
    logger.info("🧪 Testing Unified Preference Manager...")
    
    try:
        from unified_preference_manager import (
            get_unified_preference_manager,
            get_user_preferences_unified,
            update_user_preferences_unified
        )
        
        # Test 1: Get preferences
        logger.info("📋 Test 1: Getting preferences...")
        preferences = get_user_preferences_unified()
        
        if not preferences or "User Preferences:" not in preferences:
            logger.error("❌ Failed to get preferences")
            return False
        
        logger.info("✅ Preferences retrieved successfully")
        
        # Test 2: Update preferences
        logger.info("📝 Test 2: Updating preferences...")
        test_update = {
            "custom_preferences": {
                "test_preference": "test_value",
                "unified_system": "working"
            }
        }
        
        success = update_user_preferences_unified(test_update)
        if not success:
            logger.error("❌ Failed to update preferences")
            return False
        
        logger.info("✅ Preferences updated successfully")
        
        # Test 3: Verify update
        logger.info("🔍 Test 3: Verifying update...")
        updated_preferences = get_user_preferences_unified()
        
        if "test_preference: test_value" not in updated_preferences:
            logger.error("❌ Update not reflected in preferences")
            return False
        
        logger.info("✅ Update verification successful")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Cannot import unified preference manager: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

def test_consistency_across_systems():
    """Test that all systems now return the same preferences"""
    
    logger.info("🔄 Testing Consistency Across Systems...")
    
    try:
        # Test 1: Unified preference manager
        from unified_preference_manager import get_user_preferences_unified
        unified_prefs = get_user_preferences_unified()
        
        # Test 2: Local MCP server (should now use unified system)
        from local_mcp_server_simple import _get_user_preferences
        mcp_prefs = _get_user_preferences()
        
        # Test 3: Prompt generator (should now use unified system)
        from prompt_generator import PromptGenerator
        gen = PromptGenerator()
        # We need to create a mock context to test this
        # For now, just check if the import works
        
        logger.info("✅ All systems imported successfully")
        
        # Compare preferences
        if unified_prefs == mcp_prefs:
            logger.info("✅ Preferences are consistent across systems!")
            logger.info("🎯 Single source of truth working correctly")
            return True
        else:
            logger.error("❌ Preferences are still inconsistent!")
            logger.error("This means the unified system is not fully integrated")
            return False
            
    except Exception as e:
        logger.error(f"❌ Consistency test failed: {e}")
        return False

def test_database_persistence():
    """Test that preferences are properly persisted in database"""
    
    logger.info("💾 Testing Database Persistence...")
    
    try:
        from unified_preference_manager import get_unified_preference_manager
        
        manager = get_unified_preference_manager()
        
        # Test database operations
        test_data = {
            "custom_preferences": {
                "database_test": "persistent_value",
                "timestamp": "2025-08-31"
            }
        }
        
        # Update preferences
        success = manager.update_preferences(test_data)
        if not success:
            logger.error("❌ Failed to update preferences in database")
            return False
        
        # Force refresh to test database loading
        refreshed_prefs = manager.get_preferences(force_refresh=True)
        
        if not refreshed_prefs:
            logger.error("❌ Failed to load preferences from database")
            return False
        
        # Check if our test data is there
        custom_prefs = refreshed_prefs.custom_preferences
        if not custom_prefs or "database_test" not in custom_prefs:
            logger.error("❌ Test data not found in database")
            return False
        
        logger.info("✅ Database persistence working correctly")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database persistence test failed: {e}")
        return False

def show_preference_comparison():
    """Show a comparison of preferences from different systems"""
    
    logger.info("📊 Showing Preference Comparison...")
    
    try:
        # Get preferences from unified system
        from unified_preference_manager import get_user_preferences_unified
        unified_prefs = get_user_preferences_unified()
        
        # Get preferences from MCP server
        from local_mcp_server_simple import _get_user_preferences
        mcp_prefs = _get_user_preferences()
        
        logger.info("=" * 60)
        logger.info("🔍 PREFERENCE COMPARISON")
        logger.info("=" * 60)
        
        logger.info("📋 Unified System Preferences:")
        logger.info(unified_prefs)
        
        logger.info("\n📋 MCP Server Preferences:")
        logger.info(mcp_prefs)
        
        logger.info("\n" + "=" * 60)
        
        if unified_prefs == mcp_prefs:
            logger.info("✅ PREFERENCES ARE IDENTICAL!")
            logger.info("🎯 Single source of truth achieved!")
        else:
            logger.warning("⚠️ PREFERENCES ARE STILL DIFFERENT!")
            logger.warning("The unified system needs further integration")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Comparison failed: {e}")
        return False

def main():
    """Main test function"""
    
    logger.info("=" * 60)
    logger.info("🧪 UNIFIED PREFERENCE SYSTEM TEST SUITE")
    logger.info("=" * 60)
    
    tests = [
        ("Unified Preference Manager", test_unified_preference_manager),
        ("Consistency Across Systems", test_consistency_across_systems),
        ("Database Persistence", test_database_persistence),
        ("Preference Comparison", show_preference_comparison)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                logger.info(f"✅ {test_name}: PASSED")
            else:
                logger.error(f"❌ {test_name}: FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"   {test_name}: {status}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED!")
        logger.info("🚀 Your unified preference system is working perfectly!")
        logger.info("🎯 You now have a single source of truth for preferences!")
    else:
        logger.warning("⚠️ Some tests failed - check the logs above")
        logger.warning("The unified system may need further configuration")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
