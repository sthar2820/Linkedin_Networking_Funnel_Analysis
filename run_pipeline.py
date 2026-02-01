"""
LinkedIn Networking Analytics - Master ETL Pipeline

This script orchestrates the complete data cleaning and standardization process
for all LinkedIn export datasets.

Usage:
    python run_pipeline.py [--skip-missing]

Options:
    --skip-missing    Continue processing even if some files are missing
"""

import sys
import os
import argparse
from datetime import datetime
import json

# Add src to path
sys.path.append(os.path.dirname(__file__))

from src.utils import logger
from src.clean_invitations import clean_invitations
from src.clean_connections import clean_connections
from src.clean_messages import clean_messages
from src.clean_guide_messages import clean_guide_messages
from src.clean_learning_messages import clean_learning_messages
from src.clean_comments import clean_comments


class ETLPipeline:
    """Master ETL Pipeline for LinkedIn Networking Data"""
    
    def __init__(self, skip_missing=False):
        self.skip_missing = skip_missing
        self.results = {
            'start_time': datetime.now().isoformat(),
            'datasets_processed': [],
            'datasets_failed': [],
            'datasets_skipped': []
        }
        
        # Define all datasets to process
        self.datasets = [
            {
                'name': 'Invitations',
                'input_file': 'Invitations.csv',
                'output_file': 'invitations_cleaned.csv',
                'function': clean_invitations,
                'description': 'Top of funnel - connection requests'
            },
            {
                'name': 'Connections',
                'input_file': 'Connections.csv',
                'output_file': 'connections_cleaned.csv',
                'function': clean_connections,
                'description': 'Network growth - accepted connections'
            },
            {
                'name': 'Messages',
                'input_file': 'messages.csv',
                'output_file': 'messages_cleaned.csv',
                'function': clean_messages,
                'description': 'Mid funnel - direct messaging conversations'
            },
            {
                'name': 'Guide Messages',
                'input_file': 'guide_messages.csv',
                'output_file': 'guide_messages_cleaned.csv',
                'function': clean_guide_messages,
                'description': 'Platform engagement - guided messages'
            },
            {
                'name': 'Learning Messages',
                'input_file': 'learning_coach_messages.csv',
                'output_file': 'learning_messages_cleaned.csv',
                'function': clean_learning_messages,
                'description': 'Learning engagement - coach interactions'
            },
            {
                'name': 'Comments',
                'input_file': 'Comments.csv',
                'output_file': 'comments_cleaned.csv',
                'function': clean_comments,
                'description': 'Engagement layer - public comments'
            }
        ]
    
    def check_raw_data_exists(self):
        """Check which raw data files exist"""
        
        logger.info("=" * 80)
        logger.info("CHECKING RAW DATA FILES")
        logger.info("=" * 80)
        
        raw_dir = 'data/raw'
        existing_files = []
        missing_files = []
        
        for dataset in self.datasets:
            filepath = os.path.join(raw_dir, dataset['input_file'])
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath) / 1024  # KB
                logger.info(f"✓ Found: {dataset['input_file']} ({file_size:.2f} KB)")
                existing_files.append(dataset['name'])
            else:
                logger.warning(f"✗ Missing: {dataset['input_file']}")
                missing_files.append(dataset['name'])
        
        logger.info(f"\nSummary: {len(existing_files)} found, {len(missing_files)} missing")
        
        if missing_files and not self.skip_missing:
            logger.error("\nMissing files detected. Options:")
            logger.error("1. Add missing files to data/raw/")
            logger.error("2. Run with --skip-missing flag to process available files only")
            return False
        
        return True
    
    def run_dataset_cleaning(self, dataset):
        """Run cleaning for a single dataset"""
        
        logger.info("=" * 80)
        logger.info(f"PROCESSING: {dataset['name']}")
        logger.info(f"Description: {dataset['description']}")
        logger.info("=" * 80)
        
        try:
            # Check if file exists
            raw_path = os.path.join('data/raw', dataset['input_file'])
            if not os.path.exists(raw_path):
                if self.skip_missing:
                    logger.warning(f"Skipping {dataset['name']} - file not found")
                    self.results['datasets_skipped'].append(dataset['name'])
                    return None
                else:
                    raise FileNotFoundError(f"File not found: {raw_path}")
            
            # Run cleaning function
            df_cleaned = dataset['function'](
                input_file=dataset['input_file'],
                output_file=dataset['output_file']
            )
            
            # Record success
            self.results['datasets_processed'].append({
                'name': dataset['name'],
                'rows': len(df_cleaned),
                'columns': len(df_cleaned.columns),
                'output_file': dataset['output_file']
            })
            
            logger.info(f"✓ Successfully processed {dataset['name']}")
            return df_cleaned
            
        except Exception as e:
            logger.error(f"✗ Failed to process {dataset['name']}: {str(e)}")
            self.results['datasets_failed'].append({
                'name': dataset['name'],
                'error': str(e)
            })
            
            if not self.skip_missing:
                raise
            
            return None
    
    def run(self):
        """Execute the complete ETL pipeline"""
        
        logger.info("\n")
        logger.info("=" * 80)
        logger.info("LINKEDIN NETWORKING ANALYTICS - ETL PIPELINE")
        logger.info("=" * 80)
        logger.info(f"Start Time: {self.results['start_time']}")
        logger.info(f"Skip Missing: {self.skip_missing}")
        logger.info("")
        
        # Check raw data files
        if not self.check_raw_data_exists():
            logger.error("Pipeline aborted - missing required files")
            return False
        
        logger.info("\n")
        
        # Process each dataset
        for dataset in self.datasets:
            self.run_dataset_cleaning(dataset)
            logger.info("\n")
        
        # Record completion
        self.results['end_time'] = datetime.now().isoformat()
        
        # Generate summary
        self.print_summary()
        
        # Save pipeline report
        self.save_report()
        
        return True
    
    def print_summary(self):
        """Print pipeline execution summary"""
        
        logger.info("=" * 80)
        logger.info("PIPELINE EXECUTION SUMMARY")
        logger.info("=" * 80)
        
        logger.info(f"\n✓ Datasets Processed: {len(self.results['datasets_processed'])}")
        for dataset in self.results['datasets_processed']:
            logger.info(f"  - {dataset['name']}: {dataset['rows']} rows, {dataset['columns']} columns")
        
        if self.results['datasets_skipped']:
            logger.info(f"\n⊘ Datasets Skipped: {len(self.results['datasets_skipped'])}")
            for name in self.results['datasets_skipped']:
                logger.info(f"  - {name}")
        
        if self.results['datasets_failed']:
            logger.info(f"\n✗ Datasets Failed: {len(self.results['datasets_failed'])}")
            for dataset in self.results['datasets_failed']:
                logger.info(f"  - {dataset['name']}: {dataset['error']}")
        
        logger.info(f"\nStart Time: {self.results['start_time']}")
        logger.info(f"End Time: {self.results['end_time']}")
        
        logger.info("\nCleaned data saved to: data/cleaned/")
        logger.info("=" * 80)
    
    def save_report(self):
        """Save pipeline execution report"""
        
        os.makedirs('outputs', exist_ok=True)
        
        report_path = os.path.join('outputs', 'pipeline_report.json')
        
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        logger.info(f"\nPipeline report saved to: {report_path}")


def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description='LinkedIn Networking Analytics - ETL Pipeline'
    )
    parser.add_argument(
        '--skip-missing',
        action='store_true',
        help='Continue processing even if some files are missing'
    )
    
    args = parser.parse_args()
    
    # Create and run pipeline
    pipeline = ETLPipeline(skip_missing=args.skip_missing)
    success = pipeline.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
