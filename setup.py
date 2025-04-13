from setuptools import setup, find_packages

setup(
    name="insta_tiktok_bot",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aiogram>=3.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
        "gallery-dl>=1.25.0",
        "tiktok-downloader>=0.2.0"
    ],
    python_requires=">=3.8",
    author="Aleksandr O.",
    author_email="aleksohotnikov@gmail.com",
    description="A Telegram bot for downloading content from Instagram and TikTok",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alexohotnikov/insta_tiktok_download_bot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 