import pickle
import os
import time
from xml.sax.saxutils import quoteattr
from typing import Any, Dict, List, Tuple, Optional
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

string_type = str


def fix_field(name: str) -> str:
    res = ""
    for s in name:
        if s == "#":
            res += "-"
        elif s == ".":
            res += "."
        else:
            if s.isdigit() or s.isalpha() or s == "_":
                res += s
    return res


class Matrix:
    def __init__(self) -> None:
        self.cells: List[List[str]] = []
        self.transposed: bool = False
        self.height: int = 0
        self.width: int = 0

    def init(self, cells: List[List[str]]) -> None:
        self.cells = cells
        self.transposed = False
        self.height = len(cells)
        self.width = len(cells[0]) if cells else 0

        for line in self.cells:
            if self.width < len(line):
                self.width = len(line)

    def init_sub(self, mat: 'Matrix', pos: Tuple[int, int], size: Tuple[int, int]) -> None:
        self.width, self.height = size
        self.transposed = False
        self.cells = [[mat.get(x + pos[0], y + pos[1]) for x in range(self.width)] for y in range(self.height)]

    def transpose(self) -> None:
        self.transposed = not self.transposed
        self.height, self.width = self.width, self.height

    def get(self, x: int, y: int) -> str:
        if self.transposed:
            x, y = y, x

        try:
            val = self.cells[y][x]
            if isinstance(val, string_type):
                return val
            return str(val)
        except IndexError:
            return ""

    def set(self, x: int, y: int, value: str) -> None:
        if self.transposed:
            x, y = y, x

        self.cells[y][x] = str(value)


ids = ["id", "type"]


class Args:
    def __init__(self, src: str, dest: str, pretty: bool, service_account: Optional[str], client_credentials: Optional[str], rename: List[str], preset: str) -> None:
        self.src = src
        self.dest = dest
        self.pretty = pretty
        self.service_account = service_account
        self.client_credentials = client_credentials
        self.rename = rename
        self.preset = preset


def export_table(args: Args, mat: Matrix, sheet_name: str, tables: Dict[str, str]) -> None:
    print("  {}".format(sheet_name))

    if mat.get(1, 0) in ids and mat.get(0, 1) not in ids:
        mat.set(1, 0, "id")
        mat.transpose()

    result = ""

    if mat.get(0, 1) in ids:
        mat.set(0, 1, "id")
        mat.set(0, 0, mat.get(0, 1))

    sheet_name = fix_field(sheet_name)
    for rename in args.rename:
        src_name, target_name = rename.split(":")
        if sheet_name == src_name:
            sheet_name = target_name
            print("renamed {} to {}".format(sheet_name, target_name))

    y = 1
    result += '\t<' + sheet_name

    y = 2

    fields = {}
    for x in range(mat.width):

        field = mat.get(x, 0)

        if not field:
            continue

        if field.startswith("*"):
            continue

        if "#" in field:
            continue

        tp = mat.get(x, 1)
        field_name = fix_field(field)
        result += " {}={}".format(field_name, quoteattr(tp))

        fields[field_name] = field_name

    result += '>\n'

    while y < mat.height:

        if mat.get(0, y).startswith("*"):
            y += 1
            continue

        result += '\t\t<item'

        if args.pretty:
            result += '\n'

        for x in range(mat.width):

            field = mat.get(x, 0)

            if not field:
                continue

            if "@" in field:
                continue

            if field.startswith("*"):
                continue

            value = mat.get(x, y)

            q = quoteattr(value)
            field_name = fix_field(field)
            if args.pretty:
                z = u"\t\t\t{}={}\n".format(field_name, q)
            else:
                z = u" {}={}".format(field_name, q)

            result += z

        if args.pretty:
            result += '\t\t/>\n'
        else:
            result += '/>\n'

        y += 1

    result += '\t</' + sheet_name + '>\n'
    tables[sheet_name.lower()] = result


def export_sheet(args: Args, sheet_name: str, values: Any, tables: Dict[str, str]) -> None:
    print("")

    if sheet_name.startswith("*"):
        print("skipped {}".format(sheet_name))
        return

    print("tab '{}'".format(sheet_name))

    response = values.get(spreadsheetId=args.src, range=sheet_name, valueRenderOption='UNFORMATTED_VALUE',
                          dateTimeRenderOption='FORMATTED_STRING').execute()

    page = response.get('values', [])

    if len(page) < 1:
        return

    mat = Matrix()
    mat.init(page)

    ret = False

    for y in range(mat.height):
        for x in range(mat.width):

            cell = mat.get(x, y)

            if cell.startswith("@"):
                # it is sub table

                name = cell[1:]

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

                sub = Matrix()
                sub.init_sub(mat, (x, y + 1), (sub_width, sub_height))

                export_table(args, sub, name, tables)
                ret = True

    if ret:
        return

    export_table(args, mat, sheet_name, tables)


def main(args: Args) -> None:
    creds = None

    if args.service_account:
        creds = ServiceAccountCredentials.from_json_keyfile_name(args.service_account, SCOPES)
    else:
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
                flow = InstalledAppFlow.from_client_secrets_file(args.client_credentials, SCOPES)
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token, protocol=2)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    sheet_metadata = sheet.get(spreadsheetId=args.src).execute()

    sheets = sheet_metadata.get('sheets', '')
    values = sheet.values()

    result = """<?xml version="1.0" encoding="UTF-8" ?>"""
    result += "<data timestamp=\"{}\"\n\tpreset=\"{}\" >\n".format(int(time.time()), args.preset)

    tables = {}
    for sheet_item in sheets:
        name = sheet_item.get("properties", {}).get("title", "Sheet1")
        export_sheet(args, name, values, tables)

    sorted_tables = sorted(tables)
    for table in sorted_tables:
        val = tables[table]
        result += val
    result += "</data>"

    folder = os.path.split(args.dest)[0]

    try:
        os.makedirs(folder)
    except OSError:
        pass

    try:
        with open(args.dest, "rb") as old:
            data_old = old.read().decode("utf-8").split("\n", 1)[1]
            data_new = result.split("\n", 1)[1]
            if data_old == data_new:
                print("there are not any changes in document: " + args.dest)
                return
    except Exception:
        pass

    with open(args.dest, "wb") as fh:
        fh.write(result.encode("utf-8"))
    print("file saved: " + args.dest)


def run(params: Optional[List[str]]) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="export google spreadsheet to xml")
    parser.add_argument("-s", "--src", help="source spreadsheet ID", required=True)
    parser.add_argument("-d", "--dest", help="destination file")
    parser.add_argument("--pretty", help="pretty xml render", default=True)
    parser.add_argument("--service_account", help="google service account credentials json file")
    parser.add_argument("--client_credentials", help="client credentials json file")
    parser.add_argument("--rename", help="add table rename", action='append', default=[])
    parser.add_argument("--preset", help="compile time preset", required=False, default="")

    args = parser.parse_args(params)

    if not args.dest:
        args.dest = args.src + ".xml"

    args_obj = Args(
        src=args.src,
        dest=args.dest,
        pretty=args.pretty,
        service_account=args.service_account,
        client_credentials=args.client_credentials,
        rename=args.rename,
        preset=args.preset
    )

    main(args_obj)


if __name__ == "__main__":
    run(None)
