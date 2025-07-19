#!/usr/bin/env python3
"""
Push NaturalSQL app to Hugging Face Spaces
"""

import os
from huggingface_hub import HfApi, create_repo
from pathlib import Path

def push_to_huggingface():
    """Push the NaturalSQL app to Hugging Face Spaces."""
    
    # Initialize API
    api = HfApi()
    
    # Space details
    repo_id = "Shouryacanicus/naturalsql"
    repo_type = "space"
    
    print(f"🚀 Pushing to Hugging Face Space: {repo_id}")
    
    try:
        # Create the space if it doesn't exist
        print("📋 Creating/updating space...")
        create_repo(
            repo_id=repo_id,
            repo_type=repo_type,
            exist_ok=True,
            space_sdk="gradio"
        )
        
        # List of files to upload
        files_to_upload = [
            "app.py",
            "requirements.txt", 
            "README.md",
            ".gitattributes",
            "pipeline.py",
            "parser_agent/parser.py",
            "parser_agent/prompt_template.txt",
            "parser_agent/__init__.py",
            "intent_classifier/classifier.py",
            "intent_classifier/__init__.py",
            "schema_mapper/mapper.py",
            "schema_mapper/schema.py",
            "schema_mapper/__init__.py",
            "query_generator/generator.py",
            "query_generator/__init__.py",
            "agents/__init__.py",
            "schema/__init__.py"
        ]
        
        print("📤 Uploading files...")
        for file_path in files_to_upload:
            if os.path.exists(file_path):
                print(f"  ✅ Uploading: {file_path}")
                api.upload_file(
                    path_or_fileobj=file_path,
                    path_in_repo=file_path,
                    repo_id=repo_id,
                    repo_type=repo_type
                )
            else:
                print(f"  ⚠️  File not found: {file_path}")
        
        print("🎉 Successfully pushed to Hugging Face Spaces!")
        print(f"🌐 Your app is available at: https://huggingface.co/spaces/{repo_id}")
        
    except Exception as e:
        print(f"❌ Error pushing to Hugging Face: {e}")

if __name__ == "__main__":
    push_to_huggingface() 