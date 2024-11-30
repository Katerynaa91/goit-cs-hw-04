from multiprocessing import Process, Queue
import time


def search_words(filename, words, queue):
    """Функція для пошуку слів у текстовому файлі. Зберігаємо словник у чергу для подальшого використання у різних процесах"""
    found_words = {word: [] for word in words}
    try:
        with open(filename, "r", encoding='utf-8') as f:
            text = f.read().lower()
            for word in words:
                if word.lower() in text:
                    found_words[word].append(filename)
    except Exception as e:
        print(f"Error: File doesn't exist or Incorrect file format: {e}")
    queue.put(found_words)


def multiprocessing_search(filenames, words):
    """Функція для пошуку слів у списку текстових файлів із використанням багатопроцесовості.
    Обробка кожного окремого файлу виконується в окремому процесі"""
    processes = []
    queue = Queue()
    found_words = {word: [] for word in words}

    for filename in filenames:
        process = Process(
            target=search_words, args=(filename, words, queue)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        process_dict = queue.get()
        for word in process_dict:
            found_words[word].extend(process_dict[word])

    return found_words


if __name__ == "__main__":
    
    words_lookup = ['analytics', 'data', 'ai', 'technology', 'problem', 'generative', 'quality', 
                    'facebook’s', 'windows', 'prescriptive', 'analytics', 'rfp', 'statistical',
                    'alien', 'catBoris', 'word-not-in-text']
    filenames = ['txt_files/txt1.txt', 'txt_files/txt10.txt', 'txt_files/txt2.txt', 'txt_files/txt3.txt', 
                  'txt_files/txt4.txt', 'txt_files/txt5.txt', 'txt_files/txt6.txt', 'txt_files/txt7.txt', 
                  'txt_files/txt8.txt', 'txt_files/txt9.txt']

    start_regular = time.perf_counter()
    for filename in filenames:
        search_words(filename, words_lookup, queue=Queue())
    end_regular = time.perf_counter() - start_regular

    start = time.perf_counter()
    result = multiprocessing_search(filenames, words_lookup)
    end = time.perf_counter() - start

    print(f"Search with multiprocessing took: {end} seconds")     #час виконання пошуку із використанням процесів для обробки кожного файлу окремо              
    print(f"Search with no multiprocessing took: {end_regular} seconds")                 #час виконання пошуку без використання багатьох процесів
    print("Found Words:")
    for word, files in result.items():
        print(word, files)
        