# OpenAI API Setup Guide

## ✅ System Configured for OpenAI

The Insurance Claims Processing Agent is now configured to use **OpenAI GPT-4o-mini** for AI-powered extraction.

---

## 🔑 How to Add Your OpenAI API Key

### Step 1: Get Your API Key

1. Go to https://platform.openai.com/
2. Sign in or create an account
3. Navigate to **API Keys** section
4. Click **"Create new secret key"**
5. Copy your API key (starts with `sk-...`)

### Step 2: Add Key to .env File

Open the `.env` file in your project:

```bash
nano .env
```

Replace `your_openai_api_key_here` with your actual key:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-your-actual-key-here

# Routing Configuration
FAST_TRACK_THRESHOLD=25000

# Application Settings
LOG_LEVEL=INFO
```

Save and close the file.

---

## 🚀 Test the System

### Test with AI Extraction

```bash
# Process a single claim with OpenAI
python -m src.main --input tests/sample_fnol/fast_track_claim.pdf
```

Expected output:
```
Step 1: Extracting data from PDF...
✓ Extraction complete

Step 2: Validating extracted fields...
✓ All mandatory fields present

Step 3: Routing claim...
✓ Route determined: RouteType.FAST_TRACK
```

### Test Without AI (Regex Only)

```bash
# Process without AI (no API key needed)
python -m src.main --input tests/sample_fnol/fast_track_claim.pdf --no-ai
```

### Run Demo (No API Key Needed)

```bash
# Demo uses mock data, no API calls
python demo.py
```

---

## 📊 What Changed

### Files Modified

1. ✅ **requirements.txt** - Uses `openai>=1.0.0`
2. ✅ **src/config.py** - Reads `OPENAI_API_KEY`
3. ✅ **src/extractor.py** - Uses GPT-4o-mini model
4. ✅ **.env.example** - Template for OpenAI key
5. ✅ **README.md** - Updated documentation
6. ✅ **QUICKSTART.md** - Updated setup guide

### AI Model Details

- **Model**: `gpt-4o-mini`
- **Provider**: OpenAI
- **Use Case**: Structured data extraction from ACORD forms
- **Fallback**: Regex-based extraction if API unavailable

---

## ✅ Verification

All tests pass:
```
======================== 17 passed in 0.16s =========================
```

Demo works perfectly:
```
ROUTING DISTRIBUTION
Fast-track:         1 claim(s)  ✅
Investigation Flag: 1 claim(s)  🚨
Manual review:      2 claim(s)  ⚠️
Specialist Queue:   1 claim(s)  🏥
```

---

## 💰 OpenAI Pricing

**GPT-4o-mini** is very affordable:
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens

Processing a typical FNOL document costs less than $0.01 per claim.

---

## 🔧 Troubleshooting

### Issue: "OpenAI API key not set"
**Solution**: Make sure you created `.env` file (not just `.env.example`) and added your key

### Issue: API authentication error
**Solution**: Verify your API key is correct and has credits available

### Issue: Rate limit errors
**Solution**: OpenAI has rate limits. Add delays between requests or upgrade your plan

---

## 📝 Summary

✅ **Status**: Configured for OpenAI GPT-4o-mini  
✅ **Tests**: All 17 tests passing  
✅ **Demo**: Working perfectly  
✅ **Documentation**: Fully updated  
✅ **Ready**: Add your API key and start processing claims!

---

## 🎯 Next Steps

1. Add your OpenAI API key to `.env`
2. Test with: `python -m src.main --input tests/sample_fnol/fast_track_claim.pdf`
3. Process your own FNOL documents
4. Enjoy accurate AI-powered claim extraction! 🎉
