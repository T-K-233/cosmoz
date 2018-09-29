import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name = 'cosmoz',
    version = '0.5.0',
    author = '-T.K.-',
    author_email = 'tk.fantasy.233@gmail.com',
    description = '',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/T-K-233/cosmoz',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['keyboard', 'opencv-python'],
    entry_points={}
)
