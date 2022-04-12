import NewArgParser as nap
import argparse


def setting_comp_search_params():
    """
    This function asks for and parses user input the type of search for company to be performed.

    :return: dictionary of selected parameters
    """
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
            print("Please choose one of the two options:\n"
                  "\t1. Type 'n' followed by company names separates by spaces to search for companies by name:"
                  "\n\t\te.g. 'n comp1 comp2 comp3' (Please use underscore for spaces in company names)\n"
                  "\t2. Type 'l' followed by locations separated by space to search for companies based on their location:\n"
                  "\t\te.g. 'l Loc1 Loc2 Loc3' (Please use underscore for spaces in location names)"
                  "\n Type '-h' for help and '-b' to go back to the previous menu.")

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
    """
        This function asks for and parses user input for display parameters for company search output.

        :return: dictionary of selected parameters
        """
    display_flags = nap.NewArgParser(exit_on_error=False)
    display_flags.add_argument('-d', '--d', action='store_true', help='get description')
    display_flags.add_argument('-l', '--l', action='store_true', help='get location')
    display_flags.add_argument('-w', '--w', action='store_true', help='get website')
    display_flags.add_argument('-p', '--p', action='store_true', help='get positions')
    display_flags.add_argument('-a', '--all', action='store_true', help='get everything')
    display_flags.add_argument('-f', '--f', action='store_true', help='get company profile from People Data Labs')
    display_flags.add_argument('-x', '--cancel', action='store_true', help='cancel search')
    flags_dic = {}

    while True:
        try:
            print("Now you can choose what information you want displayed about the companies that match your search.\n"
                  "Please use the following flags:\n"
                  "\t'-d' to display company description\n"
                  "\t'-l' to display company location\n"
                  "\t'-w' to display company website\n"
                  "\t'-p' to display all open positions in the company\n"
                  "\t'-f' to display company's profile from People Data Labs\n"
                  "\t'-a' to display all of the above\n"
                  "\t'e.g. Typing '-lw' will output companies' location and website (name always by default)\n"
                  "Type '-h' for help and '-x' to cancel the search")
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
        flags_dic['pdl'] = params.f
        flags_dic['all'] = params.all
        if all([v for v in flags_dic.values() if v is False]):
            print("You did not enter any display parameters. By default the program will display company website.")
            flags_dic['website'] = True

        return flags_dic


def setting_posit_display_params():
    """
           This function asks for and parses user input for display parameters for positions search output.

           :return: dictionary of selected parameters
           """
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
            print("Now you can choose what information you want displayed about the positions that match your search.\n"
                  "Please use the following flags:\n"
                  "\t'-d' to display position department\n"
                  "\t'-l' to position location\n"
                  "\t'-t' to display employment type\n"
                  "\t'-e' to display experience level\n"
                  "\t'-s' to display position description\n"
                  "\t'-a' to display all of the above\n"
                  "\t'e.g. Typing '-ds' will output positions' departament and description (name and company always by default)\n"
                  "Type '-h' for help and '-x' to cancel the search")
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
        if all([v for v in flags_dic.values() if v is False]):
            print(
                "You did not enter any display parameters. By default the program will only display position title and company name.")

        return flags_dic


def setting_posit_search_params():
    """
               This function asks for and parses user input for parameters by which to search for open positions..

               :return: dictionary of selected parameters
               """
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
            print("Please use the following flags to specify your search parameters:\n"
                  "Please use underscores instead of spaces in a single input argument)"
                  "\t'-n' to search positions by title (e.g. '-n data_scientist programmer')\n"
                  "\t'-d' to search positions by department (e.g. '-d HR')\n"
                  "\t'-l' to search positions by location (e.g. '-l Israel Tel_Aviv')\n"
                  "\t'-t' to search positions by employment type (e.g. '-t full_time')\n"
                  "\t'-e' to search positions by experience level (e.g. '-e Entry-level')\n"
                  "\t'-c' to search by company name (e.g. '-c Comp1 Comp2')\n"
                  "Type '-h' for help and '-b' to go back to the previous menu")
            options = input('Please type you search parameters:')
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
