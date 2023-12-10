from setuptools import setup, find_packages

setup(
    name="e_commerce_models",
    description="e_commerce database models",
    version="1.0.0",
    author="Omar Elsayd",
    author_email="omar_2546@hotmail.com",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.11"],
    install_requires=[
        "sqlalchemy",
        "fastapi",
        "uvicorn",
        "alembic",
        "psycopg2-binary",
        "uvicorn[standard]",
        "passlib",
        "python-jose",
        "python-multipart",
        "bcrypt"
        ]
)
