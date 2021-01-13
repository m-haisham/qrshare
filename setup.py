from setuptools import setup, find_packages

import qrshare

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='qrshare',
    version=qrshare.__version__,
    author="Schicksal",
    description="flask waitress svelte file share program",
    author_email='mhaisham79@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',

    entry_points={
        "console_scripts": ["qrshare=qrshare.__main__:serve"]
    },
    install_requires=requirements,
    package_data={
        'qrshare': [
            'client/public/build/*',
            'client/public/*',
            'client/scripts/*',
            'client/src/**/*',
            'client/src/*',
            'client/*',
        ]
    },
    include_package_data=True,

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
    license="MIT license",
    keywords='qr share localhost',

    url='https://github.com/mHaisham/qrshare',
    project_urls={
        'Source code': 'https://github.com/mHaisham/qrshare'
    },
    packages=find_packages(),
    python_requires='>=3.6'
)

