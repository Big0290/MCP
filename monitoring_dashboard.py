#!/usr/bin/env python3
"""
Personal Monitoring Dashboard
Real-time insights into your intelligent context enhancement system
"""

import sys
import os
import time
import json
from datetime import datetime, timedelta
import threading
from typing import Dict, Any, List
import curses
import locale

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class MonitoringDashboard:
    """
    Real-time monitoring dashboard for your context enhancement system
    
    Features:
    1. Live system performance metrics
    2. Real-time cache statistics
    3. Learning system insights
    4. Context enhancement analytics
    5. Interactive system controls
    """
    
    def __init__(self, refresh_rate: float = 1.0):
        self.refresh_rate = refresh_rate
        self.is_running = False
        self.dashboard_data = {}
        self.update_thread = None
        self.last_update = datetime.now()
        
        # Initialize system connections
        self._initialize_system_connections()
        
        # Dashboard layout
        self.layout = {
            'header_height': 3,
            'metrics_height': 8,
            'cache_height': 6,
            'learning_height': 6,
            'performance_height': 6,
            'footer_height': 2
        }
    
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
            
            print("✅ Monitoring systems connected successfully")
            
        except ImportError as e:
            print(f"⚠️ Some monitoring systems not available: {e}")
            self.monitoring_functions = {}
    
    def start_monitoring(self):
        """Start the monitoring dashboard"""
        self.is_running = True
        
        # Start data update thread
        self.update_thread = threading.Thread(target=self._update_data_loop, daemon=True)
        self.update_thread.start()
        
        # Start curses-based dashboard
        try:
            curses.wrapper(self._run_dashboard)
        except Exception as e:
            print(f"❌ Dashboard failed: {e}")
            self._run_fallback_dashboard()
    
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
            
        except Exception as e:
            print(f"❌ Data collection failed: {e}")
    
    def _calculate_performance_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance metrics from collected data"""
        metrics = {
            'overall_health': 'unknown',
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
            
            # Calculate overall health
            health_score = 0
            if metrics['cache_efficiency'] > 0.7:
                health_score += 1
            if metrics['response_time_avg'] < 0.001:
                health_score += 1
            if metrics['learning_effectiveness'] > 0.5:
                health_score += 1
            
            if health_score >= 2:
                metrics['overall_health'] = 'excellent'
            elif health_score >= 1:
                metrics['overall_health'] = 'good'
            else:
                metrics['overall_health'] = 'needs_attention'
            
        except Exception as e:
            print(f"⚠️ Performance calculation failed: {e}")
        
        return metrics
    
    def _run_dashboard(self, stdscr):
        """Run the curses-based dashboard"""
        # Setup curses
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        
        # Define colors
        curses.init_pair(1, curses.COLOR_GREEN, -1)    # Success
        curses.init_pair(2, curses.COLOR_YELLOW, -1)   # Warning
        curses.init_pair(3, curses.COLOR_RED, -1)      # Error
        curses.init_pair(4, curses.COLOR_BLUE, -1)     # Info
        curses.init_pair(5, curses.COLOR_CYAN, -1)     # Highlight
        
        # Main dashboard loop
        while self.is_running:
            try:
                self._draw_dashboard(stdscr)
                time.sleep(0.1)
            except KeyboardInterrupt:
                break
            except Exception as e:
                stdscr.addstr(0, 0, f"Dashboard Error: {str(e)}")
                stdscr.refresh()
                time.sleep(1)
    
    def _draw_dashboard(self, stdscr):
        """Draw the dashboard on screen"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Draw header
        self._draw_header(stdscr, width)
        
        # Draw metrics section
        self._draw_metrics_section(stdscr, width)
        
        # Draw cache section
        self._draw_cache_section(stdscr, width)
        
        # Draw learning section
        self._draw_learning_section(stdscr, width)
        
        # Draw performance section
        self._draw_performance_section(stdscr, width)
        
        # Draw footer
        self._draw_footer(stdscr, width)
        
        stdscr.refresh()
    
    def _draw_header(self, stdscr, width):
        """Draw dashboard header"""
        title = "🧠 Intelligent Context Enhancement System - Live Monitor"
        timestamp = f"Last Update: {self.last_update.strftime('%H:%M:%S')}"
        
        stdscr.addstr(0, (width - len(title)) // 2, title, curses.color_pair(5))
        stdscr.addstr(1, (width - len(timestamp)) // 2, timestamp, curses.color_pair(4))
        stdscr.addstr(2, 0, "=" * width, curses.color_pair(4))
    
    def _draw_metrics_section(self, stdscr, width):
        """Draw system metrics section"""
        y_offset = self.layout['header_height']
        
        stdscr.addstr(y_offset, 0, "📊 SYSTEM METRICS", curses.color_pair(5))
        stdscr.addstr(y_offset + 1, 0, "-" * 50)
        
        if self.dashboard_data:
            data = self.dashboard_data
            performance = data.get('performance', {})
            
            # Overall health
            health = performance.get('overall_health', 'unknown')
            health_color = curses.color_pair(1) if health == 'excellent' else \
                          curses.color_pair(2) if health == 'good' else curses.color_pair(3)
            
            stdscr.addstr(y_offset + 2, 0, f"🏥 Overall Health: {health.upper()}", health_color)
            
            # Performance metrics
            stdscr.addstr(y_offset + 3, 0, f"⚡ Avg Response Time: {performance.get('response_time_avg', 0):.6f}s")
            stdscr.addstr(y_offset + 4, 0, f"💾 Cache Efficiency: {performance.get('cache_efficiency', 0):.1%}")
            stdscr.addstr(y_offset + 5, 0, f"🧠 Learning Effectiveness: {performance.get('learning_effectiveness', 0):.1%}")
            
            # System status
            if 'systems' in data and 'context_manager' in data['systems']:
                systems = data['systems']['context_manager']
                stdscr.addstr(y_offset + 6, 0, f"🔧 Active Systems: {systems.get('active_systems', 0)}")
                stdscr.addstr(y_offset + 7, 0, f"📈 Total Processed: {systems.get('total_prompts_processed', 0)}")
    
    def _draw_cache_section(self, stdscr, width):
        """Draw cache system section"""
        y_offset = self.layout['header_height'] + self.layout['metrics_height']
        
        stdscr.addstr(y_offset, 0, "💾 CACHE SYSTEM", curses.color_pair(5))
        stdscr.addstr(y_offset + 1, 0, "-" * 50)
        
        if self.dashboard_data and 'cache' in self.dashboard_data:
            cache = self.dashboard_data['cache']
            
            stdscr.addstr(y_offset + 2, 0, f"📥 Cache Hits: {cache.get('total_hits', 0)}")
            stdscr.addstr(y_offset + 3, 0, f"❌ Cache Misses: {cache.get('total_misses', 0)}")
            stdscr.addstr(y_offset + 4, 0, f"🎯 Hit Rate: {cache.get('cache_hit_rate', 0):.1%}")
            stdscr.addstr(y_offset + 5, 0, f"💾 Memory Usage: {cache.get('memory_usage_mb', 0):.2f}MB")
    
    def _draw_learning_section(self, stdscr, width):
        """Draw learning system section"""
        y_offset = self.layout['header_height'] + self.layout['metrics_height'] + self.layout['cache_height']
        
        stdscr.addstr(y_offset, 0, "🧠 LEARNING SYSTEM", curses.color_pair(5))
        stdscr.addstr(y_offset + 1, 0, "-" * 50)
        
        if self.dashboard_data and 'learning' in self.dashboard_data:
            learning = self.dashboard_data['learning']
            stats = learning.get('learning_stats', {})
            
            stdscr.addstr(y_offset + 2, 0, f"📚 Total Learned: {stats.get('total_learned', 0)}")
            stdscr.addstr(y_offset + 3, 0, f"🔍 Patterns Recognized: {stats.get('patterns_recognized', 0)}")
            stdscr.addstr(y_offset + 4, 0, f"⚙️ Strategies Optimized: {stats.get('strategies_optimized', 0)}")
            
            # Context effectiveness
            context_summary = learning.get('context_effectiveness_summary', {})
            if context_summary:
                stdscr.addstr(y_offset + 5, 0, f"🎯 Context Types: {len(context_summary)}")
    
    def _draw_performance_section(self, stdscr, width):
        """Draw performance analytics section"""
        y_offset = self.layout['header_height'] + self.layout['metrics_height'] + self.layout['cache_height'] + self.layout['learning_height']
        
        stdscr.addstr(y_offset, 0, "📈 PERFORMANCE ANALYTICS", curses.color_pair(5))
        stdscr.addstr(y_offset + 1, 0, "-" * 50)
        
        if self.dashboard_data:
            # Alerts
            alerts = self.dashboard_data.get('alerts', [])
            if alerts:
                stdscr.addstr(y_offset + 2, 0, f"⚠️ Alerts: {len(alerts)}", curses.color_pair(2))
                for i, alert in enumerate(alerts[:3]):  # Show first 3 alerts
                    stdscr.addstr(y_offset + 3 + i, 0, f"   {alert[:47]}...")
            else:
                stdscr.addstr(y_offset + 2, 0, "✅ No alerts - System running smoothly", curses.color_pair(1))
            
            # Performance trends
            if 'cache' in self.dashboard_data:
                cache = self.dashboard_data['cache']
                stdscr.addstr(y_offset + 4, 0, f"🔄 Optimizations: {cache.get('optimization_count', 0)}")
                stdscr.addstr(y_offset + 5, 0, f"🧹 Total Evictions: {cache.get('total_evictions', 0)}")
    
    def _draw_footer(self, stdscr, width):
        """Draw dashboard footer"""
        y_offset = height - self.layout['footer_height']
        
        footer_text = "Press Ctrl+C to exit | Real-time monitoring active"
        stdscr.addstr(y_offset, (width - len(footer_text)) // 2, footer_text, curses.color_pair(4))
        stdscr.addstr(y_offset + 1, 0, "=" * width, curses.color_pair(4))
    
    def _run_fallback_dashboard(self):
        """Run a fallback text-based dashboard if curses fails"""
        print("🔄 Starting fallback monitoring dashboard...")
        
        while self.is_running:
            try:
                self._display_fallback_dashboard()
                time.sleep(self.refresh_rate)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"⚠️ Fallback dashboard error: {e}")
                time.sleep(5)
    
    def _display_fallback_dashboard(self):
        """Display fallback text-based dashboard"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("🧠 Intelligent Context Enhancement System - Live Monitor")
        print("=" * 60)
        print(f"Last Update: {self.last_update.strftime('%H:%M:%S')}")
        print()
        
        if self.dashboard_data:
            self._display_fallback_metrics()
        else:
            print("⏳ Collecting system data...")
        
        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
    
    def _display_fallback_metrics(self):
        """Display metrics in fallback mode"""
        data = self.dashboard_data
        
        # System metrics
        print("📊 SYSTEM METRICS")
        print("-" * 30)
        
        if 'performance' in data:
            perf = data['performance']
            health = perf.get('overall_health', 'unknown')
            health_icon = "🟢" if health == 'excellent' else "🟡" if health == 'good' else "🔴"
            
            print(f"{health_icon} Overall Health: {health.upper()}")
            print(f"⚡ Avg Response Time: {perf.get('response_time_avg', 0):.6f}s")
            print(f"💾 Cache Efficiency: {perf.get('cache_efficiency', 0):.1%}")
            print(f"🧠 Learning Effectiveness: {perf.get('learning_effectiveness', 0):.1%}")
        
        # Cache system
        print("\n💾 CACHE SYSTEM")
        print("-" * 30)
        
        if 'cache' in data:
            cache = data['cache']
            print(f"📥 Hits: {cache.get('total_hits', 0)} | ❌ Misses: {cache.get('total_misses', 0)}")
            print(f"🎯 Hit Rate: {cache.get('cache_hit_rate', 0):.1%}")
            print(f"💾 Memory: {cache.get('memory_usage_mb', 0):.2f}MB")
        
        # Learning system
        print("\n🧠 LEARNING SYSTEM")
        print("-" * 30)
        
        if 'learning' in data:
            learning = data['learning']
            stats = learning.get('learning_stats', {})
            print(f"📚 Total Learned: {stats.get('total_learned', 0)}")
            print(f"🔍 Patterns: {stats.get('patterns_recognized', 0)}")
            print(f"⚙️ Optimizations: {stats.get('strategies_optimized', 0)}")
        
        # Alerts
        alerts = data.get('alerts', [])
        if alerts:
            print(f"\n⚠️ ALERTS ({len(alerts)})")
            print("-" * 30)
            for alert in alerts[:5]:  # Show first 5 alerts
                print(f"• {alert}")
    
    def stop_monitoring(self):
        """Stop the monitoring dashboard"""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=2)
        print("🛑 Monitoring dashboard stopped")

# Global instance for easy access
monitoring_dashboard = MonitoringDashboard()

def start_dashboard(refresh_rate: float = 1.0):
    """Start the monitoring dashboard"""
    dashboard = MonitoringDashboard(refresh_rate)
    dashboard.start_monitoring()

def get_dashboard_data() -> Dict[str, Any]:
    """Get current dashboard data"""
    return monitoring_dashboard.dashboard_data if monitoring_dashboard.is_running else {}

if __name__ == "__main__":
    print("🚀 Starting Personal Monitoring Dashboard...")
    print("=" * 50)
    
    try:
        # Start the dashboard
        start_dashboard(refresh_rate=1.0)
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Dashboard failed: {e}")
        print("💡 Try running with: python3 monitoring_dashboard.py")
