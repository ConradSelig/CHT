from testing_suite import gen_tests


def main():

    '''
    mlist = [[]]
    print(mlist)
    mlist[-1][-1] = 1
    print(mlist)
    '''

    gen_tests.initialize_test()
    gen_tests.add_row_test()
    gen_tests.add_many_rows_test()
    return


if __name__ == '__main__':
    main()
