import nltk

print("Downloading NLTK data...")
try:
    nltk.download('brown')
    nltk.download('punkt')
    nltk.download('punkt_tab')
    print("NLTK data downloaded successfully!")
except Exception as e:
    print(f"Error downloading NLTK data: {e}")
    print("The app will still work, but TextBlob might have limited functionality.")
