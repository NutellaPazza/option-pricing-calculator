# Option Pricing Calculator - Quick Start Guide

## 🚀 Starting the Application

### Automatic Start (RECOMMENDED)
Simply run:
```bash
./start.sh
```

This script will:
- Kill any existing Streamlit processes
- Activate the virtual environment
- Start the server on port 8501
- Verify the server is running

### Manual Start
If you prefer to start manually:
```bash
source venv/bin/activate
streamlit run app.py
```

## 🛑 Stopping the Application

To stop the server:
```bash
./stop.sh
```

Or manually:
```bash
pkill -f streamlit
```

## 🔄 Restarting the Application

To restart (useful after code changes):
```bash
./restart.sh
```

## 🌐 Accessing the Application

Once started, open your browser and go to:
**http://localhost:8501**

## ❗ Troubleshooting

### "Can't connect to localhost:8501"
1. Make sure the server is running: `./start.sh`
2. Check if port 8501 is in use: `lsof -i :8501`
3. Try restarting: `./restart.sh`

### Server won't start
1. Kill all processes: `./stop.sh`
2. Wait 3 seconds
3. Start again: `./start.sh`

### Changes not showing
The server auto-reloads on file changes. If it doesn't:
- Refresh your browser (Cmd+R or Ctrl+R)
- Restart the server: `./restart.sh`

## 📝 Common Commands

```bash
# Check if server is running
curl -s http://localhost:8501 > /dev/null && echo "✅ Running" || echo "❌ Not running"

# View server logs
tail -f ~/.streamlit/logs/streamlit.log

# Check what's using port 8501
lsof -i :8501
```

## ✅ Everything Fixed

- ✅ Type errors in `calculations/greeks.py` (float conversion)
- ✅ Type errors in `ui/charts.py` (Callable → Any)
- ✅ Subplot vline error fixed (using add_shape instead)
- ✅ Auto-start scripts created (start.sh, stop.sh, restart.sh)
- ✅ Server will now start reliably every time

## 🎯 Next Time

Just run:
```bash
./start.sh
```

And you're ready to go! No more connection issues! 🎉
