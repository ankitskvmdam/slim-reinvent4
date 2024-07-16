import requests
import os
import sys
from tqdm import tqdm

BASE_URL = "https://github.com/MolecularAI/REINVENT4/raw/main/priors"

current_path = os.path.dirname(os.path.join(__file__))
priors_path = os.path.join(current_path, "priors")

available_priors = [
    "libinvent.prior",
    "linkinvent.prior",
    "mol2mol_high_similarity.prior",
    "mol2mol_medium_similarity.prior",
    "mol2mol_mmp.prior",
    "mol2mol_scaffold.prior",
    "mol2mol_scaffold_generic.prior",
    "mol2mol_similarity.prior",
    "pubchem_ecfp4_with_count_with_rank_reinvent4_dict_voc.prior",
    "reinvent.prior",
]


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def parse_arg() -> bool:
    n = len(sys.argv)

    if n < 2:
        print(
            f"{bcolors.FAIL}Please enter the name of the priors to download.{bcolors.ENDC}"
        )
        print("Available priors", available_priors)
        print("\n\nTo install a prior do the following")
        print("\n\tpython download_priors.py reinvent.priors\n\n")
        return False

    if n >= 3:
        print(f"{bcolors.WARNING}Only 1 argument is supported. {bcolors.ENDC}")
        print("\n\nTo install a prior do the following")
        print("\n\tpython download_priors.py reinvent.priors\n\n")
        return False

    prior_name = sys.argv[1]

    if prior_name not in available_priors:
        print(f"{bcolors.FAIL}Prior {prior_name} is not available. {bcolors.ENDC}")
        print("Available priors", available_priors)
        return False

    return prior_name


class DownloadStatus:
    Success = 1
    Failed = 2
    Suspended = 3


def download_prior(name) -> "DownloadStatus":
    filepath = os.path.join(priors_path, name)

    if os.path.exists(filepath):
        return DownloadStatus.Suspended

    res = requests.get(f"{BASE_URL}/{name}", stream=True)

    total_size = int(res.headers.get("content-length", 0))
    block_size = 1024
    print(res)
    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(filepath, "wb") as file:
            for data in res.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

    if total_size != 0 and progress_bar.n != total_size:
        os.unlink(filepath)
        return DownloadStatus.Failed

    return DownloadStatus.Success


if __name__ == "__main__":
    prior_name = parse_arg()
    if prior_name:
        if not os.path.exists(priors_path):
            os.mkdir(priors_path)
        status = download_prior(prior_name)

        if status == DownloadStatus.Success:
            print(
                f"{bcolors.OKGREEN}Prior {prior_name} downloaded successfully.{bcolors.ENDC}"
            )
        elif status == DownloadStatus.Failed:
            print(
                f"{bcolors.FAIL}Failed to download {prior_name}. Please try again after sometime. If the issue persist create an issue at https://github.com/ankitskvmdam/slim-reinvent4.{bcolors.ENDC}"
            )
        elif status == DownloadStatus.Suspended:
            print(
                f"{bcolors.WARNING}{prior_name} already exists, hence not download.{bcolors.ENDC}"
            )
