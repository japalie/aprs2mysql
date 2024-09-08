from distutils.core import setup

setup(
    name='aprs2mysql',
    version='0.1.1',
    author='Patrick',
    author_email='github@japa.li',
    packages=['aprs2mysql'],
    url='https://github.com/japalie/aprs2mysql',
    license='GPLv3',
    description='Interfaces ham radio APRS-IS servers and saves packet data into an MySQL database',
    long_description=open('README.md').read(),
    install_requires=[
        "aprslib>=0.6.46",
        "certifi>=2017.7.27.1",
        "chardet>=3.0.4",
        "configparser>=3.5.0",
        "idna>=2.6",
        "pymysql>=0.9.3",
        "pbr>=3.1.1",
        "python-dateutil>=2.6.1",
        "pytz>=2017.2",
        "requests>=2.18.4",
        "six>=1.11.0",
        "urllib3>=1.22",
    ],
    entry_points={
        'console_scripts':
            ['aprs2mysql = aprs2mysql.__main__:main']
    }
)
