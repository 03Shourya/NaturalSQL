# 🚀 Hugging Face Spaces Deployment Guide

This guide will help you deploy the NaturalSQL app to Hugging Face Spaces for public access and free hosting.

## 📋 Prerequisites

1. **Hugging Face Account**: Sign up at [huggingface.co](https://huggingface.co)
2. **Git**: Ensure you have Git installed
3. **Project Ready**: All files should be committed to Git

## 🎯 Deployment Steps

### Step 1: Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Choose settings:
   - **Owner**: Your username
   - **Space name**: `naturalsql` (or your preferred name)
   - **Space SDK**: **Gradio**
   - **Space hardware**: **CPU** (free tier)
   - **License**: MIT (or your preferred license)

### Step 2: Clone the Space Repository

```bash
# Clone your new space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/naturalsql
cd naturalsql
```

### Step 3: Copy Project Files

Copy these essential files to your space repository:

```bash
# Core application files
cp app.py ./
cp requirements.txt ./
cp README.md ./
cp .gitattributes ./

# Pipeline components
cp -r pipeline.py ./
cp -r parser_agent/ ./
cp -r intent_classifier/ ./
cp -r schema_mapper/ ./
cp -r query_generator/ ./
cp -r agents/ ./
cp -r schema/ ./
```

### Step 4: Commit and Push

```bash
# Add all files
git add .

# Commit with a descriptive message
git commit -m "Initial deployment of NaturalSQL app"

# Push to Hugging Face Spaces
git push origin main
```

### Step 5: Verify Deployment

1. Go to your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/naturalsql`
2. Wait for the build to complete (usually 2-5 minutes)
3. Test the application with example queries

## 🔧 Configuration Options

### Hardware Options

- **CPU** (Free): Suitable for most use cases
- **GPU** (Paid): Faster processing for complex queries
- **T4** (Paid): Good balance of performance and cost

### Environment Variables

You can add these to your Space settings if needed:

```bash
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
```

## 📁 Required Files Structure

```
naturalsql/
├── app.py                    # Main Gradio application
├── requirements.txt          # Python dependencies
├── README.md                # Space description
├── .gitattributes           # Git file handling
├── pipeline.py              # Main pipeline
├── parser_agent/            # Parser components
├── intent_classifier/       # Intent classification
├── schema_mapper/           # Schema mapping
├── query_generator/         # SQL generation
├── agents/                  # Agent implementations
└── schema/                  # Database schema
```

## 🎉 Benefits of Hugging Face Spaces

- ✅ **Public Access**: Anyone can use your app
- ✅ **Permanent Hosting**: Always online
- ✅ **Free Tier**: No cost for basic usage
- ✅ **GPU Support**: Optional paid GPU access
- ✅ **Easy Updates**: Simple git push to update
- ✅ **Community**: Share with the AI community

## 🔄 Updating Your Space

To update your deployed app:

```bash
# Make changes to your local files
# Then commit and push
git add .
git commit -m "Update: [describe your changes]"
git push origin main
```

## 🐛 Troubleshooting

### Common Issues:

1. **Build Fails**: Check `requirements.txt` for missing dependencies
2. **Import Errors**: Ensure all Python files are copied
3. **App Not Loading**: Check the Space logs for errors
4. **Slow Performance**: Consider upgrading to GPU tier

### Check Logs:

1. Go to your Space on Hugging Face
2. Click on "Settings" tab
3. Check "Build logs" for any errors

## 📞 Support

If you encounter issues:

1. Check the [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces)
2. Review the build logs in your Space settings
3. Ensure all dependencies are properly listed in `requirements.txt`

## 🎯 Next Steps

After successful deployment:

1. **Share your Space**: Post the URL on social media
2. **Add Examples**: Include more example queries
3. **Monitor Usage**: Check Space analytics
4. **Gather Feedback**: Collect user feedback for improvements

---

**Your NaturalSQL app will be live at:**
`https://huggingface.co/spaces/YOUR_USERNAME/naturalsql`

Happy deploying! 🚀 