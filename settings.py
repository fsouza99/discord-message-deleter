import json

from constants import CONFIG_FILE


class Settings:
    """Settings defined in JSON file, accessed as an object."""

    def __init__(self):
        """Load settings from JSON source file."""
        self.src_path = CONFIG_FILE

        try:
            with open(self.src_path, encoding='utf8') as file:
                data = json.load(file)
        except:
            raise Exception(
                f'Settings could not be loaded from file: {self.src_path}.')

        for scope in data.values():
            for key, value in scope.items():
                setattr(self, key, value)

        return

    def search_key(self) -> str:
        if self.searchkey is not None:
            return self.searchkey

        prefixes = (
            ('de:', self.username),
            ('em:', self.channel),
            ('tem:', self.item),
            ('menciona:', self.mention),
            ('antes:', self.before),
            ('depois:', self.after),
            ('durante:', self.during),
            ('', self.sentence))

        return ' '.join(
            f'{prefix} {value}'
            for prefix, value in prefixes
            if value is not None)

    def briefing(self) -> str:
        return (
            f'User: {self.username}\n'
            f'Target server: {self.server}\n'
            f'Search key: "{self.search_key()}"')
