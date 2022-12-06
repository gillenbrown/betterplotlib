from pathlib import Path
from git import Repo

# initialize the repo
home_dir = Path(__file__).parent.parent
repo = Repo(home_dir)
changed_files = [item.a_path for item in repo.index.diff(None)]

if "pyproject.toml" not in changed_files:
    # go through the file and modify the version number. I'll default to a minor
    # update
    pyproject_in_loc = home_dir / "pyproject.toml"
    pyproject_out_loc = home_dir / "pyproject.toml.temp"
    pyproject_in_file = open(pyproject_in_loc, "r")
    pyproject_out_file = open(pyproject_out_loc, "w")
    # go through the file, and modify the version number. Keep all other lines the same
    for line in pyproject_in_file:
        if line.startswith("version = "):
            version = line.split("=")[-1].strip()
            major, minor, patch = version.split(".")
            line = f"version = {major}.{int(minor) + 1}.{patch}\n"
        pyproject_out_file.write(line)

    pyproject_in_file.close()
    pyproject_out_file.close()

    # then move the temp file to replace the original file
    pyproject_out_loc.rename(pyproject_in_loc)
