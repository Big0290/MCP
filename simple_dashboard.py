#!/usr/bin/env python3
"""
Simple Personal Monitoring Dashboard
Reliable text-based monitoring for your context enhancement system
"""

import sys
import os
import time
import json
from datetime import datetime, timedelta
import threading
from typing import Dict, Any, List

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class SimpleDashboard:
    """
    Simple, reliable text-based monitoring dashboard
    
    Features:
    1. Real-time system metrics
    2. Cache performance monitoring
    3. Learning system insights
    4. Performance analytics
    5. System health indicators
    """
    
    def __init__(self, refresh_rate: float = 2.0):
        self.refresh_rate = refresh_rate
        self.is_running = False
        self.dashboard_data = {}
        self.update_thread = None
        self.last_update = datetime.now()
        self.start_time = datetime.now()
        
        # Initialize system connections
        self._initialize_system_connections()
        
        # Performance tracking
        self.performance_history = []
        self.alert_history = []
        
        print("🚀 Simple Monitoring Dashboard Initialized")
    
    def _initialize_system_connections(self):
        """Initialize connections to all monitoring systems"""
        try:
            # Import monitoring functions
            from context_manager import get_performance_summary, get_context_system_status
            from smart_caching_system import get_cache_stats
            from context_learning_system import get_learning_insights
            
            self.monitoring_functions = {
                'context_manager': get_performance_summary,
                'cache_system': get_cache_stats,
                'learning_system': get_learning_insights
            }
            
            print("✅ All monitoring systems connected successfully")
            
        except ImportError as e:
            print(f"⚠️ Some monitoring systems not available: {e}")
            self.monitoring_functions = {}
    
    def start_monitoring(self):
        """Start the monitoring dashboard"""
        self.is_running = True
        print("🔄 Starting monitoring...")
        
        # Start data update thread
        self.update_thread = threading.Thread(target=self._update_data_loop, daemon=True)
        self.update_thread.start()
        
        # Main display loop
        try:
            while self.is_running:
                self._display_dashboard()
                time.sleep(self.refresh_rate)
        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped by user")
        except Exception as e:
            print(f"❌ Dashboard error: {e}")
        finally:
            self.stop_monitoring()
    
    def _update_data_loop(self):
        """Background loop to update monitoring data"""
        while self.is_running:
            try:
                self._collect_monitoring_data()
                time.sleep(self.refresh_rate)
            except Exception as e:
                print(f"⚠️ Data update failed: {e}")
                time.sleep(5)  # Longer delay on error
    
    def _collect_monitoring_data(self):
        """Collect data from all monitoring systems"""
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'systems': {},
                'performance': {},
                'cache': {},
                'learning': {},
                'alerts': []
            }
            
            # Collect context manager data
            if 'context_manager' in self.monitoring_functions:
                try:
                    data['systems']['context_manager'] = self.monitoring_functions['context_manager']()
                except Exception as e:
                    data['alerts'].append(f"Context manager error: {str(e)}")
            
            # Collect cache system data
            if 'cache_system' in self.monitoring_functions:
                try:
                    data['cache'] = self.monitoring_functions['cache_system']()
                except Exception as e:
                    data['alerts'].append(f"Cache system error: {str(e)}")
            
            # Collect learning system data
            if 'learning_system' in self.monitoring_functions:
                try:
                    data['learning'] = self.monitoring_functions['learning_system']()
                except Exception as e:
                    data['alerts'].append(f"Learning system error: {str(e)}")
            
            # Calculate performance metrics
            data['performance'] = self._calculate_performance_metrics(data)
            
            # Update dashboard data
            self.dashboard_data = data
            self.last_update = datetime.now()
            
            # Track performance history
            self._track_performance_history(data)
            
        except Exception as e:
            print(f"❌ Data collection failed: {e}")
    
    def _calculate_performance_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance metrics from collected data"""
        metrics = {
            'overall_health': 'unknown',
            'health_score': 0,
            'response_time_avg': 0.0,
            'cache_efficiency': 0.0,
            'learning_effectiveness': 0.0,
            'system_utilization': 0.0
        }
        
        try:
            # Calculate cache efficiency
            if 'cache' in data and 'total_hits' in data['cache']:
                total_requests = data['cache']['total_hits'] + data['cache']['total_misses']
                if total_requests > 0:
                    metrics['cache_efficiency'] = data['cache']['total_hits'] / total_requests
            
            # Calculate response time
            if 'cache' in data and 'average_response_time' in data['cache']:
                metrics['response_time_avg'] = data['cache']['average_response_time']
            
            # Calculate learning effectiveness
            if 'learning' in data and 'learning_stats' in data['learning']:
                learning_stats = data['learning']['learning_stats']
                total_learned = learning_stats.get('total_learned', 0)
                if total_learned > 0:
                    metrics['learning_effectiveness'] = min(total_learned / 100, 1.0)  # Normalize to 0-1
            
            # Calculate health score
            health_score = 0
            if metrics['cache_efficiency'] > 0.7:
                health_score += 1
            if metrics['response_time_avg'] < 0.001:
                health_score += 1
            if metrics['learning_effectiveness'] > 0.5:
                health_score += 1
            
            metrics['health_score'] = health_score
            
            # Determine overall health
            if health_score >= 2:
                metrics['overall_health'] = 'excellent'
            elif health_score >= 1:
                metrics['overall_health'] = 'good'
            else:
                metrics['overall_health'] = 'needs_attention'
            
        except Exception as e:
            print(f"⚠️ Performance calculation failed: {e}")
        
        return metrics
    
    def _track_performance_history(self, data: Dict[str, Any]):
        """Track performance history for trends"""
        if 'performance' in data:
            perf = data['performance']
            history_entry = {
                'timestamp': datetime.now(),
                'health_score': perf.get('health_score', 0),
                'cache_efficiency': perf.get('cache_efficiency', 0),
                'response_time': perf.get('response_time_avg', 0)
            }
            
            self.performance_history.append(history_entry)
            
            # Keep only recent history (last 50 entries)
            if len(self.performance_history) > 50:
                self.performance_history = self.performance_history[-50:]
    
    def _display_dashboard(self):
        """Display the monitoring dashboard"""
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Display header
        self._display_header()
        
        # Display system metrics
        self._display_system_metrics()
        
        # Display cache system
        self._display_cache_system()
        
        # Display learning system
        self._display_learning_system()
        
        # Display performance analytics
        self._display_performance_analytics()
        
        # Display alerts
        self._display_alerts()
        
        # Display footer
        self._display_footer()
    
    def _display_header(self):
        """Display dashboard header"""
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]  # Remove microseconds
        
        print("🧠 INTELLIGENT CONTEXT ENHANCEMENT SYSTEM - LIVE MONITOR")
        print("=" * 70)
        print(f"🕐 Started: {self.start_time.strftime('%H:%M:%S')} | ⏱️ Uptime: {uptime_str}")
        print(f"🔄 Last Update: {self.last_update.strftime('%H:%M:%S')}")
        print("=" * 70)
        print()
    
    def _display_system_metrics(self):
        """Display system metrics section"""
        print("📊 SYSTEM METRICS")
        print("-" * 50)
        
        if self.dashboard_data and 'performance' in self.dashboard_data:
            perf = self.dashboard_data['performance']
            health = perf.get('overall_health', 'unknown')
            health_score = perf.get('health_score', 0)
            
            # Health indicator
            if health == 'excellent':
                health_icon = "🟢"
                health_color = "EXCELLENT"
            elif health == 'good':
                health_icon = "🟡"
                health_color = "GOOD"
            else:
                health_icon = "🔴"
                health_color = "NEEDS ATTENTION"
            
            print(f"{health_icon} Overall Health: {health_color} (Score: {health_score}/3)")
            print(f"⚡ Avg Response Time: {perf.get('response_time_avg', 0):.6f}s")
            print(f"💾 Cache Efficiency: {perf.get('cache_efficiency', 0):.1%}")
            print(f"🧠 Learning Effectiveness: {perf.get('learning_effectiveness', 0):.1%}")
            
            # System status
            if 'systems' in self.dashboard_data and 'context_manager' in self.dashboard_data['systems']:
                systems = self.dashboard_data['systems']['context_manager']
                print(f"🔧 Active Systems: {systems.get('active_systems', 0)}")
                print(f"📈 Total Prompts Processed: {systems.get('total_prompts_processed', 0)}")
        else:
            print("⏳ Collecting system data...")
        
        print()
    
    def _display_cache_system(self):
        """Display cache system section"""
        print("💾 CACHE SYSTEM")
        print("-" * 50)
        
        if self.dashboard_data and 'cache' in self.dashboard_data:
            cache = self.dashboard_data['cache']
            
            print(f"📥 Cache Hits: {cache.get('total_hits', 0)}")
            print(f"❌ Cache Misses: {cache.get('total_misses', 0)}")
            print(f"🎯 Hit Rate: {cache.get('cache_hit_rate', 0):.1%}")
            print(f"💾 Memory Usage: {cache.get('memory_usage_mb', 0):.2f}MB")
            print(f"🔄 Optimizations: {cache.get('optimization_count', 0)}")
            print(f"🧹 Total Evictions: {cache.get('total_evictions', 0)}")
            
            # Context cache breakdown
            context_caches = cache.get('context_cache_entries', {})
            if context_caches:
                print(f"📁 Context Caches: {', '.join([f'{ctx}({count})' for ctx, count in context_caches.items()])}")
        else:
            print("⏳ Collecting cache data...")
        
        print()
    
    def _display_learning_system(self):
        """Display learning system section"""
        print("🧠 LEARNING SYSTEM")
        print("-" * 50)
        
        if self.dashboard_data and 'learning' in self.dashboard_data:
            learning = self.dashboard_data['learning']
            stats = learning.get('learning_stats', {})
            
            print(f"📚 Total Learned: {stats.get('total_learned', 0)}")
            print(f"🔍 Patterns Recognized: {stats.get('patterns_recognized', 0)}")
            print(f"⚙️ Strategies Optimized: {stats.get('strategies_optimized', 0)}")
            
            # Context effectiveness
            context_summary = learning.get('context_effectiveness_summary', {})
            if context_summary:
                print(f"🎯 Context Types Analyzed: {len(context_summary)}")
                for ctx_type, data in context_summary.items():
                    avg_ratio = data.get('average_enhancement_ratio', 0)
                    total_interactions = data.get('total_interactions', 0)
                    print(f"   • {ctx_type.title()}: {avg_ratio:.2f}x enhancement ({total_interactions} interactions)")
            
            # Pattern insights
            pattern_insights = learning.get('pattern_insights', {})
            if pattern_insights:
                print(f"🔍 Pattern Insights: {len(pattern_insights)} terms analyzed")
        else:
            print("⏳ Collecting learning data...")
        
        print()
    
    def _display_performance_analytics(self):
        """Display performance analytics section"""
        print("📈 PERFORMANCE ANALYTICS")
        print("-" * 50)
        
        if self.performance_history:
            # Calculate trends
            recent_scores = [entry['health_score'] for entry in self.performance_history[-10:]]
            avg_recent_score = sum(recent_scores) / len(recent_scores) if recent_scores else 0
            
            print(f"📊 Recent Health Trend: {avg_recent_score:.1f}/3 average")
            
            # Performance history summary
            total_entries = len(self.performance_history)
            excellent_count = sum(1 for entry in self.performance_history if entry['health_score'] >= 2)
            excellent_percentage = (excellent_count / total_entries) * 100 if total_entries > 0 else 0
            
            print(f"🏆 Excellent Performance: {excellent_percentage:.1f}% of time")
            
            # Cache performance trend
            if len(self.performance_history) >= 2:
                recent_cache = [entry['cache_efficiency'] for entry in self.performance_history[-5:]]
                avg_cache = sum(recent_cache) / len(recent_cache) if recent_cache else 0
                print(f"💾 Recent Cache Performance: {avg_cache:.1%} average")
        else:
            print("⏳ Building performance history...")
        
        print()
    
    def _display_alerts(self):
        """Display system alerts"""
        if self.dashboard_data and 'alerts' in self.dashboard_data:
            alerts = self.dashboard_data['alerts']
            if alerts:
                print("⚠️ SYSTEM ALERTS")
                print("-" * 50)
                for i, alert in enumerate(alerts[:5], 1):  # Show first 5 alerts
                    print(f"{i}. {alert}")
                if len(alerts) > 5:
                    print(f"... and {len(alerts) - 5} more alerts")
                print()
        
        # Display recommendations if available
        try:
            from context_learning_system import get_learning_recommendations
            recommendations = get_learning_recommendations()
            if recommendations:
                print("💡 LEARNING RECOMMENDATIONS")
                print("-" * 50)
                for i, rec in enumerate(recommendations[:3], 1):  # Show first 3 recommendations
                    print(f"{i}. {rec}")
                print()
        except ImportError:
            pass
    
    def _display_footer(self):
        """Display dashboard footer"""
        print("=" * 70)
        print("🔄 Real-time monitoring active | Press Ctrl+C to exit")
        print("💡 Dashboard refreshes every {:.1f} seconds".format(self.refresh_rate))
    
    def stop_monitoring(self):
        """Stop the monitoring dashboard"""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=2)
        print("🛑 Monitoring dashboard stopped")
    
    def export_dashboard_data(self) -> Dict[str, Any]:
        """Export current dashboard data for analysis"""
        return {
            'dashboard_data': self.dashboard_data,
            'performance_history': [
                {
                    'timestamp': entry['timestamp'].isoformat(),
                    'health_score': entry['health_score'],
                    'cache_efficiency': entry['cache_efficiency'],
                    'response_time': entry['response_time']
                }
                for entry in self.performance_history
            ],
            'export_timestamp': datetime.now().isoformat(),
            'uptime_seconds': (datetime.now() - self.start_time).total_seconds()
        }

# Global instance for easy access
simple_dashboard = SimpleDashboard()

def start_simple_dashboard(refresh_rate: float = 2.0):
    """Start the simple monitoring dashboard"""
    dashboard = SimpleDashboard(refresh_rate)
    dashboard.start_monitoring()

def get_dashboard_data() -> Dict[str, Any]:
    """Get current dashboard data"""
    return simple_dashboard.dashboard_data if simple_dashboard.is_running else {}

def export_dashboard_data() -> Dict[str, Any]:
    """Export dashboard data for analysis"""
    return simple_dashboard.export_dashboard_data()

if __name__ == "__main__":
    print("🚀 Starting Simple Personal Monitoring Dashboard...")
    print("=" * 60)
    
    try:
        # Start the dashboard
        start_simple_dashboard(refresh_rate=2.0)
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Dashboard failed: {e}")
        print("💡 Try running with: python3 simple_dashboard.py")
