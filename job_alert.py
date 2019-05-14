from bs4 import BeautifulSoup as BS
import urllib
import itertools
import jobs_email


def job_alert():
    """Create HTML job alert and email"""
    # Get HTML summary of jobs today
    jobs = get_jobs()
    # Check if there are no jobs
    if jobs == None:
        return None
    # Email summary using email.conf settings
    jobs_email.send_job_email(jobs)


def get_jobs():
    """Get HTML summary of jobs from today matching search terms and location"""
    # Get search terms and locations from config files
    terms = get_terms()
    # Get urls for each term, loc pair
    urls = [gen_url(loc, term) for loc, term in terms]
    # Get job elements from indeed urls, flatten to one list
    elems = list(itertools.chain(*[grab_job_elems(url) for url in urls]))
    if len(elems) == 0:
        print "No jobs today!"
        return None
    # Strip key info from job elems
    elems = sort_job_elems(elems)
    # Convert to HTML
    jobs = output_html(elems)
    return jobs


def get_terms():
    """Get the search and location terms from the config files"""
    with open("terms.conf") as termfile:
        terms = [term.strip("\n") for term in termfile.readlines()]
    with open("locs.conf") as locfile:
        locs = [loc.strip("\n") for loc in locfile.readlines()]
    terms = list(itertools.product(terms, locs))
    return terms


def output_html(jobs):
    """Write jobs to html for emailing"""
    # Convert to list of dictionaries
    jobs = [{key : val[i] for key, val in jobs.items()} for i in xrange(len(jobs['title']))]
    html = "\n\n".join([job_format(job) for job in  jobs])
    return html


def job_format(job):
    """Format single job as HTML"""
    html_out = u"<h3>\n\t<a href={link}>\n\t\t{title}\n\t</a></h3>\n".format(**job)
    html_out += u"<b>{company} -- {loc}</b>\n".format(**job)
    html_out += u"<p>\n\t{summary}\n</p><br />".format(**job)
    return html_out


def sort_job_elems(elems):
    """Get job elements into a nice format"""
    jobs = {}
    jobs['title'] = [elem.find("a", "jobtitle turnstileLink ")['title'] for elem in elems]
    base_url = "http://www.indeed.co.uk"
    jobs['link'] = [base_url + elem.find("a", "jobtitle turnstileLink ")['href'] for elem in elems]
    jobs['company'] = [" ".join(get_text(elem.find("span", "company")).split()) for elem in elems]
    jobs['loc'] = [get_text(elem.find("span", "location")) for elem in elems]
    jobs['summary'] = [" ".join(get_text(elem.find("div", "summary")).split()) for elem in elems]
    return jobs


def get_text(soup_elem):
    """Get text from soup element, gracefully handling missing HTML elements"""
    try:
        return soup_elem.text
    except AttributeError:
        return "NA"


def grab_job_elems(url, page = 0):
    """Get job elems marked as 'Today' from indeed url""" 
    # Add page number onto url and load
    html = urllib.urlopen(url + "&start=" + str(page * 10)).read()
    soup = BS(html, "html.parser")
    # Get job card elements
    elems = soup.find_all("div", "jobsearch-SerpJobCard unifiedRow row result")
    # Add date info to elems
    elems = [(elem.find("span", "date"), elem) for elem in elems]
    # Remove sponsored ads
    elems = [(d.text, e) for d, e in elems if d != None]
    # Get only jobs posted today
    todays = [e for d, e in elems if d in ('Just posted', 'Today')]
    # If all on this page are for today look at next page recursively
    if len(todays) == len(elems):
        return todays + grab_job_elems(url, page = page + 1)
    else:
        return todays


def gen_url(title, loc):
    """Generate Indeed url from given job title and location"""
    url = "https://www.indeed.co.uk/jobs?q="
    # Remove spaces from job title
    url += "+".join(title.split())
    # Add location info
    url += "&l=" + loc
    # Sort by date
    url += "&sort=date"
    return url


if __name__ == '__main__':
    job_alert()
