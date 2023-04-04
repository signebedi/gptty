from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    DESCRIPTION = f.read()

with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()

setup(
    name='gptty',
    version="0.2.5",
    description='Chat GPT wrapper in your TTY ',
    author='Sig Janoska-Bedi',
    author_email='signe@atreeus.com',
    long_description=DESCRIPTION, 
    long_description_content_type='text/markdown',
    url="https://github.com/signebedi/gptty",
    packages=['gptty'],
    install_requires=REQUIRED,
    entry_points={
        'console_scripts': [
            'gptty=gptty.__main__:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)