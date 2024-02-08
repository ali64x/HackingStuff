from setuptools import setup, find_packages

setup(
    name='findxss',
    version='1.0.0',
    packages=find_packages(),
    package_data={
        '': ['*.txt'],  # Include all .txt files in the package root
    },

    # Metadata
    author='ali64x',
    author_email='htlr780@gmail.com',
    description='A Python tool for finding xss.',
    url='https://github.com/ali64x/paramspider-mod',
    license='MIT',

    # Entry point to make your script executable
    entry_points={
        
        'console_scripts': [
            'findxss = findxss.findxss:main',
        ],
    },

    # Dependencies
    install_requires=[
       'requests',
       'termcolor'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
