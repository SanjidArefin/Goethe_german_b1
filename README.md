# B1 Glossar

An offline Windows glossary for the Netzwerk neu B1 vocabulary.

## Development

```powershell
npm install
npm start
```

The app loads its curated vocabulary from `backend/data/glossary.json`; it does
not need a web server or an internet connection.

## Checks

```powershell
npm run check
npm run validate-data
npm test
npm run test:electron
```

## Windows Installer

```powershell
npm run dist
```

The installer is created in `release/` with Start Menu, desktop shortcut, and
uninstall support.
