from setuptools import setup, find_packages

setup(
    name="roast-me-app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pillow',
        'requests',
        'python-dotenv'
    ],
)