"""
Configuration singleton for the bot.
Handles locale settings and other global configurations.
"""

from enum import Enum
from typing import Optional
import argparse


class Locale(Enum):
	"""Supported locales for the bot."""

	EN = 'EN'
	TR = 'TR'


class Config:
	"""
	Singleton configuration class for the bot.
	Handles global settings like locale preferences.
	"""

	_instance: Optional['Config'] = None
	_initialized: bool = False
	_locale: Locale = Locale.EN

	def __new__(cls) -> 'Config':
		"""Ensure only one instance of Config exists."""
		if cls._instance is None:
			cls._instance = super(Config, cls).__new__(cls)
		return cls._instance

	@classmethod
	def initialize(cls) -> None:
		"""
		Initialize the configuration with locale from command line arguments.
		Can only be called once at startup.

		Raises:
		    RuntimeError: If initialize is called more than once
		    ValueError: If an invalid locale is provided
		"""
		if cls._initialized:
			raise RuntimeError('Config has already been initialized')

		parser = argparse.ArgumentParser()
		parser.add_argument(
			'--locale',
			type=str,
			default='EN',
			choices=['EN', 'TR'],
			help='Locale to use (EN or TR)',
		)
		args = parser.parse_args()
		print(args)

		try:
			cls._locale = Locale(args.locale)
		except ValueError:
			raise ValueError(f'Invalid locale: {args.locale}')

		cls._initialized = True

	@classmethod
	def get_locale(cls) -> Locale:
		"""
		Get the current locale setting.

		Returns:
		    The current locale setting

		Raises:
		    RuntimeError: If Config hasn't been initialized
		"""
		if not cls._initialized:
			raise RuntimeError('Config must be initialized before use')
		return cls._locale

	def __setattr__(self, name: str, value: any) -> None:
		"""Prevent modification of attributes after initialization."""
		if self._initialized:
			raise RuntimeError('Config is immutable after initialization')
		super().__setattr__(name, value)


# Initialize the config at the first import of the module
Config.initialize()
