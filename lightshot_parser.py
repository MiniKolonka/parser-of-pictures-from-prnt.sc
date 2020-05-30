#!/usr/bin/env python3
# coding: utf-8

import os
import string
import requests
from random import choice, randint
from bs4 import BeautifulSoup


headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}  # random user-agent


def get_html(url: str) -> str or None:
    response = requests.get(url, verify=True, headers=headers)

    if response.ok:
        return response.text


def get_image_url(html: str) -> str or None:
    soup = BeautifulSoup(html, "lxml")
    img = soup.find("img", class_="no-click screenshot-image")

    try:
        url = img.get("src")
    except AttributeError:
        return None

    # Detects deleted images
    if "http" in url:
        return url


def download_image(url: str, folder_name: str) -> None:
    response = requests.get(url, verify=True, headers=headers, stream=True)

    if response.ok:
        with open(f"{folder_name}\\{randint(1000, 10000)}.jpg", "bw") as file:
            for chunk in response.iter_content(4096):
                file.write(chunk)


def generate_url() -> str:
    return "https://prnt.sc/" + ''.join(
        [choice(string.ascii_lowercase + string.digits) for _ in range(6)]
    )


def main() -> None:
    try:
        value = int(input("How many photos download?: "))
    except ValueError:
        print("Only numbers, not letters! Parser downloads 10 images")
        value = 10
    else:

        if value < 1:
            value = 1

        elif value > 70:
            if input(
                "Are you sure you want to upload {value} photos? (Y/N): "
            ).lower() == "n":
                exit()

    folder_name = "parsed_images" + str(randint(10, 100))
    os.mkdir(folder_name)

    for _ in range(value):
        # If the image is deleted from the site, the parser will find another
        while not (url := get_image_url(get_html(generate_url()))):
            pass
        download_image(url, folder_name)


if __name__ == "__main__":
    main()
