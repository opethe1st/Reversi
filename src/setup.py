from setuptools import (
    setup,
    find_packages,
)

setup(
    name='Reversi',
    version='0.0.1',
    description="Reversi",
    url='http://github.com/opethe1st/Reversi',
    author='Opemipo Ogunkola (Ope)',
    author_email='ogunks900@gmail.com',
    license='MIT',
    # TODO(ope): figure out if this exclude is truely working - I think it is not
    packages=find_packages(where=".", exclude=[".*_test.py", "tests"]),
    zip_safe=False
)
