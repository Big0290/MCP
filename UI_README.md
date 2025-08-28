# 🧠 Context Manager UI

A simple, modern web interface for managing and monitoring your context system.

## ✨ Features

- **📊 Dashboard**: Real-time system overview with metrics and charts
- **💬 Interactions**: View and filter conversation interactions
- **🔄 Sessions**: Monitor active user sessions
- **🧠 Contexts**: Analyze context objects and usage patterns
- **⚙️ System Status**: Check system health and capabilities

## 🚀 Quick Start

### Option 1: Using the launcher script (Recommended)
```bash
./run_ui.sh
```

### Option 2: Manual launch
```bash
# Install dependencies
pip3 install -r requirements_ui.txt

# Launch the UI
streamlit run context_ui.py
```

The UI will automatically open in your browser at `http://localhost:8501`

## 📋 Prerequisites

- Python 3.7+
- Context system running (database should exist)
- Required Python packages (auto-installed by launcher)

## 🎯 What You Can Do

### Dashboard
- View system metrics (interactions, sessions, contexts)
- Monitor recent activity trends
- Check error rates and system health

### Interactions
- Browse all conversation interactions
- Filter by type, status, or time
- Export data to CSV
- View detailed interaction content

### Sessions
- Monitor active user sessions
- Track session activity and context
- Drill down into session details

### Contexts
- Analyze context objects
- View usage patterns and relevance scores
- Monitor context creation and usage

### System Status
- Check context system availability
- Verify database connectivity
- View system capabilities
- Monitor component health

## 🔧 Configuration

The UI automatically connects to your local SQLite database at `./data/agent_tracker_local.db`. Make sure:

1. Your context system is running
2. The database file exists
3. You have the necessary permissions

## 🎨 Customization

The UI uses Streamlit with custom CSS styling. You can modify:

- Colors and themes in the CSS section
- Chart types and visualizations
- Data display formats
- Export options

## 🐛 Troubleshooting

### Database Connection Issues
- Ensure the context system is running
- Check if `./data/agent_tracker_local.db` exists
- Verify database permissions

### Missing Dependencies
- Run `pip3 install -r requirements_ui.txt`
- Check Python version compatibility

### UI Not Loading
- Check if port 8501 is available
- Verify Streamlit installation
- Check browser console for errors

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## 🔒 Security Notes

- The UI runs locally on your machine
- Database access is read-only for safety
- No external network access required
- All data stays on your local system

## 🚀 Next Steps

After exploring the UI, you can:

1. **Extend functionality**: Add new pages or features
2. **Customize visualizations**: Modify charts and graphs
3. **Add real-time updates**: Implement live data refresh
4. **Export capabilities**: Add more data export formats
5. **User management**: Add authentication if needed

## 📞 Support

If you encounter issues:

1. Check the system status page
2. Verify database connectivity
3. Review error messages in the UI
4. Check the context system logs

---

**Happy Context Managing! 🧠✨**
