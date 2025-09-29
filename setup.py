from setuptools import setup, find_packages

setup(
    name='leo-prompt-optimizer',  # 🔧 Nom visible sur PyPI
    version='0.1.9',              # 🔼 Mets à jour à chaque nouvelle publication
    packages=find_packages(),     # 👌 Ça détecte bien 'leo_prompt_optimizer'
    install_requires=[
        'groq',
        'openai',
        'python-dotenv'
    ],
    description='A Python library to optimize prompts from drafts and LLM inputs/outputs.',
    author='Léonard Baesen-Wagner',
    author_email='lr.baesen@gmail.com',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    project_urls={
        "Source": "https://github.com/Leow92/prompt_optimizer",
        "Documentation": "https://github.com/Leow92/prompt_optimizer#readme",
    },
    include_package_data=True,
)
