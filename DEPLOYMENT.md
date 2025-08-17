# Streamlit Cloud Deployment Guide

This guide walks you through deploying the Multi-Agent Workout System on Streamlit Cloud.

## 📋 Pre-Deployment Checklist

### ✅ **Required Files** (Already Prepared)
- [x] `app.py` - Main Streamlit application
- [x] `requirements.txt` - Python dependencies
- [x] `.streamlit/config.toml` - Streamlit configuration
- [x] `backend/` - Backend modules
- [x] `.gitignore` - Protects secrets from being committed

### ✅ **Configuration System** (Hybrid Ready)
- [x] Local development: Uses `config.toml`  
- [x] Cloud deployment: Uses Streamlit secrets
- [x] Automatic detection of environment

## 🚀 Deployment Steps

### 1. **Prepare Your Repository**

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Verify .gitignore:**
   - Ensure `config.toml` is NOT in the repository
   - Ensure `.streamlit/secrets.toml` is NOT in the repository
   - The `.streamlit/config.toml` SHOULD be in the repository

### 2. **Deploy on Streamlit Cloud**

1. **Visit Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

2. **Create New App:**
   - Click "New app"
   - Select your repository
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: Choose a name (e.g., `your-username-workout-agent`)

3. **Click "Deploy"**

### 3. **Configure Secrets**

⚠️ **CRITICAL: The app will fail until you set up secrets!**

1. **Go to App Settings:**
   - In your deployed app, click the hamburger menu (≡)
   - Select "Settings"
   - Click "Secrets"

2. **Add Your Secrets:**
   Copy and paste this template, replacing with your actual values:

   ```toml
   [api]
   groq_api_key = "gsk_your_actual_groq_api_key_here"
   groq_model = "llama3-8b-8192"

   [agents]
   max_tokens = 32768
   temperature = 0.7
   max_iterations = 10

   [system]
   debug = false
   log_level = "INFO"
   ```

3. **Save Secrets:**
   - Click "Save"
   - The app will automatically restart

### 4. **Verify Deployment**

1. **Check App Status:**
   - App should show "Running" status
   - No import errors in logs

2. **Test Functionality:**
   - Try a simple query like "Create a basic workout plan"
   - Verify all three agents respond
   - Check that tools are working

## 🔧 Configuration Details

### **Local Development** 
```bash
# Uses config.toml (not committed)
streamlit run app.py
```

### **Cloud Deployment**
```bash
# Uses Streamlit secrets (configured in dashboard)
# Automatically detected by config system
```

### **Environment Detection**
The system automatically detects if it's running on:
- ✅ Streamlit Cloud → Uses `st.secrets`
- ✅ Local development → Uses `config.toml`

## 🛠️ Troubleshooting

### **Common Issues:**

#### **1. Import Errors**
```
ModuleNotFoundError: No module named 'xyz'
```
**Solution:** Check `requirements.txt` includes all dependencies

#### **2. API Key Errors**
```
ValueError: Groq API key not configured
```
**Solution:** Add secrets in Streamlit Cloud dashboard

#### **3. Configuration Errors**
```
Error loading Streamlit secrets
```
**Solution:** Check secrets format matches the template exactly

#### **4. Memory Issues**
```
Your app has gone over the resource limits
```
**Solution:** 
- Reduce `max_tokens` in secrets
- Check for memory leaks in agent memory

### **Debugging Tips:**

1. **Check Logs:**
   - In Streamlit Cloud, view the app logs
   - Look for configuration detection messages

2. **Test Secrets:**
   ```python
   # Add this to app.py temporarily to debug
   import streamlit as st
   st.write("API Key present:", bool(st.secrets.get("api", {}).get("groq_api_key")))
   ```

3. **Enable Debug Mode:**
   ```toml
   [system]
   debug = true
   log_level = "DEBUG"
   ```

## 📊 Resource Usage

### **Streamlit Cloud Limits:**
- **Memory:** ~1GB
- **CPU:** Shared
- **Bandwidth:** Generous but not unlimited
- **Storage:** Temporary only

### **Optimization Tips:**
- Keep `max_tokens = 32768` for full responses
- Use `temperature = 0.7` for balanced creativity
- Monitor agent memory usage
- Clear conversation history periodically

## 🔄 Updates and Maintenance

### **Updating the App:**
1. Push changes to your GitHub repository
2. Streamlit Cloud automatically redeploys
3. Secrets persist across deployments

### **Managing Secrets:**
- Update secrets anytime via the dashboard
- Changes take effect immediately
- No need to redeploy for secret changes

### **Monitoring:**
- Check app logs regularly
- Monitor API usage in Groq dashboard  
- Watch for performance issues

## 🆘 Support Resources

- **Streamlit Cloud Docs:** [docs.streamlit.io/streamlit-cloud](https://docs.streamlit.io/streamlit-cloud)
- **Community Forum:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **Groq API Docs:** [console.groq.com](https://console.groq.com)

## 🎯 Quick Deploy Checklist

- [ ] Repository pushed to GitHub
- [ ] App deployed on Streamlit Cloud
- [ ] Secrets configured with valid API key
- [ ] App running without errors
- [ ] Test query successful
- [ ] All agents responding

**Your Multi-Agent Workout System is now live! 🎉**
