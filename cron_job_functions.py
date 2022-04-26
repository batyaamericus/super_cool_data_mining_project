import scraper
import api_enrichment


if __name__ == '__main__':
    scraper.scraping()
    scraper.fill_db_tables()
    response = api_enrichment.api_enrichment()
    api_enrichment.add_info_to_db(response)
