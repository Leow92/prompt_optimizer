from setuptools import find_packages, setup

setup(
    name="leo-prompt-optimizer",  # 🔧 Nom visible sur PyPI
    version="0.2.4",  # 🔼 Mets à jour à chaque nouvelle publication
    packages=find_packages(),  # 👌 Ça détecte bien 'leo_prompt_optimizer'
    package_data={
        "leo_prompt_optimizer": ["prompts/*.j2"],
    },
    install_requires=["jinja2>=3.1.6", "openai>=2.*", "python-dotenv>=1.2.1"],
    description="A Python library to optimize prompts from drafts and LLM inputs/outputs.",
    author="Léonard Baesen-Wagner",
    author_email="lr.baesen@gmail.com",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    project_urls={
        "Source": "https://github.com/Leow92/prompt_optimizer",
        "Documentation": "https://github.com/Leow92/prompt_optimizer#readme",
    },
    include_package_data=True,
)
