#from distutils.core import setup
from setuptools import setup, find_packages

# http://guide.python-distribute.org/quickstart.html
# python setup.py sdist
# python setup.py register
# python setup.py sdist upload
# pip install tornado-rest-handler
# pip install tornado-rest-handler --upgrade --no-deps
# Manual upload to PypI
# http://pypi.python.org/pypi/tornado-rest-handler
# Go to 'edit' link
# Update version and save
# Go to 'files' link and upload the file


tests_require = [
]

install_requires = [
]

setup(name='tornado-rest-handler',
      url='https://github.com/paulocheque/tornado-rest-handler',
      author="paulocheque",
      author_email='paulocheque@gmail.com',
      keywords='python tornado rest handler',
      description='A simple Python Tornado handler that manage Rest requests automatically.',
      license='MIT',
      classifiers=[
          # 'Framework :: Tornado',
          'Operating System :: OS Independent',
          'Topic :: Software Development'
      ],

      version='0.0.5',
      install_requires=install_requires,
      tests_require=tests_require,
      # test_suite='runtests.runtests',
      # extras_require={'test': tests_require},

      packages=find_packages(),
)

