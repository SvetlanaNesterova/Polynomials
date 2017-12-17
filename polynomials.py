#!/usr/bin/python3
import argparse
from polynomial import Polynomial


def get_str_from_list(array):
    return " ".join(array)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sim', '--simplify',
                        help='Turn mathematical expression to polynomial,'
                        'if possible, or indicate the error.',
                        nargs='+',
                        type=str)
    parser.add_argument('-e', '--equal',
                        help='Should be used with key "--and_" ("-a"). '
                             'Compare mathematical expressions, which goes '
                             'after this key and key "-a", returns "Equal", '
                             'or "Not equal", or indicate the error.',
                        nargs='+',
                        type=str)
    parser.add_argument('-a', '--and_',
                        help='Should go after "--equal" ("-e") argument. '
                             'This key is for second expression in '
                             'comparison.',
                        nargs='+',
                        type=str)
    return parser.parse_args()


def handle_equality(source_1, source_2):
    if Polynomial(source_1) == Polynomial(source_2):
        print('Equal')
    else:
        print('Not equal')


def handle_console_input():
    args = get_args()
    if args.sim is not None:
        source = get_str_from_list(args.sim)
        print(Polynomial(source))
    if args.equal is not None:
        if args.and_ is None:
            print('error: After "--equal" ("-e") you '
                  'should use key "--and_" ("-a").')
        else:
            source_1 = get_str_from_list(args.equal)
            source_2 = get_str_from_list(args.and_)
            handle_equality(source_1, source_2)
    elif args.and_ is not None:
        print('error: Key "--and_" ("-a") should '
              'be used after key "--equal" ("-e").')


if __name__ == "__main__":
    handle_console_input()
