# Quick Troubleshooting Guide

## 🔍 Common Issues & Solutions

### Issue 1: "Unknown at rule @tailwind" warnings in VS Code
**Solution:** 
- Install "Tailwind CSS IntelliSense" extension (bradlc.vscode-tailwindcss)
- Reload VS Code
- Warnings disappear and autocomplete works

**If still showing:**
- Warnings are harmless - they don't affect functionality
- CSS will compile correctly with Vite
- Application works fine in production

---

### Issue 2: Tailwind classes not showing/not working
**Solution:**
1. Run `npm install` to ensure dependencies are installed
2. Check `tailwind.config.js` exists with correct content paths
3. Check `postcss.config.js` exists
4. Restart development server: `npm run dev`
5. Clear cache: `rm -rf node_modules/.vite`

---

### Issue 3: Camera not working in development
**Verify:**
- You're using `http://localhost:5173` (not IP address)
- Browser permissions granted for camera
- `navigator.mediaDevices.getUserMedia` is supported
- Try in Chrome/Firefox first (most compatible)

**For HTTPS (production):**
- Camera requires HTTPS
- Deployment configs handle this automatically

---

### Issue 4: ESLint errors/warnings
**Solution:**
```bash
npm run lint        # See all issues
npm run lint -- --fix  # Auto-fix issues
```

**Common fixes:**
- Unused variables: Prefix with `_` or remove
- Missing dependencies: Add imports
- PropTypes: Add to component props

---

### Issue 5: Build fails
**Solution:**
```bash
# Clear cache
rm -rf node_modules/.vite
rm -rf dist

# Rebuild
npm run build
```

**If still fails:**
- Check for TypeScript errors (if using TS)
- Verify all imports are correct
- Check console output for specific errors

---

### Issue 6: Prettier/ESLint conflicts
**Status:** Already handled! ✅
- ESLint config doesn't conflict with Prettier
- Prettier config respects ESLint rules
- Both work together automatically

---

### Issue 7: Styles not applying
**Check:**
1. Tailwind classes are spelled correctly
2. Tailwind config includes file paths
3. Development server is running
4. CSS file is imported in main.jsx

**Solution:**
```bash
# Restart dev server
npm run dev
```

---

## 🛠️ Setup Verification

### Step 1: Check Node Version
```bash
node --version  # Should be 18+
npm --version   # Should be 9+
```

### Step 2: Verify Installations
```bash
npm list react           # Check React installed
npm list tailwindcss     # Check Tailwind installed
npm list vite            # Check Vite installed
```

### Step 3: Test Build
```bash
npm run build    # Should complete without errors
npm run preview  # Should start without errors
```

### Step 4: Test Dev Server
```bash
npm run dev      # Should start on http://localhost:5173
```

---

## 📦 Dependencies Quick Reference

### Core Dependencies
- **react** ^18.2.0 - UI framework
- **react-dom** ^18.2.0 - React rendering
- **axios** ^1.6.0 - HTTP client
- **zustand** ^4.4.1 - State management
- **react-router-dom** ^6.20.0 - Routing
- **tailwindcss** ^3.3.0 - Styling

### Dev Dependencies
- **vite** ^5.0.0 - Build tool
- **@vitejs/plugin-react** ^4.2.0 - React plugin for Vite
- **eslint** ^8.55.0 - Code linting
- **eslint-plugin-react** ^7.33.2 - React linting rules
- **postcss** ^8.4.32 - CSS processing
- **autoprefixer** ^10.4.16 - CSS prefixes

---

## 🚀 Quick Commands

```bash
# Development
npm run dev              # Start dev server
npm run lint             # Check code quality
npm run build            # Build for production
npm run preview          # Preview production build

# Deployment
npm run deploy:vercel    # Deploy to Vercel
npm run deploy:netlify   # Deploy to Netlify

# Utilities
npm install              # Install dependencies
npm update               # Update dependencies
npm audit                # Check security issues
```

---

## 📱 Mobile Testing

### Local Testing
```bash
# Get your computer's IP
ipconfig getifaddr en0   # macOS
ipconfig                 # Windows (find IPv4)

# Access from mobile on same network
http://<YOUR_IP>:5173
```

**Note:** Camera requires HTTPS on production, but works on `http://localhost` in dev.

---

## 🔐 Security Notes

### In Development
- ✅ Tailwind classes work fine
- ✅ API calls can use HTTP
- ✅ Camera works on localhost

### In Production
- ✅ HTTPS required (for camera)
- ✅ API must use HTTPS
- ✅ Environment variables secure

---

## 📞 Getting Help

### Check These First
1. Look at console for specific error messages
2. Check if development server is running
3. Verify all dependencies installed: `npm install`
4. Clear cache: `rm -rf node_modules/.vite`
5. Restart dev server: `npm run dev`

### If Still Stuck
1. Check `ERROR_FIXES_SUMMARY.md` - Detailed error explanations
2. Check `DEPLOYMENT.md` - Setup and deployment help
3. Check `README_UPDATED.md` - Feature documentation
4. Review component comments in code

---

## ✅ Everything Working?

If you see:
- ✅ Dev server running on `http://localhost:5173`
- ✅ No console errors
- ✅ Styles applied correctly
- ✅ Camera button works
- ✅ Forms functional

**Congratulations!** 🎉 Your setup is complete.

Next steps:
1. Test all features locally
2. Deploy to Vercel/Netlify
3. Monitor for production issues

---

**Last Updated:** February 4, 2026
**Version:** 1.0.0
