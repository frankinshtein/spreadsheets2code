from __future__ import print_function
import pickle
import os.path
import codecs
import collections

from xml.sax.saxutils import quoteattr
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def fix_field(name):
    res = ""
    for s in name:
        if s == "#":
            res += "-"
        else:
            if s.isdigit() or s.isalpha() or s == "_":
                res += s
    return res


class matrix:
    def __init__(self):
        self.cells = None
        self.transposed = False
        self.height = 0
        self.width = 0

    def init(self, cells):
        self.cells = cells
        self.transposed = False
        self.height = len(cells)
        self.width = len(cells[0])

        for line in self.cells:
            if self.width < len(line):
                self.width = len(line)

    def init_sub(self, mat, pos, size):

        self.width = size[0]
        self.height = size[1]

        self.transposed = False

        self.cells = [None] * self.height
        for y in range(self.height):
            line = []
            self.cells[y] = line

            for x in range(self.width):
                line.append(mat.get(x + pos[0], y + pos[1]))


    def transpose(self):
        self.transposed = not self.transposed
        self.height, self.width = self.width, self.height

    def get(self, x, y):
        if self.transposed:
            x, y = y, x

        try:
            return str(self.cells[y][x])
        except IndexError:
            return ""

    def set(self, x, y, value):
        if self.transposed:
            x, y = y, x

        self.cells[y][x] = str(value)


def export_table(args, mat, sheet_name):

    print("  {}".format(sheet_name))

    preset = args.preset

    if mat.get(1, 0) == 'id' and mat.get(0, 1) != 'id':
        mat.transpose()

    result = ""

    if mat.get(0, 1) == "id":
        mat.set(0, 0, "id")

    sheet_name = fix_field(sheet_name)
    y = 1
    result += '\t<' + sheet_name

    y = 2

    for x in range(mat.width):

        field = mat.get(x, 0)

        if not field:
            continue

        if "#" in field:
            continue

        if field.startswith("*"):
            continue

        tp = mat.get(x, 1)
        result += " {}={}".format(fix_field(field), quoteattr(tp))


    result += '>\n'

    while y < mat.height:

        if mat.get(0, y).startswith("*"):
            y += 1
            continue

        result += '\t\t<item'

        for x in range(mat.width):

            field = mat.get(x, 0)

            if not field:
                continue

            if "@" in field:
                continue

            if field.startswith("*"):
                continue


            value = mat.get(x, y)

            """

            if preset:
                for n, nm in enumerate(fields):
                    if field + "@" + preset == nm:
                        v = page[y][n]
                        if v:
                            value = v
                        if v == "@":
                            value = ""
                        break
                        
            """

            result += " {}={}".format(fix_field(field), quoteattr(value))

        result += '/>\n'

        y += 1

    result += '\t</' + sheet_name + '>\n'

    return result


def export_sheet(args, sheet_name, values):
    """
    :type sheet_name: basestring
    """

    print("")

    if sheet_name.startswith("*"):
        print("skipped {}".format(sheet_name))
        return None



    print("tab '{}'".format(sheet_name))

    response = values.get(spreadsheetId=args.src, range=sheet_name, valueRenderOption='UNFORMATTED_VALUE').execute()


    page = response.get('values', [])

    if len(page) < 1:
        return  None

    result = ""


    mat = matrix()
    mat.init(page)


    for y in range(mat.height):
        for x in range(mat.width):
            
            cell = mat.get(x, y)

            if cell.startswith("@"):
                #it is sub table

                name = cell[1:]

                if name == "loot_box_currency_drop":
                    q = 0

                sub_width = mat.width - x
                for mx in range(x + 1, mat.width):
                    cell = mat.get(mx, y + 1)
                    if not cell:
                        sub_width = mx - x
                        break

                sub_height = mat.height - y - 1
                for my in range(y + 1, mat.height):
                    empty_line = True
                    for mx in range(x, x + sub_width):
                        cell = mat.get(mx, my)
                        if cell:
                            empty_line = False
                            break

                    if empty_line:
                        sub_height = my - y - 1
                        break


                sub = matrix()
                sub.init_sub(mat, (x, y + 1), (sub_width, sub_height))


                result += export_table(args, sub, name)


    if result:
        return result


    return export_table(args, mat, sheet_name)


def main(args):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(args.credentials, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token, protocol=2)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    sheet_metadata = sheet.get(spreadsheetId=args.src).execute()

    sheets = sheet_metadata.get('sheets', '')
    values = sheet.values()


    result = ""
    result += "<data preset=" + '"' + args.preset + '"' + ">\n"

    for sheet_item in sheets:
        name = sheet_item.get("properties", {}).get("title", "Sheet1")
        rs = export_sheet(args, name, values)
        if rs:
            result += rs

    result += "</data>"


    folder = os.path.split(args.dest)[0]

    try:
        os.makedirs(folder)
    except OSError:
        pass

    header = codecs.open(args.dest, "w", "utf-8-sig")
    header.write(result)
    header.close()
    print("file saved: " + args.dest)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="export google doc to xml.  https://developers.google.com/sheets/api/quickstart/python")
    parser.add_argument("-s", "--src", help="source spreadsheet ID", required=True)
    parser.add_argument("-d", "--dest", help="destination file")
    parser.add_argument("-c", "--credentials", help="credentials json file", default="credentials.json")

    parser.add_argument("--preset", help="compile time preset", required=False, default="")

    args = parser.parse_args()

    if not args.dest:
        args.dest = args.src + ".xml"

    try:
        os.remove(args.dest)
    except:
        pass

    main(args)