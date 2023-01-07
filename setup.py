import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bpcli',
    version='0.1.0',
    author='jfhovinne',
    author_email='bpcli@hovinne.com',
    license='MIT',
    description='Build apps with buildpacks and Dagger',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jfhovinne/bpcli',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
    ],
    python_requires='>=3.10',
    install_requires=[
        'asyncclick',
        'dagger-io'
    ],
    entry_points={
        'console_scripts': [
            'bpcli=bpcli.bpcli:main',
        ],
    },
)
