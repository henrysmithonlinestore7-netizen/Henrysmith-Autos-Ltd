# Setup Guide - HenrySmith Autos Ltd

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser
- Internet connection

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/henrysmithonlinestore7-netizen/Henrysmith-Autos-Ltd.git
cd Henrysmith-Autos-Ltd
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Application

Edit configuration files:

- `src/config/settings.py` - Application settings
- `src/config/database.py` - Database and bank configurations

### 5. Launch Application

#### Option A: Open HTML file directly

```bash
open src/pages/dashboard.html
```

#### Option B: Use Python HTTP Server

```bash
python -m http.server 8000
```

Then open: `http://localhost:8000/src/pages/dashboard.html`

#### Option C: Use Flask (if installed)

```bash
flask run
```

## Configuration

### Database Configuration

Edit `src/config/database.py` to:
- Add/remove banks
- Configure account types
- Set transaction types

### Application Settings

Edit `src/config/settings.py` to:
- Change theme colors
- Adjust pagination
- Enable/disable features
- Set UI preferences

## Troubleshooting

### Issue: Page shows "Loading original text..."

**Solution**: The JavaScript may not have loaded properly. Try:
1. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
2. Clear browser cache
3. Open in incognito/private mode

### Issue: Styling appears broken

**Solution**:
1. Check browser console for errors (F12)
2. Ensure all files are in correct directories
3. Try a different browser

### Issue: Cannot download files

**Solution**:
1. Check browser download settings
2. Try a different browser
3. Ensure sufficient disk space

## Development

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes
3. Test thoroughly
4. Submit pull request

### Code Standards

- Use meaningful variable names
- Add comments for complex logic
- Follow PEP 8 for Python code
- Use consistent formatting

## Performance Optimization

- Minimize CSS/JavaScript
- Optimize images
- Use caching strategies
- Enable gzip compression

## Security Considerations

- Always validate user input
- Use HTTPS in production
- Implement proper authentication
- Secure sensitive data
- Regular security audits

## Deployment

### Production Deployment

1. Set environment to production
2. Configure secure database
3. Set up SSL certificates
4. Configure web server (nginx/Apache)
5. Set up monitoring and logging
6. Regular backups

### Cloud Deployment

Supported platforms:
- Heroku
- AWS
- Google Cloud
- Azure

## Support

For issues or questions, please open an issue on GitHub or contact support.
