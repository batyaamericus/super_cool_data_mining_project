import NewArgParser as nap
import argparse


def setting_comp_search_params():
    company_search = nap.NewArgParser(exit_on_error=False)
    exit_parser = nap.NewArgParser(exit_on_error=False)
    company_search.add_argument('search_parameter', type=str, choices=['n', 'l'], help="'n' to search by company name, "
                                                                                       "'l' to search by company location. You"
                                                                                       " can only perform one of the two searches.")
    company_search.add_argument('input', type=str, nargs='+',
                                help="Follow you previous command with names or locations "
                                     " to search. Please write '_' instead of any whitespaces present"
                                     " in the company names or locations.")
    company_search.add_argument('-b', '--back', action='store_true', help='back to main menu')
    exit_parser.add_argument('-b', '--back', action='store_true', help='back to main menu')
    param_dic = {'name': None, 'location': None}

    while True:

        try:
            options = input("Enter search parameters:")
            args, unknown = company_search.parse_known_args(options.split())

            # returning False to return to main menu
            if args.back:
                return False

            if args.search_parameter == 'n':
                param_dic['name'] = args.input
            else:
                param_dic['location'] = args.input

            return param_dic

        except argparse.ArgumentError as error:
            exit_bool, unknown = exit_parser.parse_known_args(options.split())
            if exit_bool.back:
                return False
            print(error, "Try again or type '-b' to go back.")
            continue
        except SystemExit:
            continue


def setting_display_params():
    display_flags = nap.NewArgParser(exit_on_error=False)
    display_flags.add_argument('-d', '--d', action='store_true', help='get description')
    display_flags.add_argument('-l', '--l', action='store_true', help='get location')
    display_flags.add_argument('-w', '--w', action='store_true', help='get website')
    display_flags.add_argument('-p', '--p', action='store_true', help='get positions')
    display_flags.add_argument('-a', '--all', action='store_true', help='get everything')
    display_flags.add_argument('-x', '--cancel', action='store_true', help='cancel search')
    flags_dic = {}

    while True:
        try:
            params_input = input("Specify what information about the companies you would like to see:")
            params, unknown = display_flags.parse_known_args(params_input.split())

        except argparse.ArgumentError as error:
            print(error, "Try again or type '-x' to cancel the search")
            continue
        except SystemExit:
            continue

        if params.cancel:
            return False

        flags_dic['description'] = params.d
        flags_dic['location'] = params.l
        flags_dic['website'] = params.w
        flags_dic['positions'] = params.p
        flags_dic['all'] = params.all
        if all([v == False for v in flags_dic.values()]):
            print("You did not enter any display parameters. By default the program will display company website.")
            flags_dic['website'] = True

        return flags_dic


def setting_posit_display_params():
    posit_display_flags = nap.NewArgParser(exit_on_error=False)
    posit_display_flags.add_argument('-d', '--d', action='store_true', help='department')
    posit_display_flags.add_argument('-l', '--l', action='store_true', help='location')
    posit_display_flags.add_argument('-t', '--t', action='store_true', help='employment type')
    posit_display_flags.add_argument('-e', '--e', action='store_true', help='experience level')
    posit_display_flags.add_argument('-s', '--s', action='store_true', help='description')
    posit_display_flags.add_argument('-a', '--all', action='store_true', help='get everything')
    posit_display_flags.add_argument('-x', '--cancel', action='store_true', help='cancel search')
    flags_dic = {}

    while True:
        try:
            params_input = input("Specify what information about the positions you would like to see:")
            params, unknown = posit_display_flags.parse_known_args(params_input.split())

        except argparse.ArgumentError as error:
            print(error, "Try again or type '-x' to cancel the search")
            continue
        except SystemExit:
            continue

        if params.cancel:
            return False

        flags_dic['department'] = params.d
        flags_dic['location'] = params.l
        flags_dic['employment type'] = params.t
        flags_dic['experience level'] = params.e
        flags_dic['description'] = params.s
        flags_dic['all'] = params.all
        if all([v == False for v in flags_dic.values()]):
            print(
                "You did not enter any display parameters. By default the program will only display position title and company name.")

        return flags_dic


def setting_posit_search_params():
    print("You have selected to search for positions!")
    positions_search_parser = nap.NewArgParser(exit_on_error=False)
    positions_search_parser.add_argument('-n', '--n', type=str, nargs='+', help='by name')
    positions_search_parser.add_argument('-d', '--d', type=str, nargs='+', help='by department')
    positions_search_parser.add_argument('-l', '--l', type=str, nargs='+', help='by location')
    positions_search_parser.add_argument('-t', '--t', type=str, nargs='+', help='by employment type')
    positions_search_parser.add_argument('-e', '--e', type=str, nargs='+', help='by experience level')
    positions_search_parser.add_argument('-c', '--c', type=str, nargs='+', help='by company')
    positions_search_parser.add_argument('-b', '--back', action='store_true', help='back to main menu')
    param_dic = {}

    while True:

        try:
            options = input("Enter search parameters:")
            args, unknown = positions_search_parser.parse_known_args(options.split())

            # returning False to return to main menu
            if args.back:
                return False

            param_dic['name'] = args.n
            param_dic['location'] = args.l
            param_dic['department'] = args.d
            param_dic['emp_type'] = args.t
            param_dic['exp_level'] = args.e
            param_dic['company'] = args.c

            if all([v is None for v in param_dic.values()]):
                print("You did not enter any search parameters. Try again or type '-b' to go back.")
                continue

            return param_dic

        except argparse.ArgumentError as error:
            print(error, "Try again or type '-b' to go back.")
            continue
        except SystemExit:
            continue
