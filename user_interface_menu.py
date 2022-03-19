import sys
import argparse
import NewArgParser as nap
import interface_functions as uif
from db_search_functions import DBsearch
import scraping_and_populating_db


def main_menu():
    scraping_and_populating_db.scraping()

    db_connector = DBsearch()
    sys.stdout.write('Welcome to the Comeet Scraper!\n')
    args = None
    while True:
        command = input("Enter command :")
        parser = nap.NewArgParser(exit_on_error=False)

        subparsers = parser.add_subparsers(help="Type of search: 'c' for company search and 'p' for positions search")
        # subparsers.required = True
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
                continue

            args.func(db_connector)

        except argparse.ArgumentError as error:
            print(error)
            continue
        except SystemExit:
            if args is not None:
                if args.quit:
                    quit()
            continue


def search_company_menu(db_connector):
    print("You have selected to search for a company!")

    comp_params = uif.setting_comp_search_params()  # expecting: comp_params={'name'=[-names-], 'location'=[-location-]}

    # if return value is False, the user selected -b
    if not comp_params:
        return

    display_params = uif.setting_display_params()  # expecting: display_params= {'description','info', 'website', 'positions', 'all'}

    # if return value is False, the user selected -x
    if not display_params:
        return

    posit_disp_params = None
    if display_params['positions'] or display_params['all']:
        posit_disp_params = uif.setting_posit_display_params()
        # if return value is False, the user selected -x
        if not posit_disp_params:
            return

    company_names_list = comp_params['name']  # can be none
    company_locations_list = comp_params['location']  # can be none

    print("this is what you've got for company:")
    print(company_names_list, company_locations_list)
    print(display_params)

    db_connector.comp_search_db(comp_params, display_params, posit_disp_params)


def search_positions_menu(db_connector):
    posit_params = uif.setting_posit_search_params()  # expecting: dictionary of lists posit_params{'name', 'location'...}

    # if return value is False, the user selected -b
    if not posit_params:
        return

    posit_display_params = uif.setting_posit_display_params()
    # if return value is False, the user selected -x
    if not posit_display_params:
        return

    print("this is what you've got for positions:")
    print(posit_params, posit_display_params)

    db_connector.posit_search_db(posit_params, posit_display_params)


if __name__ == '__main__':
    main_menu()
