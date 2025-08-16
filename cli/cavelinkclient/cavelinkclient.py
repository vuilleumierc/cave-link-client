from argparse import ArgumentParser
from io import StringIO

import pandas
import requests


class CaveLinkClient:

    # Group and values for Môtiers (station 106)
    values: dict[int, dict[int, str]] = {
        0: {
            0: "Batterie Motiers [V]",
            1: "Empfangspegel GSM [dBm]",
            2: "Repetitionen GSM-Block [x]",
        },
        1: {
            0: "Temperatur Wasser [C]",
            1: "Druck des Wassers [Bar]",
            2: "Temperatur im GSM-Modul [C]",
            3: "Luftdruck im GSM-Modul [Bar]",
            101: "Wasserstand [m]",
        },
    }

    def __init__(self, base_url: str = "https://www.cavelink.com/cl/da.php"):
        self.base_url: str = base_url
        self.data: pandas.DataFrame | None = None

    def response_to_dataframe(
        self, response: requests.Response, column_name: str
    ) -> pandas.DataFrame:
        stream: StringIO = StringIO(response.text.replace("<br>", "\n"))
        return pandas.read_csv(
            stream,
            header=2,
            names=["Zeit", column_name],
            parse_dates=["Zeit"],
            index_col="Zeit",
            dayfirst=True,
        )

    def get_value(
        self, station: int, group: int, value: int, length: int = 10
    ) -> pandas.DataFrame:
        params = {"s": station, "g": group, "w": value, "l": length}
        print(
            f"Downloading data for station {station}, group {group}, value {value}, length {length}"
        )
        column_name = self.values[group][value]
        response: requests.Response = requests.get(self.base_url, params=params)
        return self.response_to_dataframe(response, column_name)

    def get_values(
        self, station: int = 106, group: int = 1, length: int = 10
    ) -> pandas.DataFrame:
        values = list(self.values[group].keys())
        dfs = [self.get_value(station, group, value, length) for value in values]
        return pandas.concat(dfs, axis=1)


def parse_args():
    parser = ArgumentParser(
        description="""
        Download data from the Cave-Link API and write it to a CSV file.
        """
    )
    parser.add_argument(
        "--station",
        "-s",
        type=int,
        help="Station ID (default: 106)",
        default=106,
    )
    parser.add_argument(
        "--group",
        "-g",
        type=int,
        default=1,
        help="Group ID (default: 1)",
    )
    parser.add_argument(
        "--length",
        "-l",
        type=int,
        default=10,
        help="Number of rows to download (default: 10)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="/tmp/cavelink.csv",
        help="Output file (default: /tmp/cavelink.csv)",
    )
    return parser.parse_args()


def run():
    args = parse_args()
    cavelink = CaveLinkClient()
    data = cavelink.get_values(args.station, args.group, args.length)
    data.to_csv(args.output)
