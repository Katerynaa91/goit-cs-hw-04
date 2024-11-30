import time
from threading import Thread


def search_words(filename:str, words:list, found_words:dict):
    """Функція для пошуку слів у текстовому файлі"""
    try:
        with open(filename, "r", encoding='utf-8') as f:
            text = f.read().lower()
            for word in words:
                if word.lower() in text:
                    if not found_words.get(word):
                        found_words[word] = [filename]
                    else:
                        found_words[word].append(filename)
    except Exception as e:
        print(f"Error: File doesn't exist or Incorrect file format: {e}")


def threading_search(filenames, words):
    """Функція для пошуку слів у списку текстових файлів із використанням багатопотоковості"""
    threads = []
    found_words = {word: [] for word in words}

    for filename in filenames:
        thread = Thread(
            target=search_words, args=(filename, words, found_words)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return found_words


if __name__== "__main__":

    words_lookup = ['analytics', 'data', 'ai', 'technology', 'problem', 'generative', 'quality', 
                    'facebook’s', 'windows', 'prescriptive', 'analytics', 'rfp', 'statistical',
                    'alien', 'catBoris', 'word-not-in-text']
    filenames = ['txt_files/txt1.txt', 'txt_files/txt10.txt', 'txt_files/txt2.txt', 'txt_files/txt3.txt', 
                  'txt_files/txt4.txt', 'txt_files/txt5.txt', 'txt_files/txt6.txt', 'txt_files/txt7.txt', 
                  'txt_files/txt8.txt', 'txt_files/txt9.txt']


    start_regular = time.perf_counter()
    for filename in filenames:
        search_words(filename, words_lookup, found_words={})
    end_regular = time.perf_counter() - start_regular

    start = time.perf_counter()
    result = threading_search(filenames, words_lookup)
    end = time.perf_counter() - start

    print(f"Search with multithreading took: {end} seconds")      #час виконання пошуку із використанням потоків для обробки кожного файлу окремо
    print(f"Search with no multithreading took: {end_regular} seconds")   #час виконання пошуку без використання потоків
    print("Found Words:")
    for word, files in result.items():
        print(word, files)
        