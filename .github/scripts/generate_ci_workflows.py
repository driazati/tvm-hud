#!/usr/bin/env python3

from pathlib import Path

import jinja2
import os
from dataclasses import dataclass
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GITHUB_DIR = REPO_ROOT / ".github"

CRONS = {
    "1 hour": "0 * * * *",
    "1 day at 8 AM": "0 8 * * *",
}


@dataclass
class Branch:
    branch: str
    cron: str = CRONS["1 hour"]
    fetch_size: int = 4
    history_size: int = 100


@dataclass
class PR:
    cron: str = CRONS["1 hour"]
    fetch_size: int = 4
    history_size: int = 100


HUD_JOBS = {
    "apache": {
        "tvm": [
            Branch(branch="main"),
            PR(),
            Branch(branch="v0.5", cron=CRONS["1 day at 8 AM"]),
            Branch(branch="v0.6", cron=CRONS["1 day at 8 AM"]),
            Branch(branch="v0.7", cron=CRONS["1 day at 8 AM"]),
            Branch(branch="v0.8", cron=CRONS["1 day at 8 AM"]),
        ],
    },
    "tlc-pack": {
        "relax": [
            Branch(branch="relax"),
        ]
    },
    "octoml": {
        "relax": [
            Branch(branch="relax"),
        ]
    },
}


class CIWorkflow:
    name: str
    template: str

    def __init__(self, name: str, template: str, **kwargs: Any) -> None:
        self.name = name
        self.template = template
        for key, value in kwargs.items():
            setattr(self, key, value)

    def generate_workflow_file(self, workflow_template: jinja2.Template) -> None:
        output_file_path = GITHUB_DIR / f"workflows/generated-{self.name}.yml"
        with open(output_file_path, "w") as output_file:
            filename = Path(workflow_template.filename).relative_to(REPO_ROOT)
            output_file.write("# @generated DO NOT EDIT MANUALLY\n")
            output_file.write(f"# Generated from {filename}\n")
            output_file.write(workflow_template.render(self.__dict__))
            output_file.write("\n")
        print("Wrote", output_file_path.relative_to(REPO_ROOT))


WORKFLOWS = []

for user_name, repos in HUD_JOBS.items():
    for repo_name, branches in repos.items():
        for branch in branches:
            data = {
                "template": "update_github_status.yml.j2",
                "repo": repo_name,
                "user": user_name,
                "cron": branch.cron,
                "fetch_size": branch.fetch_size,
                "history_size": branch.history_size,
                "is_pr": isinstance(branch, PR),
            }
            if isinstance(branch, PR):
                data["workflow_name"] = f"{user_name}/{repo_name}/PRs"
                data["name"] = "update-github-stats-PRs"
            else:
                data["branch"] = branch.branch
                data[
                    "workflow_name"
                ] = f"{user_name}/{repo_name}/{branch.branch.replace('/', '_')}"
                data[
                    "name"
                ] = f"update-github-status-{user_name}-{repo_name}-{branch.branch.replace('/', '_')}"

            WORKFLOWS.append(CIWorkflow(**data))


if __name__ == "__main__":
    jinja_env = jinja2.Environment(
        variable_start_string="!{{",
        loader=jinja2.FileSystemLoader(str(GITHUB_DIR / "templates")),
        undefined=jinja2.StrictUndefined,
    )

    # Delete the existing generated files first, this should align with .gitattributes file description.
    existing_workflows = GITHUB_DIR.glob("workflows/generated-*")
    for w in existing_workflows:
        try:
            os.remove(w)
        except Exception as e:
            print(f"Error occurred when deleting file {w}: {e}")

    for workflow in WORKFLOWS:
        template = jinja_env.get_template(workflow.template)
        workflow.generate_workflow_file(workflow_template=template)
