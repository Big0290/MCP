#!/usr/bin/env python3
"""
Test script to verify interaction filtering logic
"""

import sqlite3
import os

def test_filtering_logic():
    """Test the filtering logic used in the UI"""
    print("🔍 Testing Interaction Filtering Logic")
    print("=" * 60)
    
    db_path = "./data/agent_tracker.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test 1: Total count
        cursor.execute("SELECT COUNT(*) FROM agent_interactions")
        total_count = cursor.fetchone()[0]
        print(f"📊 Total interactions: {total_count}")
        
        # Test 2: Filter by conversation types
        conversation_types = ['conversation_turn', 'client_request', 'agent_response', 'user_prompt']
        placeholders = ','.join(['?'] * len(conversation_types))
        query = f"SELECT COUNT(*) FROM agent_interactions WHERE interaction_type IN ({placeholders})"
        cursor.execute(query, conversation_types)
        conversation_count = cursor.fetchone()[0]
        print(f"💬 Conversation types ({', '.join(conversation_types)}): {conversation_count}")
        
        # Test 3: Filter by system types
        system_types = ['health_check', 'monitoring_started', 'module_import', 'system_startup', 'system_shutdown']
        placeholders = ','.join(['?'] * len(system_types))
        query = f"SELECT COUNT(*) FROM agent_interactions WHERE interaction_type IN ({placeholders})"
        cursor.execute(query, system_types)
        system_count = cursor.fetchone()[0]
        print(f"⚙️ System types ({', '.join(system_types)}): {system_count}")
        
        # Test 4: Filter by tool types
        tool_types = ['tool_call', 'tool_response', 'tool_error']
        placeholders = ','.join(['?'] * len(tool_types))
        query = f"SELECT COUNT(*) FROM agent_interactions WHERE interaction_type IN ({placeholders})"
        cursor.execute(query, tool_types)
        tool_count = cursor.fetchone()[0]
        print(f"🔧 Tool types ({', '.join(tool_types)}): {tool_count}")
        
        # Test 5: Verify totals
        calculated_total = conversation_count + system_count + tool_count
        print(f"🧮 Calculated total: {calculated_total}")
        print(f"✅ Match: {'Yes' if calculated_total == total_count else 'No'}")
        
        # Test 6: Show all interaction types
        print(f"\n📋 All interaction types:")
        cursor.execute("SELECT interaction_type, COUNT(*) FROM agent_interactions GROUP BY interaction_type ORDER BY COUNT(*) DESC")
        for interaction_type, count in cursor.fetchall():
            print(f"  • {interaction_type}: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Interaction Filtering Test")
    print("=" * 60)
    test_filtering_logic()
    
    print(f"\n🎯 Expected Results:")
    print(f"• Total: 617 interactions")
    print(f"• Conversations: 107 interactions")
    print(f"• System: 501 interactions") 
    print(f"• Tools: 16 interactions")
    print(f"• Total: 107 + 501 + 16 = 624 (should match 617)")

if __name__ == "__main__":
    main()
