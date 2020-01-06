import requests
from bs4 import BeautifulSoup
from wiktionaryparser import WiktionaryParser


if __name__ == "__main__":
    # Initialize parser
    parser = WiktionaryParser()
    
    wiktionaryDomain = "https://en.wiktionary.org"
    targetURL = f"{wiktionaryDomain}/w/index.php?title=Category:French_terms_with_homophones"
    currentPage = 1
    
    # Open text file to write homophones
    with open(f"french_homophones.txt", "a+", encoding="utf8") as f:
        # Initialize headers for GET request
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

        # Request to wiktionary
        req = requests.get(targetURL, headers=headers)
        # While successful crawling through the links
        while (req.status_code == 200):
            print(f"Successful GET request for page {currentPage}!")
            content = req.content
            html = BeautifulSoup(content, "html.parser")
            
            div = html.find("div", class_="mw-category-generated")
            links = div.find_all('a', href=True)
        
            # print(links)
            previousURL = targetURL
            targetURL = f"{wiktionaryDomain}{links[-1]['href']}"
            
            if currentPage == 1:
                words = links[1:-1]
            else:
                words = links[2:-2]
                
            for word in words:
                # if "ex.php" not in str(word):
                f.write(f"{word['href'][6:]}\n")  # Remove /wiki/ preffix
            # print(words)
            # f.writelines(words)
            
            print(f"\nCurrent page: {currentPage} ({previousURL}). Requesting page {currentPage + 1}: {targetURL}")
            # TODO: avoid cycling between previous/next page when content ends
            # if (targetURL != previousURL):
            #     req = requests.get(targetURL, headers=headers)
            #     currentPage += 1
            # else:
            #     break
    print('\nFailed GET request.')
    # print("\n\n{currentPage} pages scraped. End of script.\n")
