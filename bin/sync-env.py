#!/usr/bin/env python3

from pathlib import Path
import re


def extract_keys(path: Path) -> list[str]:
    pattern = re.compile(r"^\s*export\s+([A-Za-z_][A-Za-z0-9_]*)\s*=")
    keys: list[str] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            key = match.group(1)
            if key not in keys:
                keys.append(key)

    return keys


def main() -> None:
    env_path = Path.home() / ".env"
    example_path = Path(__file__).resolve().parent / ".." / "env" / ".env.example"
    example_path = example_path.resolve()

    if not env_path.exists():
        print("No ~/.env file found; nothing to synchronize.")
        return

    if not example_path.exists():
        print(f"Missing template file: {example_path}")
        return

    env_keys = set(extract_keys(env_path))
    example_keys = extract_keys(example_path)
    missing = [key for key in example_keys if key not in env_keys]

    if not missing:
        print("No new environment keys to add.")
        return

    current = env_path.read_text(encoding="utf-8")
    with env_path.open("a", encoding="utf-8") as fp:
        if current and not current.endswith("\n"):
            fp.write("\n")
        fp.write("# Added by make install (synchronized from env/.env.example)\n")
        for key in missing:
            fp.write(f"export {key}=\n")

    print("Appended environment keys: " + ", ".join(missing))


if __name__ == "__main__":
    main()
