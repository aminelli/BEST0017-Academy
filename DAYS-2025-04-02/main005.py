import gc
import psutil

rss = psutil.Process().memory_info().rss
print(rss / 1024 ** 2, "MB")
gc.collect()

print("fine programma")