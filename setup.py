from setuptools import setup, find_packages

setup(
    name='PolyglotDict',
    version='1.0.0',
    description='A library/class designed to easily create, manage, and expand a smart multilingual dictionary.',
    author='Ruben Sabatini',
    url='https://github.com/RubenSab/PolyglotDict',
    packages=find_packages(),
    install_requires=[
        'eng-to-ipa',
        'deep-translator',
        'langid',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
