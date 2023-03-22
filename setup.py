from setuptools import setup, find_packages

setup(
    name='gptty',
    version='0.1.0',
    description=' Chat GPT wrapper in your TTY ',
    author='Sig Janoska-Bedi',
    author_email='signe@atreeus.com',
    packages=find_packages(),
    install_requires=[
        'click',
        'pandas',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'gptty=gptty.__main__:main',
        ],
    },
)