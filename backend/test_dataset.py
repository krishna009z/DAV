from movie_data import (
    load_imdb_dataset, 
    get_dataset_statistics, 
    get_reviews_by_sentiment,
    get_random_reviews,
    get_famous_movies_data
)

print("=" * 60)
print("Testing IMDB Dataset Integration")
print("=" * 60)

# Test 1: Load dataset
print("\n1. Loading dataset...")
df = load_imdb_dataset(limit=10)
if df is not None:
    print(f"   ✓ Successfully loaded {len(df)} reviews")
    print(f"   Columns: {df.columns.tolist()}")
else:
    print("   ✗ Failed to load dataset")

# Test 2: Get statistics
print("\n2. Getting dataset statistics...")
stats = get_dataset_statistics()
if stats:
    print(f"   ✓ Total reviews: {stats.get('total_reviews', 0)}")
    print(f"   ✓ Positive reviews: {stats.get('positive_reviews', 0)}")
    print(f"   ✓ Negative reviews: {stats.get('negative_reviews', 0)}")
else:
    print("   ✗ Failed to get statistics")

# Test 3: Get positive reviews
print("\n3. Getting positive reviews...")
positive_reviews = get_reviews_by_sentiment('positive', limit=3)
if positive_reviews:
    print(f"   ✓ Retrieved {len(positive_reviews)} positive reviews")
    print(f"   Sample: {positive_reviews[0][:100]}...")
else:
    print("   ✗ Failed to get positive reviews")

# Test 4: Get negative reviews
print("\n4. Getting negative reviews...")
negative_reviews = get_reviews_by_sentiment('negative', limit=3)
if negative_reviews:
    print(f"   ✓ Retrieved {len(negative_reviews)} negative reviews")
    print(f"   Sample: {negative_reviews[0][:100]}...")
else:
    print("   ✗ Failed to get negative reviews")

# Test 5: Get random reviews
print("\n5. Getting random reviews...")
random_reviews = get_random_reviews(count=5)
if random_reviews:
    print(f"   ✓ Retrieved {len(random_reviews)} random reviews")
else:
    print("   ✗ Failed to get random reviews")

# Test 6: Get famous movies data (now using dataset)
print("\n6. Getting famous movies data...")
movies = get_famous_movies_data()
if movies:
    print(f"   ✓ Retrieved {len(movies)} movie collections")
    for movie in movies:
        print(f"   - {movie['title']}: {len(movie.get('reviews', []))} reviews")
else:
    print("   ✗ Failed to get famous movies data")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
