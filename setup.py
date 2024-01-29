from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='docker-hosts',
      version='0.1.0',
      description='Setup hosts on the host to docker containers',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='docker hosts container',
      url='http://github.com/qunxyz/docker-hosts',
      author='Gordon Yau',
      author_email='qunxyz@gmail.com',
      license='MIT',
      packages=['dockerhosts'],
      install_requires=[
          'docker',
      ],
      entry_points={
          'console_scripts': ['docker-hosts=dockerhosts.command_line:run'],
      },
      include_package_data=True,
      zip_safe=False)
