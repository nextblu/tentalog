# tentalog
Configure your logging with a YAML file. A simple and light weight logging configuration is provided by default.

## Getting Started
To install tentalog in your environment you can simply use
```
pip install tentalog
```

## Logging with Tentacle
The Tentacle is the single unit of tentalog, managing a single logger. To start logging with tentacle you can do something like this:
```
from tentalog import Tentacle

tentacle = Tentacle(name='mylogger')

logger = tentacle.logger
logger.info("Hello World")
```
This code will use the tentalog default configuration, that contains the configuration of two logging handlers, one for the console and one for a time based file rotation of 15 days. If the "mylogger" logger is not found in configuration, the "root" logger will be used and a warning message will be showed. If the name of the logger is specified, the "root" logger will be used. If you want to use a custom configuration you can just initialize your Tentacle in this way:
```
tentacle = Tentacle(path='myconf.yaml')
```

## Versioning
We use [SemVer](http://semver.org/) for versioning.
