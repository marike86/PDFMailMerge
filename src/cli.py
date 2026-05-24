"""
Command-Line Interface for PDF Mail Merge Tool
Provides user-friendly CLI for batch PDF generation.
"""

import os
import sys
import argparse
import time
from typing import Dict, List, Optional

from .data_loader import load_data, validate_data, data_to_dict_list
from .pdf_processor import (
    fill_form_pdf, 
    replace_text, 
    get_form_field_names, 
    detect_text_placeholders,
    validate_template
)
from .template_engine import validate_template_fields
from .utils import (
    ensure_dir, 
    clean_dir, 
    parse_naming_pattern,
    print_progress,
    format_duration,
    create_zip_archive,
    get_timestamp
)


class MailMergeCLI:
    """Command-line interface for PDF mail merge operations"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with all options"""
        parser = argparse.ArgumentParser(
            description='PDF Mail Merge Tool - Batch generate personalized PDFs',
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
            """
        )
        
        parser.add_argument(
            '--template', '-t',
            required=True,
            help='Path to PDF template file'
        )
        
        parser.add_argument(
            '--data', '-d',
            required=True,
            help='Path to data source (CSV, Excel, JSON)'
        )
        
        parser.add_argument(
            '--output', '-o',
            default='./output',
            help='Output directory (default: ./output)'
        )
        
        parser.add_argument(
            '--mode', '-m',
            choices=['form', 'text', 'auto'],
            default='auto',
            help='Processing mode: form (PDF forms), text ({{placeholder}} replacement), or auto-detect'
        )
        
        parser.add_argument(
            '--name', '-n',
            default='document_{row}',
            help='Output naming pattern (default: document_{row})'
        )
        
        parser.add_argument(
            '--zip',
            action='store_true',
            help='Create ZIP archive of output files'
        )
        
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean output directory before processing'
        )
        
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output'
        )
        
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate template and data without generating PDFs'
        )
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run CLI with provided arguments.
        
        Args:
            args: Command-line arguments (default: sys.argv[1:])
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            parsed_args = self.parser.parse_args(args)
            
            if parsed_args.verbose:
                print("PDF Mail Merge Tool")
                print("=" * 50)
            
            start_time = time.time()
            
            if parsed_args.clean:
                print(f"Cleaning output directory: {parsed_args.output}")
                clean_dir(parsed_args.output)
            
            ensure_dir(parsed_args.output)
            
            if parsed_args.verbose:
                print(f"Loading data from: {parsed_args.data}")
            
            df = load_data(parsed_args.data)
            
            if parsed_args.verbose:
                print(f"Loaded {len(df)} records")
            
            mode = parsed_args.mode
            
            if mode == 'auto':
                form_fields = get_form_field_names(parsed_args.template)
                text_placeholders = detect_text_placeholders(parsed_args.template)
                
                if form_fields:
                    mode = 'form'
                elif text_placeholders:
                    mode = 'text'
                else:
                    print("Error: No form fields or text placeholders detected in PDF")
                    return 1
                
                if parsed_args.verbose:
                    print(f"Auto-detected mode: {mode}")
            
            if parsed_args.verbose:
                print(f"Processing mode: {mode}")
            
            if mode == 'form':
                template_fields = get_form_field_names(parsed_args.template)
            else:
                template_fields = detect_text_placeholders(parsed_args.template)
            
            if parsed_args.verbose:
                print(f"Template fields: {', '.join(template_fields)}")
                print(f"Data fields: {', '.join(df.columns.tolist())}")
            
            validation = validate_template_fields(template_fields, df.columns.tolist())
            
            if not validation['valid']:
                print("\nField mapping issues:")
                if validation['unmatched_template']:
                    print(f"  Template fields without data: {', '.join(validation['unmatched_template'])}")
                if validation['unmatched_data']:
                    print(f"  Data fields not in template: {', '.join(validation['unmatched_data'])}")
                
                response = input("\nContinue anyway? (y/n): ").lower().strip()
                if response != 'y':
                    print("Cancelled by user")
                    return 1
            
            if parsed_args.validate_only:
                print("\nValidation passed!")
                return 0
            
            print(f"\nGenerating PDFs...")
            print(f"Output directory: {parsed_args.output}")
            
            records = data_to_dict_list(df)
            success_count = 0
            error_count = 0
            
            for idx, record in enumerate(records, 1):
                try:
                    row_output_dir = parsed_args.output
                    ensure_dir(row_output_dir)
                    
                    filename = parse_naming_pattern(
                        parsed_args.name,
                        {**record, 'row': idx},
                        default=f'document_{idx}'
                    ) + '.pdf'
                    
                    output_path = os.path.join(row_output_dir, filename)
                    
                    if mode == 'form':
                        fill_form_pdf(parsed_args.template, record, output_path)
                    else:
                        replacements = {key: str(record.get(key, '')) for key in template_fields}
                        replace_text(parsed_args.template, replacements, output_path)
                    
                    success_count += 1
                    
                    if parsed_args.verbose or (idx % 10 == 0):
                        print_progress(idx, len(records), prefix='Progress:')
                        
                except Exception as e:
                    error_count += 1
                    if parsed_args.verbose:
                        print(f"\nError processing record {idx}: {e}")
            
            print(f"\n{'='*50}")
            print(f"Completed!")
            print(f"  Total records: {len(records)}")
            print(f"  Successful: {success_count}")
            print(f"  Errors: {error_count}")
            print(f"  Time: {format_duration(time.time() - start_time)}")
            print(f"  Output: {os.path.abspath(parsed_args.output)}")
            
            if parsed_args.zip and success_count > 0:
                zip_name = f"pdf_mail_merge_{get_timestamp()}.zip"
                zip_path = os.path.join(os.path.dirname(parsed_args.output), zip_name)
                
                print(f"\nCreating ZIP archive...")
                if create_zip_archive(parsed_args.output, zip_path):
                    print(f"  Archive: {zip_path}")
                else:
                    print("  Warning: Failed to create ZIP archive")
            
            return 0 if error_count == 0 else 1
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            return 130
        except Exception as e:
            print(f"\nError: {e}")
            if parsed_args.verbose if 'parsed_args' in locals() else False:
                import traceback
                traceback.print_exc()
            return 1


def main():
    """Entry point for CLI"""
    cli = MailMergeCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()