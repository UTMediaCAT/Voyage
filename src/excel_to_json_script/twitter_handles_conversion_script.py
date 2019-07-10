# Filename: twitter_handles_conversion_script.py
# Author: Raiyan Rahman
# Date: June 26th, 2019
# Description: This is a conversion script that converts an excel file to a
# JSON file containing the names, position, twitter handle in the first,
# second, and third column respectively. The file may also contain an optional
# authenticated column as its fourth column.

import json
from openpyxl import load_workbook


def convert_to_json(filename: str) -> None:
    """
    Create a JSON file containing the converted data from the given excel
    file.
    The headers of the columns are stored as follows:
    Name, Position, Twitter Handle, (Optional Column), (Optional Notes Column)
    :param filename: The name of the excel file to be converted.
    :return: None
    REQ: The filename must point to a valid .xlsx file with the required data.
    """
    # Dictionary containing the headers.
    headers = {
        1: 'Name',
        2: 'Position',
        3: 'Twitter Handle',
        4: 'Authenticated',
        5: 'Notes'
    }
    # Open the excel file.
    wb = load_workbook(filename)
    # Create a dictionary and store the data for each sheet in it.
    excel_data = get_excel_data(wb, headers)
    # Create the JSON and save it.
    dump_data = json.dumps(excel_data)
    outfile = open('twitter_handles.json', 'a')
    outfile.write(dump_data)
    outfile.close()
    return


def get_excel_data(wb, headers: dict) -> dict:
    """
    Return the parsed excel data from the given workbook with respect to the
    given dictionary of headers.
    :param wb: The excel file's workbook.
    :param headers: The dictionary of headers.
    :return: The dictionary containing the parsed excel sheets data.
    """
    # Create the dictionary to hold all the excel data.
    parsed_data = {}
    # Get the sheet names.
    sheet_names = wb.sheetnames
    # Loop through the sheets and get sheet data to parsed data.
    for sheet in sheet_names:
        parsed_data[sheet] = get_sheet_data(wb[sheet], headers)
    # Return the data.
    return parsed_data


def get_sheet_data(sheet, headers: dict) -> dict:
    """
    Return the parsed data for a single excel sheet with respect to the given
    dictionary of headers.
    :param sheet: The worksheet.
    :param headers: The dictionary of headers.
    :return: The dictionary containing the parsed sheet data.
    """
    sheet_data = []
    max_column = 3
    # Check the first row for column names and the max_column length.
    if sheet['A1'].value == 'Name':
        # Check for optional headers and update headers dictionary.
        for optional_header in range(4, 6):
            # Break out if there are no optional columns.
            if sheet.cell(row=1, column=optional_header).value is None:
                break
            elif sheet.cell(row=1, column=optional_header)\
                    .value is not None and\
                    sheet.cell(row=1, column=optional_header)\
                    .value != headers[optional_header]:
                headers[optional_header] = sheet.\
                    cell(row=1, column=optional_header).value
                max_column = optional_header
            else:
                max_column = optional_header
    # If there weren't headers present, use default ones in the headers dict.
    # Parse the first row to find the number of columns.
    else:
        row_data = {}
        for i in range(1, 6):
            if sheet.cell(row=1, column=i).value is None:
                max_column = i - 1
                break
            else:
                row_data[headers[i]] = sheet.cell(row=1, column=i).value\
                    .strip()
                max_column = i
        # Add the row data to the sheet data.
        sheet_data.append(row_data)
    # Loop through the remaining cells containing data, recording them.
    row_counter = 2
    finished = False
    while not finished:
        # If the next two rows are empty.
        if sheet.cell(row=row_counter, column=1).value is None and\
                sheet.cell(row=row_counter + 1, column=1).value is None:
            finished = True
            pass
        elif sheet.cell(row=row_counter, column=1).value is None:
            row_counter += 1
            pass
        else:
            # Get all the row data.
            row_data = {}
            for i in range(1, max_column + 1):
                if sheet.cell(row=row_counter, column=i).value is not None:
                    # Convert Yes/No to bool.
                    if i is 4:
                        val = sheet.cell(row=row_counter, column=i)\
                            .value.strip()
                        val = val.lower()[0]
                        val = True if val == 'y' else False
                        row_data[headers[i]] = val
                    else:
                        row_data[headers[i]] = sheet\
                            .cell(row=row_counter, column=i).value.strip()
            # Add the row data and increment the row counter.
            sheet_data.append(row_data)
            row_counter += 1
    # Return the data.
    return sheet_data


if __name__ == '__main__':
    file_name = input('Enter filename of Excel File: ')
    convert_to_json(filename=file_name)
