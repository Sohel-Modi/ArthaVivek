import os
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from db_utils import get_db_connection

# --- INITIALIZATION ---
load_dotenv()
openai_api_key = os.getenv("LLM_API_KEY")
if not openai_api_key:
    raise ValueError("LLM_API_KEY not found. Please check your .env file.")

client = OpenAI(api_key=openai_api_key)
db_client, db, knowledge_base, _ = get_db_connection()


def scrape_article_text(url: str) -> str:
    """Scrapes the main text content from a given URL."""
    print(f"  Scraping URL: {url}...")
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        main_content = soup.find('article') or soup.find('main') or soup.body
        paragraphs = main_content.find_all('p')
        
        text = ' '.join([p.get_text() for p in paragraphs])
        print(f"  Successfully scraped {len(text)} characters.")
        return text[:4000] # Limit text to a manageable size for the LLM
    except Exception as e:
        print(f"  Error scraping {url}: {e}")
        return ""


def structure_content_with_ai(scraped_text: str, article_info: dict) -> dict:
    """Uses an LLM to summarize and structure the scraped text."""
    print("  Asking AI to summarize and structure...")
    
    system_prompt = """
    You are an expert financial analyst. Your job is to read the provided article text and create a concise, easy-to-understand summary.
    This summary will be the 'content' field in a larger JSON object.
    Focus on extracting the key educational points. The summary should be detailed enough to be useful on its own.
    """
    
    user_prompt = f"Please read the following article text and provide a detailed but simplified summary.\n\nArticle Text: \"{scraped_text}\""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )
        summary = response.choices[0].message.content
        
        # Combine AI-generated summary with manually provided metadata
        final_document = {
            "topic": article_info['topic'],
            "content": summary,
            "tags": article_info['tags'],
            "personas": article_info['personas'],
            "related_videos": article_info['related_videos'],
            "related_blogs": article_info['related_blogs']
        }
        print("  AI structuring successful.")
        return final_document
    except Exception as e:
        print(f"  Error structuring content with AI: {e}")
        return None

def ingest_articles(articles_to_process: list):
    """Main function to loop through articles, process them, and save to DB."""
    if not db_client:
        print("Database connection failed. Cannot ingest.")
        return

    total_articles = len(articles_to_process)
    print(f"Starting ingestion process for {total_articles} articles...")

    for i, article in enumerate(articles_to_process):
        print(f"\n--- Processing article {i+1}/{total_articles}: {article['topic']} ---")
        
        # Check if an article with this topic already exists to avoid duplicates
        if knowledge_base.count_documents({'topic': article['topic']}) > 0:
            print(f"Skipped: Article on '{article['topic']}' already exists.")
            continue

        scraped_text = scrape_article_text(article['url'])
        if scraped_text:
            structured_data = structure_content_with_ai(scraped_text, article)
            if structured_data:
                knowledge_base.insert_one(structured_data)
                print(f"✅ Successfully ingested and saved: {structured_data['topic']}")
        else:
            print(f"❌ Failed to scrape content for: {article['topic']}")


if __name__ == "__main__":
    # The complete, curated list of high-quality articles for the knowledge base.
    ARTICLES_TO_INGEST = [
        # Part 1: Foundational Concepts for Students
        {
            "url": "https://www.hdfcbank.com/personal/resources/learning-centre/save/types-of-bank-accounts", "topic": "Types of Bank Accounts", "personas": ["student"], "tags": ["banking", "basics", "account", "savings"], "related_videos": ["https://www.youtube.com/watch?v=nC3n-Q8gY-A"], "related_blogs": []
        },
        {
            "url": "https://www.npci.org.in/what-we-do/upi/product-overview", "topic": "What is UPI?", "personas": ["student", "professional"], "tags": ["upi", "digital payments", "basics"], "related_videos": ["https://www.youtube.com/watch?v=c_S8i21-h1s"], "related_blogs": []
        },
        {
            "url": "https://www.investopedia.com/articles/personal-finance/062615/how-budget-your-pocket-money.asp", "topic": "How to Budget Pocket Money", "personas": ["student"], "tags": ["budgeting", "saving", "student life"], "related_videos": ["https://www.youtube.com/watch?v=F_TrSO1g414"], "related_blogs": []
        },
        {
            "url": "https://www.investopedia.com/terms/c/compounding.asp", "topic": "The Power of Compounding", "personas": ["student", "professional"], "tags": ["investing", "basics", "long-term"], "related_videos": ["https://www.youtube.com/watch?v=wf91rEGw8_Q"], "related_blogs": []
        },
        {
            "url": "https://www.bankbazaar.com/credit-card/debit-card-vs-credit-card.html", "topic": "Debit Card vs Credit Card", "personas": ["student", "professional"], "tags": ["banking", "basics", "credit", "debit"], "related_videos": ["https://www.youtube.com/watch?v=zJgQd5P1j5g"], "related_blogs": []
        },
        # Part 2: Core Concepts for Professionals
        {
            "url": "https://cleartax.in/s/form-16", "topic": "Understanding Form 16 and Salary Slips", "personas": ["professional"], "tags": ["salary", "tax", "form 16", "basics"], "related_videos": ["https://www.youtube.com/watch?v=gAVpKb4k7jA"], "related_blogs": []
        },
        {
            "url": "https://zerodha.com/varsity/chapter/the-importance-of-an-emergency-fund/", "topic": "Building an Emergency Fund", "personas": ["professional"], "tags": ["saving", "safety", "emergency fund", "basics"], "related_videos": ["https://www.youtube.com/watch?v=34gM5hs-4gE"], "related_blogs": ["https://groww.in/blog/why-is-an-emergency-fund-important/"]
        },
        {
            "url": "https://www.policybazaar.com/life-insurance/term-insurance/", "topic": "What is Term Life Insurance?", "personas": ["professional"], "tags": ["insurance", "safety", "family", "protection"], "related_videos": ["https://www.youtube.com/watch?v=iT8KjTICHkM"], "related_blogs": []
        },
        {
            "url": "https://www.investopedia.com/terms/h/healthinsurance.asp", "topic": "Why You Need Health Insurance", "personas": ["professional"], "tags": ["insurance", "safety", "health", "protection"], "related_videos": ["https://www.youtube.com/watch?v=2TzT5-p6P6U"], "related_blogs": []
        },
        {
            "url": "https://www.experian.in/consumer/what-is-a-credit-score", "topic": "What is a CIBIL or Credit Score?", "personas": ["professional"], "tags": ["credit score", "cibil", "loans", "basics"], "related_videos": ["https://www.youtube.com/watch?v=APO0K8s2dJc"], "related_blogs": []
        },
        {
            "url": "https://groww.in/p/elss-tax-saving-mutual-funds", "topic": "How to Save Tax with ELSS Mutual Funds", "personas": ["professional"], "tags": ["tax saving", "investing", "mutual funds", "elss", "80c"], "related_videos": ["https://www.youtube.com/watch?v=5V56h62_f9s"], "related_blogs": []
        },
        # Part 3: General Investing & Economic Concepts
        {
            "url": "https://www.rbi.org.in/commonperson/English/Scripts/Inflation.aspx", "topic": "What is Inflation (Mehngai)?", "personas": ["student", "professional"], "tags": ["economics", "basics", "inflation"], "related_videos": ["https://www.youtube.com/watch?v=BHwJ41-a6b4"], "related_blogs": []
        },
        {
            "url": "https://groww.in/p/stock-market-basics", "topic": "What is the Stock Market (Sensex & Nifty)?", "personas": ["student", "professional"], "tags": ["investing", "stocks", "basics", "sensex", "nifty"], "related_videos": ["https://www.youtube.com/watch?v=kdxh43T54W0"], "related_blogs": []
        },
        {
            "url": "https://www.hdfcbank.com/personal/resources/learning-centre/invest/fixed-deposit-vs-mutual-funds", "topic": "Fixed Deposits (FD) vs Mutual Funds", "personas": ["student", "professional"], "tags": ["investing", "saving", "fd", "mutual funds"], "related_videos": ["https://www.youtube.com/watch?v=GugbA4s4aG8"], "related_blogs": []
        },
        {
            "url": "https://www.etmoney.com/learn/mutual-funds/what-are-index-funds/", "topic": "What are Index Funds?", "personas": ["student", "professional"], "tags": ["investing", "mutual funds", "stocks", "index funds"], "related_videos": ["https://www.youtube.com/watch?v=1n_c6tHwYpg"], "related_blogs": ["https://zerodha.com/varsity/chapter/index-funds/"]
        },
        {
            "url": "https://groww.in/p/public-provident-fund", "topic": "Public Provident Fund (PPF)", "personas": ["professional"], "tags": ["saving", "investment", "long-term", "tax saving", "ppf"], "related_videos": ["https://www.youtube.com/watch?v=wzHIIx-agw4"], "related_blogs": []
        },
        # Part 4: Loans (Education, Personal, Home)
        {
            "url": "https://www.bankbazaar.com/personal-loan/guide.html", "topic": "What is a Personal Loan?", "personas": ["professional"], "tags": ["loan", "personal loan", "credit", "basics"], "related_videos": ["https://www.youtube.com/watch?v=u1725b-wI8g"], "related_blogs": []
        },
        {
            "url": "https://housing.com/news/a-guide-to-availing-a-home-loan-in-india/", "topic": "How Home Loans Work", "personas": ["professional"], "tags": ["loan", "home loan", "property", "emi"], "related_videos": ["https://www.youtube.com/watch?v=FihPqA_33vE"], "related_blogs": []
        },
        {
            "url": "https://www.sbi.co.in/web/personal-banking/loans/education-loans", "topic": "Understanding Education Loans", "personas": ["student"], "tags": ["loan", "education loan", "student"], "related_videos": ["https://www.youtube.com/watch?v=34dF-d_rWp8"], "related_blogs": []
        },
        # Part 5: Deeper Investment & Stock Market Concepts
        {
            "url": "https://zerodha.com/varsity/chapter/introduction-to-stock-markets/", "topic": "Introduction to the Share Market", "personas": ["student", "professional"], "tags": ["share market", "stocks", "investing", "basics"], "related_videos": ["https://www.youtube.com/watch?v=fn5-sXl_a-c"], "related_blogs": ["https://groww.in/p/stock-market-basics"]
        },
        {
            "url": "https://www.investopedia.com/terms/d/demataccount.asp", "topic": "What is a Demat Account?", "personas": ["student", "professional"], "tags": ["share market", "demat account", "trading", "basics"], "related_videos": ["https://www.youtube.com/watch?v=XhGE8vOAb24"], "related_blogs": []
        },
        {
            "url": "https://www.motilaloswal.com/blog-details/25-must-know-basic-stock-market-terms/1816", "topic": "Common Share Market Terms", "personas": ["student", "professional"], "tags": ["share market", "terminology", "basics", "glossary"], "related_videos": ["https://www.youtube.com/watch?v=--x_gQUd4vA"], "related_blogs": []
        },
        {
            "url": "https://zerodha.com/varsity/chapter/introducing-mutual-funds/", "topic": "Introduction to Mutual Funds", "personas": ["student", "professional"], "tags": ["mutual funds", "investing", "sip", "basics"], "related_videos": ["https://www.youtube.com/watch?v=mfk-2n4kGWo"], "related_blogs": []
        },
        {
            "url": "https://groww.in/p/what-are-etfs", "topic": "What is an ETF (Exchange Traded Fund)?", "personas": ["student", "professional"], "tags": ["etf", "investing", "stocks", "mutual funds"], "related_videos": ["https://www.youtube.com/watch?v=S0uS82d-Gko"], "related_blogs": []
        },
        # Part 6: Trading Concepts
        {
            "url": "https://www.investopedia.com/terms/i/intraday.asp", "topic": "What is Intraday Trading?", "personas": ["professional"], "tags": ["trading", "intraday", "share market", "advanced"], "related_videos": ["https://www.youtube.com/watch?v=xZ_AkB5aN_c"], "related_blogs": ["https://zerodha.com/varsity/chapter/introduction-to-intraday-trading/"]
        },
        {
            "url": "https://www.angelone.in/knowledge-center/intraday-trading/delivery-trading", "topic": "Delivery Trading vs Intraday Trading", "personas": ["professional"], "tags": ["trading", "delivery", "share market", "investing"], "related_videos": ["https://www.youtube.com/watch?v=dEMrA_1-p2M"], "related_blogs": []
        },
        # Part 7: Tools and Calculators (Explanatory Content)
        {
            "url": "https://groww.in/calculators/sip-calculator", "topic": "How to Use an SIP Calculator", "personas": ["student", "professional"], "tags": ["sip", "calculator", "tools", "planning", "investing"], "related_videos": ["https://www.youtube.com/watch?v=zTf2T17T4zM"], "related_blogs": ["https://www.etmoney.com/tools/sip-calculator"]
        }
    ]
    
    ingest_articles(ARTICLES_TO_INGEST)
    
    if db_client:
        db_client.close()
        print("\nDatabase connection closed.")