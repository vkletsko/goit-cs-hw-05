import os
import shutil
import asyncio
import argparse
import logging

logging.basicConfig(level=logging.ERROR)


async def read_folder(source_folder, output_folder):
    for root, _, files in os.walk(source_folder):
        tasks = []
        for file in files:
            tasks.append(copy_file(root, file, output_folder))
        await asyncio.gather(*tasks)


async def copy_file(root, file, output_folder):
    file_extension = os.path.splitext(file)[1]
    source_path = os.path.join(root, file)
    output_path = os.path.join(output_folder, file_extension.strip('.'))
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    try:
        shutil.copy(source_path, output_path)
        print(f"File {file} copied to {output_path}")
    except Exception as e:
        logging.error(f"Error copying file {file}: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Sort files")
    parser.add_argument("source_folder", help="Source folder path")
    parser.add_argument("output_folder", help="Output folder path")
    args = parser.parse_args()

    source_folder = args.source_folder
    output_folder = args.output_folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
