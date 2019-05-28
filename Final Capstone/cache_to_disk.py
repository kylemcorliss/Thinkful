import pickle
import atexit

# creates a pickle file with cached results so not scraping every item each time
def cache_to_disk(filename: str):
    def decorator(func):
        try:
            with open(filename, 'rb') as f:
                cache = pickle.load(f)
        except (IOError, ValueError, EOFError):
            cache = {}
        
        @atexit.register
        def save_cache():
            with open(filename, 'wb') as f:
                pickle.dump(cache, f)            

        def decorated(*args, **kwargs):
            if args not in cache:
                cache[args] = func(*args, **kwargs)

            return cache[args]
    
        return decorated
    
    return decorator