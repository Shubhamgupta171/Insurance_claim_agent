# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
cd /Users/shubhamgupta/Desktop/Insurance_claim_Agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Demo (No API Key Required)

```bash
python demo.py
```

This will process 5 sample claims and show all routing scenarios.

### 3. Run Unit Tests

```bash
pytest tests/ -v
```

Expected: 17 tests passing ✅

### 4. Process Sample PDFs

First, generate the PDF samples:

```bash
python scripts/convert_to_pdf.py
```

Then process them (without AI):

```bash
python -m src.main --input-dir tests/sample_fnol/ --no-ai
```

### 5. Use with AI (Optional)

If you have an OpenAI API key:

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here

# Process with AI
python -m src.main --input tests/sample_fnol/fast_track_claim.pdf
```

## 📊 Expected Results

### Demo Output

```
ROUTING DISTRIBUTION
Fast-track:         1 claim(s)  ✅
Investigation Flag: 1 claim(s)  🚨
Manual review:      2 claim(s)  ⚠️
Specialist Queue:   1 claim(s)  🏥
```

### Test Results

```
======================== 17 passed in 0.94s =========================
```

## 📁 Output Location

All processed claims are saved as JSON in:
```
data/output/
```

## 🎯 Next Steps

1. Review the [README.md](file:///Users/shubhamgupta/Desktop/Insurance_claim_Agent/README.md) for detailed documentation
2. Check [walkthrough.md](file:///Users/shubhamgupta/.gemini/antigravity/brain/92db3a8d-f374-47d8-b03a-36984fb1b833/walkthrough.md) for implementation details
3. Explore sample FNOL documents in `tests/sample_fnol/`
4. Customize routing rules in `src/config.py`

## 🆘 Troubleshooting

**Issue**: `python: command not found`  
**Solution**: Use `python3` instead

**Issue**: AI extraction not working  
**Solution**: Ensure API key is set in `.env` file, or use `--no-ai` flag

**Issue**: Tests failing  
**Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

## 📞 Support

For questions or issues, refer to:
- [README.md](file:///Users/shubhamgupta/Desktop/Insurance_claim_Agent/README.md) - Full documentation
- [walkthrough.md](file:///Users/shubhamgupta/.gemini/antigravity/brain/92db3a8d-f374-47d8-b03a-36984fb1b833/walkthrough.md) - Implementation walkthrough
- Sample code in `tests/` directory
