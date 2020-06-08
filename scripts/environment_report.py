import sys
import pygit2
import platform
import subprocess


env_stub_template = """
<details>

### Machine
- **OS**: {os}

---

### Python
{python_version}
<details>
<summary>Packages</summary>
Package Name | Version
------------ | -------   
{python_packages}

</details>

---

### Facile
- **Branch Name**: {git_branch}
- **Commit Hash**: {git_commit}

---

{target_app_info}

{additional_info}

</details>
"""

def getEnvironmentStub():
    # OS info
    os = platform.platform()

    # Python info
    python_version = sys.version
    packages = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()
    python_packages = "\n".join([f'{p.split("==")[0]} | {p.split("==")[1]}' for p in packages])

    # Repo information
    repo = pygit2.Repository("../")
    git_branch = repo.head.shorthand
    git_commit = repo.revparse_single('HEAD^').hex

    # Target App info
    target_app_name = input("What's the name of your target application [N/A]? ")
    target_app_name = target_app_name if target_app_name.strip() else "N/A"
    if target_app_name != "N/A":
        target_app_version = input("What's the version of your target application [N/A]? ")
        target_app_version = target_app_version if target_app_version.strip() else "N/A"
        target_app_info = f"### Target Application\n" \
                          f"- **Name**: {target_app_name}\n" \
                          f"- **Version**: {target_app_version}\n"
    else:
        target_app_info = ""

    # Additional environment information
    additional_info = input("Is there any additional information you'd like to share about your setup [N/A]? ")
    additional_info = additional_info if additional_info.strip() else "N/A"
    if additional_info != "N/A":
        additional_info = "---\n\n### Additional context\n" \
                          f"{additional_info}"
    else:
        additional_info = ""

    report_md = env_stub_template.format(os=os,
                                         python_version=python_version,
                                         python_packages=python_packages,
                                         git_branch=git_branch,
                                         git_commit=git_commit,
                                         target_app_info=target_app_info,
                                         additional_info=additional_info)

    return report_md

if __name__ == "__main__":
    print(getEnvironmentStub())