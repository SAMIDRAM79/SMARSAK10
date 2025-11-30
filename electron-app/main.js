const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let mainWindow;
let backendProcess;
let frontendProcess;

// Chemins
const BACKEND_PATH = path.join(__dirname, 'backend');
const PYTHON_PATH = path.join(__dirname, 'python', 'Scripts', 'python.exe');
const MONGO_PATH = 'C:\\Program Files\\MongoDB\\Server\\7.0\\bin\\mongod.exe';
const FRONTEND_BUILD = path.join(__dirname, 'frontend-build');

function checkPort(port, callback) {
  const options = {
    host: 'localhost',
    port: port,
    timeout: 2000
  };

  const req = http.request(options, () => {
    callback(true);
  });

  req.on('error', () => {
    callback(false);
  });

  req.on('timeout', () => {
    req.destroy();
    callback(false);
  });

  req.end();
}

function startMongoDB() {
  console.log('Démarrage MongoDB...');
  
  // Vérifier si MongoDB est déjà en cours d'exécution
  checkPort(27017, (isRunning) => {
    if (isRunning) {
      console.log('MongoDB déjà en cours d\'exécution');
      startBackend();
    } else {
      // Démarrer MongoDB via service Windows
      const mongoProcess = spawn('net', ['start', 'MongoDB'], { shell: true });
      
      mongoProcess.on('error', (error) => {
        console.error('Erreur MongoDB:', error);
        // Continuer quand même, l'utilisateur peut avoir MongoDB installé différemment
        startBackend();
      });

      mongoProcess.on('close', (code) => {
        console.log('MongoDB démarré (code:', code, ')');
        setTimeout(() => startBackend(), 2000);
      });
    }
  });
}

function startBackend() {
  console.log('Démarrage Backend FastAPI...');
  
  checkPort(8001, (isRunning) => {
    if (isRunning) {
      console.log('Backend déjà en cours d\'exécution');
      createWindow();
    } else {
      const serverPath = path.join(BACKEND_PATH, 'server.py');
      
      backendProcess = spawn(PYTHON_PATH, [
        '-m', 'uvicorn',
        'server:app',
        '--host', '0.0.0.0',
        '--port', '8001'
      ], {
        cwd: BACKEND_PATH,
        shell: true
      });

      backendProcess.stdout.on('data', (data) => {
        console.log(`Backend: ${data}`);
      });

      backendProcess.stderr.on('data', (data) => {
        console.error(`Backend Error: ${data}`);
      });

      backendProcess.on('close', (code) => {
        console.log(`Backend fermé (code: ${code})`);
      });

      // Attendre que le backend soit prêt
      setTimeout(() => {
        checkBackendReady();
      }, 5000);
    }
  });
}

function checkBackendReady() {
  checkPort(8001, (isReady) => {
    if (isReady) {
      console.log('Backend prêt !');
      createWindow();
    } else {
      console.log('Attente du backend...');
      setTimeout(() => checkBackendReady(), 2000);
    }
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    },
    icon: path.join(__dirname, 'logo.jpg'),
    title: 'SMARTSAK10 - Gestion Scolaire IEPP SAKASSOU'
  });

  // Charger l'application React buildée
  mainWindow.loadFile(path.join(FRONTEND_BUILD, 'index.html'));

  // Menu personnalisé
  const menu = Menu.buildFromTemplate([
    {
      label: 'Fichier',
      submenu: [
        {
          label: 'Actualiser',
          accelerator: 'F5',
          click: () => mainWindow.reload()
        },
        { type: 'separator' },
        {
          label: 'Quitter',
          accelerator: 'Alt+F4',
          click: () => app.quit()
        }
      ]
    },
    {
      label: 'Affichage',
      submenu: [
        {
          label: 'Plein écran',
          accelerator: 'F11',
          click: () => mainWindow.setFullScreen(!mainWindow.isFullScreen())
        },
        {
          label: 'Outils de développement',
          accelerator: 'F12',
          click: () => mainWindow.webContents.openDevTools()
        }
      ]
    },
    {
      label: 'Aide',
      submenu: [
        {
          label: 'À propos',
          click: () => {
            const { dialog } = require('electron');
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'À propos de SMARTSAK10',
              message: 'SMARTSAK10\nVersion 1.0.0',
              detail: 'Système de Management Scolaire\nIEPP SAKASSOU\nAnnée Scolaire 2024-2025'
            });
          }
        }
      ]
    }
  ]);

  Menu.setApplicationMenu(menu);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', () => {
  console.log('Application SMARTSAK10 démarrée');
  startMongoDB();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('before-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
  if (frontendProcess) {
    frontendProcess.kill();
  }
});
