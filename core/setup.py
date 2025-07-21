from setuptools import setup, find_packages

setup(
    name="apac_core",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Dependências aqui, se tiver
    ],
    author="Seu Nome",
    author_email="seu.email@example.com",
    description="Biblioteca core para APAC",
    url="https://github.com/seu_usuario/apac_core",  # opcional
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
