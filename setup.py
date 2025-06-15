from setuptools import setup, find_packages

setup(
    name="ecoagent-framework",
    version="2.0.0",
    description="Framework open-source d'agents d'IA collaboratifs pour le développement logiciel économique",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jean Bargibant",
    author_email="contact@ecoagent.dev",
    url="https://github.com/jeanbgt59/EcoAgent-Framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    
    # AJOUT CRUCIAL : Point d'entrée pour la CLI
    entry_points={
        'console_scripts': [
            'ecoagent=ecoagent.cli.cli:cli_main',
        ],
    },
    
    # AJOUT : Dépendances CLI
    install_requires=[
        # Vos dépendances existantes
        'typer>=0.9.0',
        'rich>=13.0.0',
        'psutil>=5.9.0',
        'click>=8.0.0',
        # Ajoutez vos autres dépendances existantes ici
    ],
    
    # OPTIONNEL : Dépendances de développement
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ],
    },
    
    include_package_data=True,
    zip_safe=False,
)