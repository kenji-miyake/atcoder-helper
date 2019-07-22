import argparse
import json
import logging
import re
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass(frozen=True)
class Task:
    contest_id: str
    task_id: str
    task_url: str
    alphabet: str


def get_tasks(contest_id: str) -> Optional[List[Task]]:
    base_url = "https://atcoder.jp"
    tasks_url = base_url + f"/contests/{contest_id}/tasks"

    try:
        response = requests.get(tasks_url)
    except ConnectionError as e:
        logger.error(e)
        return None
    except Exception as e:
        logger.error(e)
        return None

    if response.status_code != requests.codes.ok:
        logger.error(f"statuc_code was {response.status_code}")
        logger.info(f"please confirm url: {tasks_url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    tbody = soup.find("tbody")

    if not tbody:
        logger.error("no tbody found")
        return None

    tasks = []
    for tr in tbody.find_all("tr"):
        tds = tr.find_all("td")

        alphabet = tds[0].text
        task_url = base_url + tds[1].find("a").attrs["href"]
        task_id = Path(task_url).name

        if not re.match(r"[A-Z]", alphabet):
            continue

        tasks.append(Task(contest_id, task_id, task_url, alphabet))

    if not tasks:
        logger.error("no task found")
        return None

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


def main(args: List[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("contest_id")
    parser.add_argument("--contests-dir", type=Path, default=Path("./contests"))
    parser.add_argument("--template-file", type=Path)
    ns = parser.parse_args(args)

    tasks = get_tasks(ns.contest_id)
    if not tasks:
        logger.error(f"do nothing because no task was found")
        sys.exit(1)

    for task in tasks:
        task_dir = ns.contests_dir / task.contest_id / task.alphabet

        generate_task_dir(task, task_dir)

        if ns.template_file and ns.template_file.exists():
            copy_template_file(task_dir, ns.template_file)


if __name__ == "__main__":
    main(sys.argv[1:])
