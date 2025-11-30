const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const waitOn = require('wait-on');

let mainWindow;
let backendProcess;
let frontendProcess;

const isDev = process.env.NODE_ENV === 'development';
const BACKEND_PORT = 8001;
const FRONTEND_PORT = 3000;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
    icon: path.join(__dirname, 'icon.png'),
    title: 'SMARTSAK10 - Gestion Scolaire',
    autoHideMenuBar: false,
  });

  // Créer un menu personnalisé
  const menu = Menu.buildFromTemplate([
    {
      label: 'Fichier',
      submenu: [
        {
          label: 'Actualiser',
          accelerator: 'F5',
          click: () => mainWindow.reload()
        },
        {
          label: 'Quitter',
          accelerator: 'Alt+F4',
          click: () => app.quit()
        }
      ]
    },
    {
      label: 'Aide',
      submenu: [
        {
          label: 'À propos',
          click: () => {
            const aboutWindow = new BrowserWindow({
              width: 400,
              height: 300,
              parent: mainWindow,
              modal: true,
              title: 'À propos de SMARTSAK10'
            });
            aboutWindow.loadURL(`data:text/html;charset=utf-8,
              <html>
                <body style="font-family: Arial; padding: 20px; text-align: center;">
                  <h1>SMARTSAK10</h1>
                  <p>Version 1.0.0</p>
                  <p>Système de gestion scolaire complet</p>
                  <p>Pré-primaire, Maternelle, Primaire</p>
                  <br>
                  <p>© 2024 SMARTSAK10</p>
                </body>
              </html>
            `);
          }
        }
      ]
    }
  ]);
  Menu.setApplicationMenu(menu);

  // Charger l'application
  if (isDev) {
    mainWindow.loadURL(`http://localhost:${FRONTEND_PORT}`);
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadURL(`http://localhost:${FRONTEND_PORT}`);
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startBackend() {
  return new Promise((resolve, reject) => {
    console.log('Démarrage du backend...');
    
    const backendPath = path.join(__dirname, '..', 'backend');
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
    
    backendProcess = spawn(pythonCmd, [
      '-m', 'uvicorn',
      'server:app',
      '--host', '127.0.0.1',
      '--port', BACKEND_PORT.toString(),
      '--workers', '1'
    ], {
      cwd: backendPath,
      env: { ...process.env }
    });

    backendProcess.stdout.on('data', (data) => {
      console.log(`Backend: ${data}`);
    });

    backendProcess.stderr.on('data', (data) => {
      console.error(`Backend Error: ${data}`);
    });

    backendProcess.on('error', (error) => {
      console.error('Erreur backend:', error);
      reject(error);
    });

    // Attendre que le backend soit prêt
    waitOn({
      resources: [`http://localhost:${BACKEND_PORT}/api/`],
      timeout: 30000,
      interval: 500
    }).then(() => {
      console.log('✓ Backend démarré');
      resolve();
    }).catch((err) => {
      console.error('Timeout backend:', err);
      reject(err);
    });
  });
}

function startFrontend() {
  return new Promise((resolve, reject) => {
    console.log('Démarrage du frontend...');
    
    const frontendPath = path.join(__dirname, '..', 'frontend');
    const yarnCmd = process.platform === 'win32' ? 'yarn.cmd' : 'yarn';
    
    frontendProcess = spawn(yarnCmd, ['start'], {
      cwd: frontendPath,
      env: { ...process.env, BROWSER: 'none', CI: 'true' },
      shell: true
    });

    frontendProcess.stdout.on('data', (data) => {
      console.log(`Frontend: ${data}`);
      if (data.includes('webpack compiled successfully') || data.includes('Compiled successfully')) {
        resolve();
      }
    });

    frontendProcess.stderr.on('data', (data) => {
      console.log(`Frontend Info: ${data}`);
    });

    frontendProcess.on('error', (error) => {
      console.error('Erreur frontend:', error);
      reject(error);
    });

    // Timeout de secours
    setTimeout(() => {
      console.log('✓ Frontend démarré (timeout)');
      resolve();
    }, 45000);
  });
}

async function initializeApp() {
  try {
    console.log('Initialisation de SMARTSAK10...');
    
    // Démarrer le backend
    await startBackend();
    
    // Démarrer le frontend
    await startFrontend();
    
    // Attendre que le frontend soit vraiment prêt
    await waitOn({
      resources: [`http://localhost:${FRONTEND_PORT}`],
      timeout: 60000,
      interval: 1000
    });
    
    console.log('✓ Application prête, ouverture de la fenêtre...');
    
    // Créer la fenêtre
    createWindow();
    
  } catch (error) {
    console.error('Erreur lors de l\'initialisation:', error);
    app.quit();
  }
}

app.on('ready', () => {
  initializeApp();
});

app.on('window-all-closed', () => {
  // Tuer les processus
  if (backendProcess) {
    backendProcess.kill();
  }
  if (frontendProcess) {
    frontendProcess.kill();
  }
  app.quit();
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// Gérer la fermeture propre
process.on('SIGTERM', () => {
  if (backendProcess) backendProcess.kill();
  if (frontendProcess) frontendProcess.kill();
  app.quit();
});
