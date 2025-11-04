# Fix Movie Search - Step by Step

## The Problem
You changed the JWT_SECRET_KEY in the `.env` file, which made all existing JWT tokens invalid. This causes 422 errors.

## The Solution - Follow These Exact Steps:

### Step 1: Open Browser Console
1. Open your browser where the app is running
2. Press `F12` on your keyboard
3. Click the "Console" tab

### Step 2: Clear Local Storage
In the console, type this EXACTLY and press Enter:
```javascript
localStorage.clear()
```

### Step 3: Reload the Page
In the console, type this and press Enter:
```javascript
location.reload()
```

OR just press `F5` on your keyboard

### Step 4: You Should See Login Page
- If you see the login page, GOOD! ✅
- If you still see the dashboard, repeat steps 1-3

### Step 5: Create a NEW Account
**DO NOT use your old account**. Create a completely new one:
- Click "Sign up"
- Username: `testuser2`
- Email: `test2@example.com`
- Password: `password123`
- Click "Sign Up"

### Step 6: Try Movie Search
1. Click "Movie Search" in the navigation
2. Type: `Inception`
3. Click "Search"

## Expected Result:
You should see:
- Movie poster
- IMDB rating: 8.8
- Plot description
- Sentiment analysis charts

## If It Still Doesn't Work:

### Check Backend Terminal
Look for these messages after you search:
```
=== Movie Search Request ===
Movie name: Inception
MovieScraper initialized with API key: ********
Fetching movie data from: http://www.omdbapi.com/?apikey=...
```

### Check Browser Console
Look for:
- "Token verification failed, clearing token" - This is GOOD, means old token was cleared
- "Login successful" or similar - Means new login worked
- Any RED errors - Copy and send them

## Alternative: Complete Reset

If nothing works, do a complete reset:

1. **Stop Backend** (Ctrl+C in backend terminal)
2. **Delete Database:**
   ```bash
   cd c:\moviereviewanalysis\backend
   del instance\moviereview.db
   ```
3. **Start Backend:**
   ```bash
   .\venv\Scripts\python.exe app.py
   ```
4. **Clear Browser:** Press `Ctrl+Shift+Delete`, clear everything
5. **Reload Frontend:** Press `F5`
6. **Create New Account**
7. **Try Movie Search**

## Your Current Configuration:
✅ OMDB API Key: `39ff6825` (working)
✅ JWT Secret Key: `f4064426f638636f74abe3c0e94b8377`
✅ Backend: Running on port 5000
✅ Frontend: Running on port 3000

The API key works (tested successfully). The only issue is the JWT token mismatch.
