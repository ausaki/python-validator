from setuptools import setup, find_packages


def read_meta():
    import re
    with open('./validator/__init__.py') as fp:
        content = fp.read()
        m = re.search(
            r'__version__\s*=\s*([\'"])([^\'"]+)\1', content, re.MULTILINE)
        version = m.group(2)

    return {
        'version': version,
    }


meta = read_meta()

setup(
    name='python-validator',
    description="a data validator like Django ORM",
    version=meta['version'],
    author='ausaki',
    author_email='ljm51689@gmail.com',
    url="http://github.com/theskumar/python-dotenv",
    keywords=['validator', 'Django-ORM',
              'data validator', 'validation', 'python'],
    packages=find_packages(),
    install_requires=['six'],
)
