"""
Command-Line Interface for PDF Mail Merge Tool
Provides user-friendly CLI for batch PDF generation.
"""

import os
import sys
import argparse
import time
from typing import List, Optional

from .utils import (
    print_progress,
    format_duration,
)


class MailMergeCLI:
    """Command-line interface for PDF mail merge operations"""

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with all options"""
        parser = argparse.ArgumentParser(
            description="PDF Mail Merge Tool - Batch generate personalized PDFs",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Form PDF mode
  python -m src.cli --template template.pdf --data contacts.csv --output ./output --mode form

  # Text replacement mode
  python -m src.cli --template template.pdf --data contacts.csv --output ./output --mode text

  # Custom naming pattern
  python -m src.cli --template template.pdf --data contacts.csv --output ./output --name "{id}_{name}"

  # Pack results to ZIP
  python -m src.cli --template template.pdf --data contacts.csv --output ./output --zip
            """,
        )

        parser.add_argument(
            "--template", "-t", required=True, help="Path to PDF template file"
        )

        parser.add_argument(
            "--data", "-d", required=True, help="Path to data source (CSV, Excel, JSON)"
        )

        parser.add_argument(
            "--output",
            "-o",
            default="./output",
            help="Output directory (default: ./output)",
        )

        parser.add_argument(
            "--mode",
            "-m",
            choices=["form", "text", "auto"],
            default="auto",
            help="Processing mode: form (PDF forms), text ({{placeholder}} replacement), or auto-detect",
        )

        parser.add_argument(
            "--name",
            "-n",
            default="document_{row}",
            help="Output naming pattern (default: document_{row})",
        )

        parser.add_argument(
            "--zip", action="store_true", help="Create ZIP archive of output files"
        )

        parser.add_argument(
            "--clean",
            action="store_true",
            help="Clean output directory before processing",
        )

        parser.add_argument(
            "--verbose", "-v", action="store_true", help="Enable verbose output"
        )

        parser.add_argument(
            "--validate-only",
            action="store_true",
            help="Only validate template and data without generating PDFs",
        )

        parser.add_argument("--mapping", help="Comma-separated template_field=data_column pairs")

        return parser

    def run(self, args: Optional[List[str]] = None) -> int:
        """Validate before touching output; run the shared desktop/CLI pipeline."""
        from .merge_service import inspect_inputs, validate_mapping, run_merge
        try:
            options = self.parser.parse_args(args)
            if options.verbose:
                print("PDF Mail Merge Tool")
            started = time.time()
            mapping = {}
            for pair in (options.mapping or "").split(","):
                if pair:
                    if "=" not in pair:
                        raise ValueError("Mapping must use template_field=data_column")
                    key, column = pair.split("=", 1)
                    mapping[key.strip()] = column.strip()
            plan = inspect_inputs(options.template, options.data, options.mode, mapping)
            validate_mapping(plan)
            if options.validate_only:
                print("Validation passed!")
                return 0
            result = run_merge(
                plan, options.output, options.name, options.zip,
                progress=lambda current, total, message: print_progress(current, total, prefix="Progress:"),
                clean=options.clean, data_path=options.data,
            )
            print(f"\nCompleted! Successful: {len(result.files)}; Errors: {len(result.errors)}")
            print(f"Time: {format_duration(time.time() - started)}")
            print(f"Output: {os.path.abspath(options.output)}")
            for error in result.errors:
                print(error)
            if result.archive:
                print(f"Archive: {result.archive}")
            return 1 if result.errors or result.cancelled else 0
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            return 130
        except Exception as exc:
            print(f"Error: {exc}")
            return 1


def main():
    """Entry point for CLI"""
    cli = MailMergeCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
