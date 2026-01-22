# Frontend Setup Instructions

## Quick Start

Open a **NEW terminal window** (keep the backend running) and run:

```bash
cd frontend
npm install
npm run dev
```

Then open your browser to: **http://localhost:5173**

## What You'll See

A welcome page with:
- Link to the API documentation
- Instructions for next steps
- Confirmation that the backend is running

## To Build the Full UI

The frontend structure is ready with:
- API service configured (`src/services/api.js`)
- Component examples in `frontend/README.md`
- Basic placeholder UI

### Follow these steps to add full functionality:

1. **See the component examples** in `frontend/README.md`
2. **Copy the component code** from the README
3. **Create the component files** in `src/components/`
4. **Update App.jsx** with the full application logic

## Current Frontend Files

- ✅ `index.html` - HTML entry point
- ✅ `src/main.jsx` - React entry point  
- ✅ `src/App.jsx` - Main app component (placeholder)
- ✅ `src/App.css` - Styling
- ✅ `src/index.css` - Global styles
- ✅ `src/services/api.js` - API integration
- ✅ `package.json` - Dependencies
- ✅ `vite.config.js` - Vite configuration

## Troubleshooting

### "npm: command not found"
Install Node.js from https://nodejs.org/

### "Port 5173 already in use"
```bash
lsof -ti:5173 | xargs kill
```

### "Cannot find module"
```bash
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

1. Run `npm install` in the frontend directory
2. Run `npm run dev` to start the development server
3. Visit http://localhost:5173 in your browser
4. You'll see a welcome page with a link to the API docs
5. Follow the instructions in `frontend/README.md` to build the full UI

The backend API is already running with 50 questions and 32 quotes ready to use!