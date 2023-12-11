from setuptools import setup, find_packages

setup(
    name='exchanges_coins_list',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-telegram-bot',
        'python-dotenv'
    ],
)
