from pathlib import Path

import yaml
from elastic_enterprise_search import EnterpriseSearch

with (Path(__file__).absolute().parent.parent / "config.yml").open() as f:
    CONFIG = yaml.safe_load(f.read())


# Create our client instance.
ent_search = EnterpriseSearch(CONFIG["app_search"]["url"])


# Only executes when run as a script, not as an import.
if __name__ == "__main__":

    # If this code doesn't work, the rest of the examples won't either.
    version = ent_search.get_version()
    number, build_hash, build_date = (
        version["number"],
        version["build_hash"],
        version["build_date"],
    )

    print(f"You're running Enterprise Search v{number}")
    print(f"The build hash is {build_hash!r}")
    print(f"The build was created on {build_date}")
    print("Everything worked! :-)")


# Unpack the AppSearch client from the EnterpriseSearch client
# for use in the rest of the examples.
app_search = ent_search.app_search
