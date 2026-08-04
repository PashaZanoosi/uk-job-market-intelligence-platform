# =====================================================
# description_scraper.py
# Scrape full job description from Adzuna redirect URL
# =====================================================

import requests

from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/138.0.0.0 Safari/537.36"
}


# =====================================================
# HTML → Plain text
# =====================================================

def extract_page_text(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    return soup.get_text(
        " ",
        strip=True
    )


# =====================================================
# Detect blocking
# =====================================================

def detect_block(response):

    if response.status_code in [403, 429, 503]:

        return True, f"http_{response.status_code}"

    html = response.text.lower()

    block_words = [

        "captcha",
        "cloudflare",
        "verify you are human",
        "access denied",
        "checking your browser",
        "unusual traffic"

    ]

    for word in block_words:

        if word in html:

            return True, word

    return False, None


# =====================================================
# Find beginning of job description
# =====================================================

def extract_job_start(page_text, title):

    if not title:

        return page_text

    title_index = page_text.find(title)

    if title_index == -1:

        return page_text

    text_after_title = page_text[
        title_index + len(title):
    ]

    start_points = [

        "About the job",
        "About The Job",

        "The Role",

        "We are looking",
        "We're looking",
        "We’re looking",

        "We are currently looking",

        "At ",
        "As a ",
        "You will "

    ]

    positions = []

    for point in start_points:

        index = text_after_title.find(point)

        if index != -1:

            positions.append(index)

    if positions:

        start = min(positions)

        return text_after_title[start:]

    words = text_after_title.split()

    return " ".join(words[40:])


# =====================================================
# Remove footer
# =====================================================

def clean_footer(text):

    endings = [

        "Apply for this job",
        "Stats for this job",
        "Salary comparison",
        "Similar jobs",
        "Popular searches",
        "Receive similar jobs by email",
        "Create alert"

    ]

    for ending in endings:

        index = text.find(ending)

        if index != -1:

            text = text[:index]

    return text.strip()


# =====================================================
# Main function
# =====================================================

def scrape_description(
    redirect_url,
    title
):
    """
    Returns:

    {
        status,
        description,
        status_code,
        error_type,
        html_length,
        description_length
    }
    """

    try:

        response = requests.get(

            redirect_url,

            headers=HEADERS,

            timeout=20,

            allow_redirects=True

        )

    except Exception as e:

        return {

            "status": "failed",

            "status_code": None,

            "error_type": str(e),

            "html_length": 0,

            "description_length": 0,

            "description": ""

        }

    if response.status_code == 404:

        return {

            "status": "page_not_found",

            "status_code": 404,

            "error_type": "page_not_found",

            "html_length": len(response.text),

            "description_length": 0,

            "description": ""

        }

    blocked, reason = detect_block(response)

    if blocked:

        return {

            "status": "blocked",

            "status_code": response.status_code,

            "error_type": reason,

            "html_length": len(response.text),

            "description_length": 0,

            "description": ""

        }

    page_text = extract_page_text(
        response.text
    )

    description = extract_job_start(

        page_text,

        title

    )

    description = clean_footer(
        description
    )

    return {

        "status": "success",

        "status_code": response.status_code,

        "error_type": None,

        "html_length": len(response.text),

        "description_length": len(description),

        "description": description[:6000]

    }