import re
import aiohttp
import matplotlib.pyplot as plt
import asyncio
from functools import reduce


async def fetch_text(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print("Failed to retrieve the text from the URL.")
                return ""


async def map_reduce(text_chunk):
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count


def reduce_word_counts(word_counts1, word_counts2):
    word_count_total = {}
    for word, count in word_counts1.items():
        word_count_total[word] = word_count_total.get(word, 0) + count
    for word, count in word_counts2.items():
        word_count_total[word] = word_count_total.get(word, 0) + count
    return word_count_total


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


async def main(url):
    text = await fetch_text(url)
    if text:
        chunk_size = len(text) // 10
        chunks = [text[i:i+chunk_size]
                  for i in range(0, len(text), chunk_size)]

        mapped_results = await asyncio.gather(*(map_reduce(chunk) for chunk in chunks))

        reduced_result = reduce(reduce_word_counts, mapped_results)
        visualize_top_words(reduced_result)
    else:
        print("No text retrieved from the URL.")


if __name__ == "__main__":
    url = "https://gutenberg.net.au/ebooks05/0500781.txt"
    asyncio.run(main(url))
