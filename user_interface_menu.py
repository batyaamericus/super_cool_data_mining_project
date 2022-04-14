import sys
import argparse
import NewArgParser as nap
import interface_functions as uif
from db_search_functions import DBsearch
import scraper
import database
import api_enrichment
import config as CONF


def main_menu():
    """This function displays the main menu prompting the user to selected company or positions search"""

    CONF.MENU_LOGGER.info("Entering main menu.")
    db_connector = DBsearch()
    sys.stdout.write('Welcome to the Comeet Scraper!\n')
    args = None
    while True:
        print("Please choose if you want to search for a company or for open job positions. Type 'c' for the former and"
              " 'p' for the latter.\n"
              "Type '-h' for help and '-q' to quit the program.")
        command = input("Enter command :")
        CONF.MENU_LOGGER.debug(f"User input: {command}")
        parser = nap.NewArgParser(exit_on_error=False)

        subparsers = parser.add_subparsers(help="Type of search: 'c' for company search and 'p' for positions search")
        parser.add_argument('-Q', '--quit', '-q', action='store_true', help="Exit the application")

        company_search_parser = subparsers.add_parser("c")
        positions_search_parser = subparsers.add_parser("p")

        company_search_parser.set_defaults(func=search_company_menu)
        positions_search_parser.set_defaults(func=search_positions_menu)

        try:

            args, unknown = parser.parse_known_args(command.split())
            if args.quit:
                sys.stdout.write('Thank you for using Comeet Parser!\n'
                                 'We hope you have found all the information you were after!\n'
                                 'Exiting the Application...')
                quit()

            if not hasattr(args, 'func'):
                print("argument {c,p}: invalid choice:", ' '.join(unknown), " (choose from 'c', 'p')")
                parser.print_usage()
                CONF.MENU_LOGGER.error("Invalid search parameter entered for main menu")
                continue

            CONF.MENU_LOGGER.debug(f"User input parsed successfully. Calling {getattr(args, 'func')}")
            args.func(db_connector)

        except argparse.ArgumentError as error:
            CONF.MENU_LOGGER.error(f"{error}")
            print(error)
            continue
        except SystemExit:
            if args is not None:
                if args.quit:
                    CONF.MENU_LOGGER.info("Quitting application.")
                    quit()
            continue


def search_company_menu(db_connector):
    """This function presents a sub-menu for users who have selected to search for companies.
        It prompts the users to search the search and display parameters for the output.
        Finally it calls comp_search_db to preform the search."""

    CONF.MENU_LOGGER.info(f"Entering menu for company search")

    print("You have selected to search for a company!")

    CONF.MENU_LOGGER.debug(f"Calling {uif.setting_comp_search_params}")
    comp_params = uif.setting_comp_search_params()

    # if return value is False, the user selected -b
    if not comp_params:
        CONF.MENU_LOGGER.info(f"Returning to main menu.")
        return

    CONF.MENU_LOGGER.debug(f"Calling {uif.setting_display_params}")
    display_params = uif.setting_display_params()


    # if return value is False, the user selected -x
    if not display_params:
        CONF.MENU_LOGGER.info(f"Returning to main menu.")
        return

    posit_disp_params = None
    if display_params['positions'] or display_params['all']:
        CONF.MENU_LOGGER.debug(f"Calling {uif.setting_posit_display_params}")
        posit_disp_params = uif.setting_posit_display_params()
        # if return value is False, the user selected -x
        if not posit_disp_params:
            CONF.MENU_LOGGER.info(f"Returning to main menu.")
            return

    CONF.MENU_LOGGER.debug(f"Calling {db_connector.comp_search_db} with parameters: \n comp_params= {comp_params}, \n display_params= {display_params}, \n posit_disp_params={posit_disp_params}")
    db_connector.comp_search_db(comp_params, display_params, posit_disp_params)


def search_positions_menu(db_connector):
    """This function presents a sub-menu for users who have selected to search for open positions.
            It prompts the users to search the search and display parameters for the output.
            Finally it calls posit_search_db to preform the search."""

    CONF.MENU_LOGGER.info(f"Entering menu for positions search")

    CONF.MENU_LOGGER.debug(f"Calling {uif.setting_posit_search_params}")
    posit_params = uif.setting_posit_search_params()

    # if return value is False, the user selected -b
    if not posit_params:
        CONF.MENU_LOGGER.info(f"Returning to main menu")
        return

    CONF.MENU_LOGGER.debug(f"Calling {uif.setting_posit_display_params}")
    posit_display_params = uif.setting_posit_display_params()
    # if return value is False, the user selected -x
    if not posit_display_params:
        CONF.MENU_LOGGER.info(f"Returning to main menu")
        return

    CONF.MENU_LOGGER.debug(f"Calling {db_connector.posit_search_db} with parameters: \n posit_params= {posit_params}, \n posit_display_params= {posit_display_params}")
    db_connector.posit_search_db(posit_params, posit_display_params)


if __name__ == '__main__':
    # database.create_db()
    # database.create_tables()
    # scraper.scraping()
    # scraper.fill_db_tables()
    # # response=api_enrichment.api_enrichment()
    # response={'status': 200, 'data': [{'name': 'trigo', 'size': '10001+', 'employee_count': 2192, 'id': 'trigo-group', 'founded': 1997, 'industry': 'automotive', 'naics': [{'naics_code': '54', 'sector': 'professional, scientific, and technical services', 'sub_sector': None, 'industry_group': None, 'national_industry': None}], 'sic': [{'sic_code': '7389', 'major_group': 'business services', 'industry_group': 'miscellaneous business services', 'industry_sector': 'business services, not elsewhere classified'}], 'location': {'name': 'nanterre, ile-de-france, france', 'locality': 'nanterre', 'region': 'ile-de-france', 'metro': None, 'country': 'france', 'continent': 'europe', 'street_address': None, 'address_line_2': None, 'postal_code': None, 'geo': '48.89,2.20'}, 'linkedin_id': '3161462', 'linkedin_url': 'linkedin.com/company/trigo-group', 'facebook_url': None, 'twitter_url': None, 'profiles': ['linkedin.com/company/trigo-group', 'linkedin.com/company/3161462', 'crunchbase.com/organization/trigo-3'], 'website': 'trigo-group.com', 'ticker': None, 'type': 'private', 'summary': 'quality along the supply chain\n\n founded in 1997, trigo group is a multinational company providing quality solutions for the automotive, aerospace and other transport industries. with more than 5000 employees worldwide, our company offers a comprehensive portfolio of inspection and management services to address the quality challenges of various supply chains. operating a cutting-edge global know-how transfer network, trigo has become the world’s largest player in the quality sector with a growing number of subsidiaries set on four continents.\n\n\n one stop shop on the quality highway\n comprehensive quality solutions from containment action services to refined quality development packages along the supply chain (for oems, tier1s and tier2s).\n\n holistic approach // customized solutions\n customized service delivery to address individual quality issues and resolve the root causes.\n\n local expertise with global drive\n the collaboration of trigo’s global, cutting-edge know-how network and loc', 'tags': ['gestion qualité', 'quality management', 'automobile', 'aerospace', 'automotive', 'quality control', 'railway', 'rework', 'certification support', 'audit'], 'headline': 'Global Quality Solutions', 'alternative_names': ['trigo group', 'trigo qualitaire', 'trigo serbia', 'trigo france', 'trigo quality services (thailand)', 'trigo qualitaire ibérica', 'trigo c.e.e.', 'trigo quality support ltd.', 'trigo solutions', 'trigo quality production services pvt. ltd.'], 'affiliated_profiles': ['treq-services']}, {'name': 'maytronics', 'size': '1001-5000', 'employee_count': 434, 'id': 'maytronics', 'founded': 1983, 'industry': 'electrical/electronic manufacturing', 'naics': [{'naics_code': '335', 'sector': 'manufacturing', 'sub_sector': 'electrical equipment, appliance, and component manufacturing', 'industry_group': None, 'national_industry': None}, {'naics_code': '453998', 'sector': 'retail trade', 'sub_sector': 'miscellaneous store retailers', 'industry_group': 'other miscellaneous store retailers', 'national_industry': 'all other miscellaneous store retailers (except tobacco stores)'}], 'sic': [{'sic_code': '7299', 'major_group': 'personal services', 'industry_group': 'miscellaneous personal services', 'industry_sector': 'miscellaneous personal services, not elsewhere classified'}], 'location': {'name': 'illinois, united states', 'locality': None, 'region': 'illinois', 'metro': None, 'country': 'united states', 'continent': 'north america', 'street_address': None, 'address_line_2': None, 'postal_code': None, 'geo': None}, 'linkedin_id': '1152712', 'linkedin_url': 'linkedin.com/company/maytronics', 'facebook_url': 'facebook.com/maytronics', 'twitter_url': 'twitter.com/maytronicsla', 'profiles': ['linkedin.com/company/maytronics', 'linkedin.com/company/1152712', 'facebook.com/maytronics', 'twitter.com/maytronicsla', 'crunchbase.com/organization/maytronics'], 'website': 'maytronics.com', 'ticker': None, 'type': 'private', 'summary': 'founded in 1983, maytronics was the pioneer in automated electronic pool cleaning technology for private and commercial pools, developing the world-renowned dolphin robot cleaners. over the years, maytronics became the acknowledged market leader, setting worldwide standards for unmatched technological innovation coupled with highly aesthetic designs. together with our partners, we seek outstanding quality products and services which provide our customers with an exceptional experience. today, more than 25 years later, maytronics’ vision is to provide a select range of novel pool care solutions, focusing on pool cleaning, environment-friendly water treatment and pool safety.', 'tags': ['ecology', 'alarms', 'robotic cleaners', 'water motor', 'water treatment', 'swimming pools', 'natural pools', 'pool cleaners robots', 'pool safety', 'water'], 'headline': 'Exceptional Experience', 'alternative_names': ['maytronics us', 'maytronics israel', 'electronic swimming pool cleaners', 'maytronics u.s.', 'maytronics ltd', 'maytronics us, inc.', 'mg international maytronics france côtée alternext', 'maytronics/dolphin', 'maytronics/poseidon technologies', 'water technologies at maytronics'], 'affiliated_profiles': ['digital-user-manuals']}, {'name': 'playtika', 'size': '1001-5000', 'employee_count': 3464, 'id': 'playtika', 'founded': 2010, 'industry': 'computer games', 'naics': [{'naics_code': '5112', 'sector': 'information', 'sub_sector': 'publishing industries (except internet)', 'industry_group': 'software publishers', 'national_industry': None}], 'sic': [{'sic_code': '7372', 'major_group': 'business services', 'industry_group': 'computer programming, data processing, and other computer related services', 'industry_sector': 'prepackaged software'}], 'location': {'name': 'herzliya, tel aviv, israel', 'locality': 'herzliya', 'region': 'tel aviv', 'metro': None, 'country': 'israel', 'continent': 'asia', 'street_address': '8 hachoshlim street', 'address_line_2': None, 'postal_code': None, 'geo': '32.16,34.82'}, 'linkedin_id': '1919232', 'linkedin_url': 'linkedin.com/company/playtika', 'facebook_url': 'facebook.com/playtika', 'twitter_url': 'twitter.com/playtika_ltd', 'profiles': ['linkedin.com/company/playtika', 'linkedin.com/company/1919232', 'facebook.com/playtika', 'twitter.com/playtika_ltd', 'crunchbase.com/organization/playtika'], 'website': 'playtika.com', 'ticker': None, 'type': 'private', 'summary': 'playtika captivates audiences with beautifully produced, highly immersive social games. we consider ourselves storytellers and artists, gamers and strategists. we pair art with science—sophisticated algorithms that deliver a pace and rhythm in each game and heighten the thrill of winning. whether players are looking for something that is funny or dramatic, playful or full of intrigue, playtika’s diverse portfolio of games will inspire them to play, stay and ultimately pay for a highly entertaining experience.\n\n playtika’s roots are in the social casino space. we were the first to introduce free-to-play casino-style games to social networks. (slotomania remains the highest grossing app on facebook and ios.) we are successfully applying our intuitive understanding of what players want and our mastery of marketing and monetization to additional categories of games, such as bingo and strategy games. our playtika studios are hives of creativity, with the independence and flexibility to inno', 'tags': ['developers', 'social games giant', 'mobile games', 'multi-platform integration', 'user acquisition & moneitzation', 'social games', 'online games', 'gaming', 'big data', 'analytics'], 'headline': 'Creating Infinite Ways to Play', 'alternative_names': ['playtika montreal', 'playtika (house of fun)', 'playtika | caesars interactive entertainment inc.', 'playtika ukraine', 'playtika belarus', 'playtika ltd', 'playtika\\pacific interactive', 'playtika ltd.', 'playtika - santa monica', 'playtika japan'], 'affiliated_profiles': []}, {'name': 'vi', 'size': '1001-5000', 'employee_count': 282, 'id': 'vicareers', 'founded': 1987, 'industry': 'marketing and advertising', 'naics': [{'naics_code': '54199', 'sector': 'professional, scientific, and technical services', 'sub_sector': 'professional, scientific, and technical services', 'industry_group': 'other professional, scientific, and technical services', 'national_industry': None}], 'sic': [{'sic_code': '7299', 'major_group': 'personal services', 'industry_group': 'miscellaneous personal services', 'industry_sector': 'miscellaneous personal services, not elsewhere classified'}], 'location': None, 'linkedin_id': '27898', 'linkedin_url': 'linkedin.com/company/vicareers', 'facebook_url': 'facebook.com/vicareers', 'twitter_url': None, 'profiles': ['linkedin.com/company/vicareers', 'linkedin.com/company/27898', 'facebook.com/vicareers'], 'website': 'vi.ru', 'ticker': None, 'type': 'private', 'summary': 'vi is the largest operator of the advertising media market in russia and eastern europe. the company sells advertising capacities and provides media with comprehensive analytical services, legal and it-support. vi serves leading tv channels across russia and cis, russian federal radio stations, internet resources, cinema chains, as well as dooh inside shopping malls, supermarkets, airports, etc. among vi customers are the largest russian media holdings: channel one, vgtrk, prof-media, national media group, russian media group, utv, discovery tv channel, yandex, cinema park and kinostar deluxe, a trading company x5 retail group and others. vi lends large-scale support to the sale process to everest-s agencies selling advertising opportunities of ctc media holding. - year of foundation - 1987 - founders - yury zapol (1956-2005) and mikhail lesin (1958-2015) - about 2 000 employees - annual trade turnover in 2015 - 86 bln rub - acar member from 1993 - egta member from 2004 - member of the', 'tags': None, 'headline': None, 'alternative_names': ['video international', 'video international trend', 'imho vi', 'vi (video international)', 'video international  kiev', 'vi-radio', 'media service (video international group)', 'video international bulgaria', 'video international - prioritet', 'video international new media department'], 'affiliated_profiles': []}, {'name': 'vi', 'size': '1001-5000', 'employee_count': 1127, 'id': 'viliving', 'founded': 1987, 'industry': 'hospitality', 'naics': [{'naics_code': '811219', 'sector': 'other services (except public administration)', 'sub_sector': 'repair and maintenance', 'industry_group': 'electronic and precision equipment repair and maintenance', 'national_industry': 'other electronic and precision equipment repair and maintenance'}, {'naics_code': '531110', 'sector': 'real estate and rental and leasing', 'sub_sector': 'real estate', 'industry_group': 'lessors of real estate', 'national_industry': 'lessors of residential buildings and dwellings'}, {'naics_code': '623990', 'sector': 'health care and social assistance', 'sub_sector': 'nursing and residential care facilities', 'industry_group': 'other residential care facilities', 'national_industry': 'other residential care facilities'}, {'naics_code': '623311', 'sector': 'health care and social assistance', 'sub_sector': 'nursing and residential care facilities', 'industry_group': 'continuing care retirement communities and assisted living facilities for the elderly', 'national_industry': 'continuing care retirement communities'}, {'naics_code': '62151', 'sector': 'health care and social assistance', 'sub_sector': 'ambulatory health care services', 'industry_group': 'medical and diagnostic laboratories', 'national_industry': None}, {'naics_code': '621999', 'sector': 'health care and social assistance', 'sub_sector': 'ambulatory health care services', 'industry_group': 'other ambulatory health care services', 'national_industry': 'all other miscellaneous ambulatory health care services'}, {'naics_code': '623312', 'sector': 'health care and social assistance', 'sub_sector': 'nursing and residential care facilities', 'industry_group': 'continuing care retirement communities and assisted living facilities for the elderly', 'national_industry': 'assisted living facilities for the elderly'}], 'sic': [{'sic_code': '8071', 'major_group': 'health services', 'industry_group': 'medical and dental laboratories', 'industry_sector': 'medical laboratories'}], 'location': {'name': 'chicago, illinois, united states', 'locality': 'chicago', 'region': 'illinois', 'metro': 'chicago, illinois', 'country': 'united states', 'continent': 'north america', 'street_address': '233 south wacker drive', 'address_line_2': 'suite 8400', 'postal_code': '60606', 'geo': '41.85,-87.65'}, 'linkedin_id': '20016', 'linkedin_url': 'linkedin.com/company/viliving', 'facebook_url': None, 'twitter_url': None, 'profiles': ['linkedin.com/company/viliving', 'linkedin.com/company/20016'], 'website': 'viliving.com', 'ticker': None, 'type': 'private', 'summary': 'vi is an owner, operator, and developer of exclusive continuing care retirement communities (ccrcs) with locations in some of the most desirable areas throughout the united states. recognized as a top employer, we are committed to enhancing the lives of our residents, and investing in the development of our employees. from the service our communities provide to the entrepreneurial spirit that drives our culture, vi offers talented, motivated individuals an inspiring and fulfilling place to thrive. learn more about us and apply today! bring life to your career.', 'tags': ['food & beverage', 'memory suppot', 'skilled nursing', 'culinary', 'ccrc', 'housekeeping', 'elder care', 'wellness', 'hospitality', 'senior living'], 'headline': 'Bring Life to Your Career!', 'alternative_names': ['vi, formerly known as classic residence by hyatt', 'classic residence by hyatt', 'vi at silverstone', 'vi at grayhawk', 'vi (formerly classic residence by hyatt)', 'vi at bentley village', 'vi at palo alto', 'vi at la jolla village', 'vi at highlands ranch', 'vi at aventura'], 'affiliated_profiles': []}, {'name': 'ironsource', 'size': '501-1000', 'employee_count': 985, 'id': 'ironsource', 'founded': 2010, 'industry': 'internet', 'naics': [{'naics_code': '54151', 'sector': 'professional, scientific, and technical services', 'sub_sector': 'professional, scientific, and technical services', 'industry_group': 'computer systems design and related services', 'national_industry': None}], 'sic': [{'sic_code': '737', 'major_group': 'business services', 'industry_group': 'computer programming, data processing, and other computer related services', 'industry_sector': None}], 'location': {'name': 'tel aviv, israel', 'locality': None, 'region': 'tel aviv', 'metro': None, 'country': 'israel', 'continent': 'asia', 'street_address': None, 'address_line_2': None, 'postal_code': None, 'geo': None}, 'linkedin_id': '2657359', 'linkedin_url': 'linkedin.com/company/ironsource', 'facebook_url': None, 'twitter_url': 'twitter.com/ironsourcegroup', 'profiles': ['linkedin.com/company/ironsource', 'linkedin.com/company/2657359', 'twitter.com/ironsourcegroup', 'crunchbase.com/organization/ironsource'], 'website': 'ironsrc.com', 'ticker': None, 'type': 'private', 'summary': 'ironsource builds monetization, engagement, analytics and discovery tools for app developers, device manufacturers, mobile carriers and advertisers. our comprehensive solutions help industry leading companies achieve greater business success, enabling them to find, understand, engage with and monetize their target audiences more effectively.over 80k app developers are using our developer solutions, and our enterprise technology is shipping on hundreds of millions of devices worldwide, giving ironsource the ability to reach over 800 million unique users every month, globally. founded in 2010, ironsource is a truly global company, with offices in tel aviv, london, new york, san francisco, beijing, bangalore and seoul. read more at www.ironsrc.com', 'tags': ['integrated business intelligence', 'user acquisition', 'software & app delivery', 'software & app distribution', 'app discovery', 'software & app monetization', 'mobile', 'desktop apps', 'sales and marketing', 'mobile apps'], 'headline': 'We power next-generation advertising', 'alternative_names': ['ironsource (formerly supersonic)', 'iron source', 'supersonic (merged with ironsource)', 'ironsource (mobilecore)', 'ironsource, display digital solutions', 'mobilecore (ironsource)', 'ironsource (previously afterdownload)', 'ironsource innovation labs', 'ironsource ( displaycore )', 'ironsource (merged with supersonic)'], 'affiliated_profiles': ['ironsource-levelup', 'ironsource-aura']}, {'name': 'aqua security', 'size': '201-500', 'employee_count': 419, 'id': 'aquasecteam', 'founded': 2015, 'industry': 'computer software', 'naics': [{'naics_code': '5112', 'sector': 'information', 'sub_sector': 'publishing industries (except internet)', 'industry_group': 'software publishers', 'national_industry': None}], 'sic': [{'sic_code': '7372', 'major_group': 'business services', 'industry_group': 'computer programming, data processing, and other computer related services', 'industry_sector': 'prepackaged software'}], 'location': {'name': 'illinois, united states', 'locality': None, 'region': 'illinois', 'metro': None, 'country': 'united states', 'continent': 'north america', 'street_address': None, 'address_line_2': None, 'postal_code': None, 'geo': None}, 'linkedin_id': '10034420', 'linkedin_url': 'linkedin.com/company/aquasecteam', 'facebook_url': None, 'twitter_url': None, 'profiles': ['linkedin.com/company/aquasecteam', 'linkedin.com/company/10034420', 'crunchbase.com/organization/aquasecurity'], 'website': 'scalock.com', 'ticker': None, 'type': 'private', 'summary': 'aqua security provides scalable security for the complete development-to-deployment lifecycle of containerized applications. we enable companies to use containers for their many benefits without compromising their application and data security. established in 2015, aqua aims to provide organizations with a trusted, fast and scalable security solution.', 'tags': ['vms', 'cloud', 'cyber security', 'docker', 'security', 'kubernetes', 'serverless', 'container security', 'aws lambda', 'containers'], 'headline': 'The largest pure-play cloud native security company.', 'alternative_names': ['aqua', 'scalock'], 'affiliated_profiles': []}, {'name': 'msd animal health intelligence technology labs', 'size': '201-500', 'employee_count': 167, 'id': 'msdanimalhealthintelligencetechlabs', 'founded': 1948, 'industry': 'computer software', 'naics': [{'naics_code': '3254', 'sector': 'manufacturing', 'sub_sector': 'chemical manufacturing', 'industry_group': 'pharmaceutical and medicine manufacturing', 'national_industry': None}], 'sic': [{'sic_code': '2834', 'major_group': 'chemicals and allied products', 'industry_group': 'drugs', 'industry_sector': 'pharmaceutical preparations'}], 'location': {'name': 'illinois, united states', 'locality': None, 'region': 'illinois', 'metro': None, 'country': 'united states', 'continent': 'north america', 'street_address': None, 'address_line_2': None, 'postal_code': None, 'geo': None}, 'linkedin_id': '11796346', 'linkedin_url': 'linkedin.com/company/msdanimalhealthintelligencetechlabs', 'facebook_url': None, 'twitter_url': None, 'profiles': ['linkedin.com/company/msdanimalhealthintelligencetechlabs', 'linkedin.com/company/11796346'], 'website': 'msd-animal-health.com', 'ticker': None, 'type': 'private', 'summary': "msd animal health intelligence technology labs (formerly known as antelliq innovation center) is where we transform vision into reality. it's where ideas become technologies, and cutting-edge technologies become solutions for animal care and management. \n\nmsd animal health intelligence technology labs supports farmers by providing real-time actionable information to help them manage their herds. it provides pet owners with smart devices and data that give them a better understanding of their pets’ activity and health needs, enriching relationships. it helps conservationists safeguard natural environments and wildlife.\nleveraging decades of r&d experience across many markets, technologies and species, along with development environments and qa procedures, we're always inventing new ways to look after the health and well-being of animals. our decades of experience keep us ahead of curve by leveraging advanced technologies solutions from enhancing the precious bond between people and thei", 'tags': ['application design', 'livestock intelilgence', 'pet activity & behaviour', 'aquaculture', 'embedded systems', 'algorithm', 'data analytics', 'aws', 'milking intelligence', 'iot'], 'headline': 'Connecting Animals and People.', 'alternative_names': ['antelliq innovation center', 'animal healt', 'intervet egypt for animal health sae'], 'affiliated_profiles': []}, {'name': 'armis', 'size': '201-500', 'employee_count': 4, 'id': 'armisserbia', 'founded': None, 'industry': 'textiles', 'naics': None, 'sic': None, 'location': None, 'linkedin_id': '27013785', 'linkedin_url': 'linkedin.com/company/armisserbia', 'facebook_url': None, 'twitter_url': None, 'profiles': ['linkedin.com/company/armisserbia', 'linkedin.com/company/27013785'], 'website': 'armis.rs', 'ticker': None, 'type': 'private', 'summary': 'armis specializes in the production of high-quality modern formalwear, casualwear, military and police uniforms, as well as protective workwear. \n\nour production ranges from oem, odm to obm. we also offer the possibility of 2d and 3d visual solutions of the specific garment, collection or detail, as well as techpack creation.\n\nwe also provide full personalization: embroidery, badges, screen printing, digital printing and sublimination.', 'tags': ['design', 'uniforms', 'htz', 'sewing', 'military and police equipment', 'garment production', 'protective wear', 'police uniforms', 'workwear'], 'headline': 'Formalwear\nMilitary and police uniforms\nProtective workwear\nCorporate uniforms', 'alternative_names': ['armis - luss protect d.o.o.'], 'affiliated_profiles': []}, {'name': 'optimove', 'size': '201-500', 'employee_count': 338, 'id': 'optimove', 'founded': 2009, 'industry': 'computer software', 'naics': [{'naics_code': '5112', 'sector': 'information', 'sub_sector': 'publishing industries (except internet)', 'industry_group': 'software publishers', 'national_industry': None}], 'sic': [{'sic_code': '7372', 'major_group': 'business services', 'industry_group': 'computer programming, data processing, and other computer related services', 'industry_sector': 'prepackaged software'}], 'location': {'name': 'new york, new york, united states', 'locality': 'new york', 'region': 'new york', 'metro': 'new york, new york', 'country': 'united states', 'continent': 'north america', 'street_address': '217 west 21st street', 'address_line_2': None, 'postal_code': '10011', 'geo': '40.71,-74.00'}, 'linkedin_id': '227901', 'linkedin_url': 'linkedin.com/company/optimove', 'facebook_url': 'facebook.com/optimove', 'twitter_url': 'twitter.com/optimove', 'profiles': ['linkedin.com/company/optimove', 'linkedin.com/company/227901', 'facebook.com/optimove', 'twitter.com/optimove', 'crunchbase.com/organization/optimove'], 'website': 'optimove.com', 'ticker': None, 'type': 'private', 'summary': 'optimove is the leading retention automation software, used by over 150 customer-centric brands to drive their entire customer marketing operation.\n\n optimove combines the art of marketing with the science of data to enable marketers to deliver highly-effective personalized customer marketing campaigns through email, mobile, the web and other channels. optimove’s unique customer modeling, predictive micro-segmentation and campaign automation technologies help marketers maximize customer spend, engagement, retention and lifetime value. optimove is used by leading customer-centric brands of all sizes in a variety of industries, including zynga, outbrain, ceaser’s entertainment, nelly, 888 and many others.\n\n with offices in tel aviv, new york and london, the company has doubled staff and revenues over the past year.\n\n more information is available at www.optimove.com.', 'tags': ['personalization', 'customer engagement', 'predictive analytics', 'multi-channel marketing', 'micro-segmentation', 'customer retention automation', 'behavior modeling', 'conversion optimization', 'lifecycle marketing', 'customer churn prediction & prevention'], 'headline': 'CRM Marketing. Orchestrated.', 'alternative_names': ['mobius solutions ltd.', 'mobius solutions', 'optimo', 'optimove (mobius solutions ltd.)', 'mobius solutions, ltd.'], 'affiliated_profiles': ['optibot--ai-marketing-optimization']}], 'scroll_token': '201$1.0$321972', 'total': 85}
    # api_enrichment.add_info_to_db(response)
    main_menu()
