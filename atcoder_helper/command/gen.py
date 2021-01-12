import argparse
import json
import logging
import re
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import requests
from argcomplete.completers import DirectoriesCompleter, FilesCompleter
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

atcoder_base_url = "https://atcoder.jp"


@dataclass(frozen=True)
class Task:
    contest_id: str
    task_id: str
    task_url: str
    alphabet: str


def get_page(url):
    try:
        response = requests.get(url)
    except ConnectionError as e:
        logger.error(e)
        sys.exit(1)
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    if response.status_code != requests.codes.ok:
        logger.error(f"statuc_code was {response.status_code}, please confirm url: {url}")
        sys.exit(1)

    return BeautifulSoup(response.text, "html.parser")


def get_tasks(contest_id: str, alphabets: list[str] = None) -> list[Task]:
    page = get_page(f"{atcoder_base_url}/contests/{contest_id}/tasks")

    tbody = page.find("tbody")
    if not tbody:
        logger.error("no tbody found")
        sys.exit(1)

    tasks = []
    for tr in tbody.find_all("tr"):
        tds = tr.find_all("td")
        alphabet = tds[0].text
        task_path = tds[1].find("a").attrs["href"]

        task_url = f"{atcoder_base_url}{task_path}"
        task_id = Path(task_url).name

        if not re.match(r"[A-Z]", alphabet):
            continue

        if alphabets:
            if alphabet not in alphabets:
                continue

        tasks.append(Task(contest_id, task_id, task_url, alphabet))

    if not tasks:
        logger.error("no task found")
        sys.exit(1)

    return tasks


def generate_task_dir(task: Task, task_dir: Path) -> None:
    logger.debug(f"make directory: {task_dir}")
    task_dir.mkdir(parents=True, exist_ok=True)

    with open(task_dir / "task.json", "w") as f:
        json.dump(asdict(task), f)


def copy_template_file(task_dir: Path, template_file: Path) -> None:
    target = task_dir / ("main" + template_file.suffix)

    if not target.exists():
        shutil.copy(template_file, target)
    else:
        logger.info(f"template file already exists and was not copied: {target}")


def get_recent_contest_ids(prefix: str, parsed_args, **kwargs):
    get_params_dict = {}
    if prefix.startswith("abc"):
        get_params_dict["ratedType"] = 1
    if prefix.startswith("arc"):
        get_params_dict["ratedType"] = 2
    if prefix.startswith("agc"):
        get_params_dict["ratedType"] = 3

    get_params = "&".join([f"{k}={v}" for k, v in get_params_dict.items()])

    page = get_page(f"{atcoder_base_url}/contests/archive?{get_params}")
    tbody = page.find("tbody")

    contest_ids = []
    for tr in tbody.find_all("tr"):
        tds = tr.find_all("td")
        contest_id = tds[1].find("a").attrs["href"].replace("/contests/", "")
        contest_ids.append(contest_id)

    return contest_ids


def get_alphabets_in_contest(prefix: str, parsed_args, **kwargs):
    tasks = get_tasks(parsed_args.contest_id)
    all_alphabets = [task.alphabet for task in tasks]
    return [alphabet for alphabet in all_alphabets if alphabet not in parsed_args.alphabets]


def add_arguments(subparser):
    subparser.add_argument("contest_id", type=str).completer = get_recent_contest_ids
    subparser.add_argument("alphabets", type=str, nargs="*", default=[]).completer = get_alphabets_in_contest
    subparser.add_argument("--contests-dir", type=Path, default=Path("./contests")).completer = DirectoriesCompleter()
    subparser.add_argument("--template-file", type=Path).completer = FilesCompleter()


def main(args):
    tasks = get_tasks(args.contest_id, args.alphabets)
    if not tasks:
        logger.error(f"do nothing because no task was found")
        sys.exit(1)

    for task in tasks:
        task_dir = args.contests_dir / task.contest_id / task.alphabet

        generate_task_dir(task, task_dir)

        if args.template_file and args.template_file.exists():
            copy_template_file(task_dir, args.template_file)
