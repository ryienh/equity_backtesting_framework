from distutils.core import setup

setup(
    name='quick_backtest',
    version='0.1.2',
    description='Lightweight library for backtesting stocks, ETFs and ETNs using historical data with daily resolution',
    author='Ryien Hosseini',
    author_email='ryienh@umich.edu',
    packages=['quick_backtest',],
    license='MIT License',
    long_description=open('README.txt').read(),
)