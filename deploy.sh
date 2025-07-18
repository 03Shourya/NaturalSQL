#!/bin/bash

# 🚀 NaturalSQL Hugging Face Spaces Deployment Script
# This script helps you deploy your NaturalSQL app to Hugging Face Spaces

echo "🚀 NaturalSQL Deployment Script"
echo "================================"

# Check if target directory is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide the target directory for deployment"
    echo "Usage: ./deploy.sh <target_directory>"
    echo "Example: ./deploy.sh ../huggingface-naturalsql"
    exit 1
fi

TARGET_DIR="$1"

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Error: Target directory '$TARGET_DIR' does not exist"
    echo "Please create the directory first or provide a valid path"
    exit 1
fi

echo "📁 Target directory: $TARGET_DIR"
echo "🔄 Starting deployment..."

# Copy core application files
echo "📋 Copying core files..."
cp app.py "$TARGET_DIR/"
cp requirements.txt "$TARGET_DIR/"
cp README.md "$TARGET_DIR/"
cp .gitattributes "$TARGET_DIR/"

# Copy pipeline components
echo "🔧 Copying pipeline components..."
cp pipeline.py "$TARGET_DIR/"

# Copy directories
echo "📂 Copying directories..."
cp -r parser_agent/ "$TARGET_DIR/"
cp -r intent_classifier/ "$TARGET_DIR/"
cp -r schema_mapper/ "$TARGET_DIR/"
cp -r query_generator/ "$TARGET_DIR/"
cp -r agents/ "$TARGET_DIR/"
cp -r schema/ "$TARGET_DIR/"

# Create __init__.py files if they don't exist
echo "📝 Creating __init__.py files..."
touch "$TARGET_DIR/parser_agent/__init__.py"
touch "$TARGET_DIR/intent_classifier/__init__.py"
touch "$TARGET_DIR/schema_mapper/__init__.py"
touch "$TARGET_DIR/query_generator/__init__.py"
touch "$TARGET_DIR/agents/__init__.py"
touch "$TARGET_DIR/schema/__init__.py"

echo "✅ Deployment files copied successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. cd $TARGET_DIR"
echo "2. git add ."
echo "3. git commit -m 'Initial deployment of NaturalSQL app'"
echo "4. git push origin main"
echo ""
echo "🌐 Your app will be available at:"
echo "https://huggingface.co/spaces/YOUR_USERNAME/naturalsql"
echo ""
echo "Happy deploying! 🚀" 