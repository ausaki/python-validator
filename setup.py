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


def readme():
    with open('./README.md') as fp:
        content = fp.read()
    return content


meta = read_meta()

setup(
    name='python-validator',
    version=meta['version'],
    author='ausaki',
    author_email='ljm51689@gmail.com',
    description="a data validator like Django ORM",
    long_description=readme(),
    long_description_content_type='text/markdown',
    url="http://github.com/ausaki/python-validator",
    keywords=['validator', 'like Django-ORM',
              'data validator', 'validation', 'python'],
    packages=['validator'],
    python_requires='>=2.6',
    install_requires=['six>=1.11.0', 'IPy>=0.83'],
    extras_require={
        'tzinfo': ['pytz>=2018.5']
    },
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
