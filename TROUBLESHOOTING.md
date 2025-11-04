# Troubleshooting Guide

## Issue: 422 UNPROCESSABLE ENTITY / 401 UNAUTHORIZED

### Quick Fix:

1. **Clear Browser Storage:**
   - Press `F12` to open DevTools
   - Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
   - Click "Local Storage" → `http://localhost:3000`
   - Right-click and select "Clear"
   - Refresh the page (`F5`)

2. **Create a New Account:**
   - Go to the Signup page
   - Create a completely new account with a new username
   - This will create a fresh user in the database

3. **If Still Not Working - Full Reset:**

### Full Reset Instructions:

**Step 1: Stop All Servers**
- Close all terminal windows running the backend and frontend

**Step 2: Delete the Database**
```bash
cd c:\moviereviewanalysis\backend
del moviereview.db
```

**Step 3: Restart Backend**
```bash
cd c:\moviereviewanalysis\backend
.\venv\Scripts\python.exe app.py
```

**Step 4: Restart Frontend**
```bash
cd c:\moviereviewanalysis\frontend
npm start
```

**Step 5: Clear Browser Cache**
- Press `Ctrl + Shift + Delete`
- Clear "Cached images and files"
- Clear "Cookies and site data"

**Step 6: Create New Account**
- Go to `http://localhost:3000`
- Click "Sign up"
- Create a new account

## Common Issues:

### Movie Search Not Working
- Make sure OMDB API key is in `.env` file
- Backend must be restarted after adding API key
- Clear browser cache and login again

### Login Fails
- Database might be corrupted - delete `moviereview.db` and restart
- Make sure backend is running on port 5000
- Check browser console for specific errors

### CORS Errors
- Backend must be running before frontend
- Make sure CORS is configured in `app.py`
- Try hard refresh: `Ctrl + Shift + R`
