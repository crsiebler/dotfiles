#!/usr/bin/env python3
"""Audio generation CLI and dependency composition. Requires Python 3.11+."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

from audio_files import ProjectFiles
from audio_service import AudioService
from stable_audio_mlx import StableAudioBackend
from stable_audio_runtime import MODEL, models_root, setup, setup_plan


def build_service(root: Path) -> AudioService:
    return AudioService({MODEL: StableAudioBackend(root)}, ProjectFiles())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    for action in ('status', 'setup', 'generate'):
        command = commands.add_parser(action)
        command.add_argument('--models-root', help='Stable Audio: LOCAL_AUDIO_MODELS_ROOT or ~/Models/local-audio')
        if action != 'status':
            command.add_argument('--dry-run', action='store_true')
        if action == 'setup':
            command.add_argument('--weights-from', help='existing pinned MLX NPZ directory')
            command.add_argument('--accept-model-terms', action='store_true')
        if action == 'generate':
            command.add_argument('--project-root', type=Path, default=Path.cwd())
            command.add_argument('--request', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        root = models_root(args.models_root)
        if args.action == 'status':
            result = StableAudioBackend(root).status()
        elif args.action == 'setup':
            result = (setup_plan(root, args.weights_from) if args.dry_run else
                      setup(root, args.weights_from, args.accept_model_terms))
        else:
            service = build_service(root)
            operation = service.plan if args.dry_run else service.generate
            result = operation(args.project_root, args.request)
        print(json.dumps(result, indent=2))
        return 1 if result.get('ready') is False else 0
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        message = ('audio subprocess failed; inspect its output' if
                   isinstance(error, subprocess.SubprocessError) else str(error))
        print(message, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
