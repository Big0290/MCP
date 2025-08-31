#!/usr/bin/env python3
"""
🚀 Preference Migration Script

This script migrates existing JSON-based user preferences to the new
unified database system, creating a single source of truth.
"""

import json
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def migrate_preferences():
    """Migrate preferences from JSON to database"""
    
    logger.info("🚀 Starting preference migration...")
    
    try:
        # Import the unified preference manager
        from unified_preference_manager import migrate_preferences_to_database
        
        # Perform migration
        success = migrate_preferences_to_database()
        
        if success:
            logger.info("✅ Preferences successfully migrated to database!")
            logger.info("🎯 Now using single source of truth for all systems")
        else:
            logger.warning("⚠️ Migration completed with warnings - check logs")
            
        return success
        
    except ImportError as e:
        logger.error(f"❌ Cannot import unified preference manager: {e}")
        logger.error("Make sure unified_preference_manager.py is available")
        return False
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return False

def verify_migration():
    """Verify that migration was successful"""
    
    logger.info("🔍 Verifying migration...")
    
    try:
        from unified_preference_manager import get_user_preferences_unified
        
        # Get preferences from unified system
        preferences = get_user_preferences_unified()
        
        if preferences and "User Preferences:" in preferences:
            logger.info("✅ Migration verification successful!")
            logger.info("📋 Unified preferences loaded:")
            
            # Show first few lines
            lines = preferences.split('\n')[:10]
            for line in lines:
                if line.strip():
                    logger.info(f"   {line}")
            
            return True
        else:
            logger.error("❌ Migration verification failed - no preferences loaded")
            return False
            
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        return False

def cleanup_old_files():
    """Clean up old JSON preference files after successful migration"""
    
    logger.info("🧹 Cleaning up old preference files...")
    
    try:
        # List of old preference files to remove
        old_files = [
            "./data/dynamic_config/user_preferences.json",
            "./data/dynamic_config/agent_metadata.json"
        ]
        
        for file_path in old_files:
            path = Path(file_path)
            if path.exists():
                # Create backup first
                backup_path = path.with_suffix(f'.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
                path.rename(backup_path)
                logger.info(f"✅ Backed up {file_path} to {backup_path}")
            else:
                logger.info(f"ℹ️ {file_path} not found, skipping")
        
        logger.info("✅ Cleanup completed - old files backed up")
        return True
        
    except Exception as e:
        logger.error(f"❌ Cleanup failed: {e}")
        return False

def main():
    """Main migration function"""
    
    logger.info("=" * 60)
    logger.info("🚀 USER PREFERENCES MIGRATION TO UNIFIED DATABASE")
    logger.info("=" * 60)
    
    # Step 1: Migrate preferences
    logger.info("\n📋 Step 1: Migrating preferences to database...")
    migration_success = migrate_preferences()
    
    if not migration_success:
        logger.error("❌ Migration failed, stopping process")
        return False
    
    # Step 2: Verify migration
    logger.info("\n🔍 Step 2: Verifying migration...")
    verification_success = verify_migration()
    
    if not verification_success:
        logger.error("❌ Verification failed, migration may be incomplete")
        return False
    
    # Step 3: Cleanup old files (optional)
    logger.info("\n🧹 Step 3: Cleaning up old files...")
    cleanup_success = cleanup_old_files()
    
    if cleanup_success:
        logger.info("✅ Migration process completed successfully!")
        logger.info("\n🎯 BENEFITS OF UNIFIED SYSTEM:")
        logger.info("   • Single source of truth for all preferences")
        logger.info("   • Real-time updates across all systems")
        logger.info("   • Database persistence and reliability")
        logger.info("   • Consistent preference loading everywhere")
        logger.info("   • No more duplicate preference functions")
    else:
        logger.warning("⚠️ Migration completed but cleanup failed")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        logger.info("\n🎉 MIGRATION COMPLETED SUCCESSFULLY!")
        logger.info("Your system now uses a unified preference database!")
    else:
        logger.error("\n❌ MIGRATION FAILED!")
        logger.error("Check the logs above for details")
