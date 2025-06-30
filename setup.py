from setuptools import setup, find_packages

setup(
    name='trendpulse_bot',
    version='0.1.0',
    description='An automated trend analyzer and poll bot using LLMs with dashboard integration.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/your-username/trendpulse-bot',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        'tweepy',
        'openai',               # or 'google-generativeai'
        'requests',
        'beautifulsoup4',
        'pandas',
        'python-dotenv',
        'requests-html',        # for rendering Twitter HTML
        'gradio',               # or 'streamlit'
        'sqlite-utils',         # optional helper for DB ops
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'trendpulse=trendpulse_bot.pipeline:main',  # if pipeline.py has a `main()` function
        ],
    },
)
