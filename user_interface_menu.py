import sys
import argparse
import NewArgParser as nap
import interface_functions as uif
from db_search_functions import DBsearch
import scraping_and_populating_db


def main_menu():
    """This function displays the main menu prompting the user to selected company or positions search"""

    db_connector = DBsearch()
    sys.stdout.write('Welcome to the Comeet Scraper!\n')
    args = None
    while True:
        print("Please choose if you want to search for a company or for open job positions. Type'c' for the former and 'p' for the latter.\n"
              "Type '-h' for help and '-q' to quit the program.")
        command = input("Enter command :")
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
    """This function presents a sub-menu for users who have selected to search for companies.
        It prompts the users to search the search and display parameters for the output.
        Finally it calls comp_search_db to preform the search."""

    print("You have selected to search for a company!")

    comp_params = uif.setting_comp_search_params()

    # if return value is False, the user selected -b
    if not comp_params:
        return

    display_params = uif.setting_display_params()

    # if return value is False, the user selected -x
    if not display_params:
        return

    posit_disp_params = None
    if display_params['positions'] or display_params['all']:
        posit_disp_params = uif.setting_posit_display_params()
        # if return value is False, the user selected -x
        if not posit_disp_params:
            return


    db_connector.comp_search_db(comp_params, display_params, posit_disp_params)


def search_positions_menu(db_connector):
    """This function presents a sub-menu for users who have selected to search for open positions.
            It prompts the users to search the search and display parameters for the output.
            Finally it calls posit_search_db to preform the search."""
    posit_params = uif.setting_posit_search_params()

    # if return value is False, the user selected -b
    if not posit_params:
        return

    posit_display_params = uif.setting_posit_display_params()
    # if return value is False, the user selected -x
    if not posit_display_params:
        return

    db_connector.posit_search_db(posit_params, posit_display_params)


if __name__ == '__main__':
    main_menu()
