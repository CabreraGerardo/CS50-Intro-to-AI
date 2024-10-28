import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = {}
    pageLinks = corpus[page]
    if len(pageLinks):
        remainingProbability = 1 - damping_factor
        randomProbability = remainingProbability / len(corpus)
        dampingProbability = damping_factor / len(pageLinks)
        for possiblePage in corpus:
            if possiblePage in pageLinks:
                model[possiblePage] = dampingProbability + randomProbability
            else:
                model[possiblePage] = randomProbability

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    timesOnPage = {}
    currentPage = random.choice([*corpus.keys()])
    for i in range(n):
        model = transition_model(corpus, currentPage, damping_factor)
        currentPage = random.choices([*model.keys()], [*model.values()])
        if currentPage in timesOnPage:
            timesOnPage[currentPage] += 1
        else:
            timesOnPage[currentPage] = 0

    numberOfPages = len(corpus)
    pagerank = {}
    for page in timesOnPage:
        pagerank[page] = timesOnPage[page] / numberOfPages

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    numberOfPages = len(corpus)
    dampingProb = (1 - damping_factor) / numberOfPages
    pagerank = {}

    changeDiffs = {}

    while all(i <= .001 for i in [*changeDiffs.values()]):
        for currPage in corpus:
            sumOfLinksToCurrent = 0

            """ Pages linking to current one """
            linkPages = {}
            for page in corpus:
                if currPage in page:
                    linkPages.add(currPage)

            for linkPage in linkPages:
                sumOfLinksToCurrent += pagerank[page] / len(linkPages)

            pagerank[currPage] = dampingProb + sumOfLinksToCurrent

    return pagerank


if __name__ == "__main__":
    main()
