from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from matplotlib import pyplot as plt

import requests

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        return None

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce
def map_reduce(text):
    words = text.split()

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def visualize_top_words(word_freq, top_n=10):
    sorted_word_freq = sorted(
        word_freq.items(), key=lambda x: x[1], reverse=True)
    top_words = [word[0] for word in sorted_word_freq[:top_n]]
    top_word_counts = [word[1] for word in sorted_word_freq[:top_n]]

    plt.figure(figsize=(10, 6))
    plt.bar(top_words, top_word_counts, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top {} Most Frequently Used Words'.format(top_n))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks05/0500781.txt"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        result = map_reduce(text)

        visualize_top_words(result)

        print("Результат підрахунку слів:", result)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
