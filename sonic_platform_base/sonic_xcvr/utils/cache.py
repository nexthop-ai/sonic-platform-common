from collections import abc
import functools
import os

def read_only_cached_api_return(func):
    """Cache until func(...) returns a non-None, non-empty collections cache_value.

    Works for methods with or without arguments. Results are cached per unique
    set of positional and keyword arguments, so calls with different arguments
    are cached independently. The per-method cache is stored on the instance
    under ``_<func name>_cache`` as a dict keyed by the call arguments.
    """
    cache_name = f'_{func.__name__}_cache'

    def _make_key(args, kwargs):
        # Build a hashable key from the call arguments (excluding ``self``).
        return (args, tuple(sorted(kwargs.items())))

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not getattr(self, 'cache_enabled', False):
            return func(self, *args, **kwargs)
        cache = getattr(self, cache_name, None)
        if cache is None:
            cache = {}
            setattr(self, cache_name, cache)
        key = _make_key(args, kwargs)
        if key not in cache:
            cache[key] = func(self, *args, **kwargs)
        else:
            cache_value = cache[key]
            if cache_value is None or (isinstance(cache_value, abc.Iterable) and not cache_value):
                cache[key] = func(self, *args, **kwargs)
        return cache[key]
    return wrapper
