from ddgs import DDGS

def web_search(query):
    results = DDGS().text(query, max_results=5)
    return "\n\n".join([f"Source: {r['href']}\n{r['body']}" for r in results])
