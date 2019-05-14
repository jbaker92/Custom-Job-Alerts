# Custom Job Alerts

This script allows you to create custom daily job alerts which are emailed to you. It will combine multiple locations and search terms. The jobs listings are scraped from the job site Indeed (UK), and links to those job adverts are sent to your inbox.

To use simply edit the three configuration files: `email.conf`, `terms.conf`, `locs.conf`:

- `email.conf` -- contains the details for emailing the results. It does this by accessing the SMTP server `Hostname`. It assumes the password is saved using the python library `keyring`.
- `terms.conf` -- contains the search terms you wish to search for e.g. `developer`.
- `locs.conf` -- contains the locations you wish to search for. Currently it uses `indeed.co.uk` so is limited to the UK; but it is easily extendable to use other locations.

_Dependencies:_ `Python 2.x`, `BeautifulSoup4` (Python package), `keyring` (Python package).
