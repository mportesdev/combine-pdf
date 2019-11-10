def string_to_range_tuples(user_string: str, number_of_pages: int) -> list:
    """Return a list of tuples if user_string is valid, an empty list
    otherwise. From the user's point of view, pages are numbered from 1.
    In PdfFileMerger's interface, pages are numbered from 0.

    Example: string_to_range_tuples('1-5, 12, 48, 96-98', 98)
    return value: [(0, 5), (11, 12), (47, 48), (95, 98)]
    """
    # TODO: rewrite using regexps
    result = []
    valid = True

    if user_string:
        user_string = user_string.strip(' ,')
        for part in user_string.split(','):

            if part.strip() == '':
                continue

            try:
                # valid single number?
                from_page = int(part.strip())
            except ValueError:
                # not a single number

                try:
                    # valid range of numbers?
                    from_page = int(part.split('-')[0].strip())
                    to_page = int(part.split('-', 1)[1].strip())
                except ValueError:
                    # not a valid range of numbers
                    valid = False
                    break
                else:
                    # valid range of numbers

                    if 1 <= from_page <= to_page <= number_of_pages:
                        # valid page range -> make a tuple to be directly
                        # passed to merger.append() (pages numbered from 0)
                        range_tuple = (from_page - 1, to_page)
                    else:
                        # range of numbers out of page range
                        valid = False
                        break
            else:
                # some single number

                if 1 <= from_page <= number_of_pages:
                    # valid page number -> make a tuple to be directly
                    # passed to merger.append() (pages numbered from 0)
                    range_tuple = (from_page - 1, from_page)
                else:
                    # number out of page range
                    valid = False
                    break
            result.append(range_tuple)

    return result if valid else []
