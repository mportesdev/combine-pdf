def string_to_range_tuples(user_string, last_page):
    """Returns a list of tuples if string is valid, empty list otherwise. From
    the user's point of view, pages are numbered from 1. In PdfFileMerger
    interface, pages are numbered from 0.

    Example input:    '1-5, 12, 48, 96-98'
           output:    [(0, 5), (11, 12), (47, 48), (95, 98)]

    The argument 'last_page' (equal to the PDF file's number of pages) is being
    passed to check if a page number is in valid range.
    """
    result = []
    valid = True

    if user_string:
        user_string = user_string.strip(" ,")
        for part in user_string.split(","):
            try:
                # valid single page number?
                from_page = int(part.strip())
            except ValueError:
                # not a valid single number
                try:
                    # valid range of page numbers?
                    from_page = int(part.split("-")[0].strip())
                    to_page = int(part.split("-", 1)[1].strip())
                except ValueError:
                    # not a valid range of numbers
                    valid = False
                    break
                else:
                    # valid range of numbers
                    if 1 <= from_page <= last_page and \
                       1 <= to_page <= last_page:
                        # we have a range of valid page numbers -> make a
                        # tuple to be directly used by merger.append()
                        # (pages numbered from 0)
                        range_tuple = (from_page - 1, to_page)
                    else:
                        # range of numbers out of page range
                        valid = False
                        break
            else:
                # valid single number
                if 1 <= from_page <= last_page:
                    # we have a valid page number -> make a tuple to be
                    # directly used by merger.append()
                    # (pages numbered from 0)
                    range_tuple = (from_page - 1, from_page)
                else:
                    # number out of page range
                    valid = False
                    break
            result.append(range_tuple)

    if result and valid:
        return result, valid
    else:
        return [], False
