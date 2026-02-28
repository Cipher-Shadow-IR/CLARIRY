# build_app.ps1

Write-Host "Installing PyInstaller..."
pip install Pyinstaller

Write-Host "Building CLARIRY Universe Teacher..."

# We need to include 'public' folder and 'study_engine' modules if they are not picked up.
# PyInstaller command:
# --noconfirm: replace output directory without asking
# --onedir: create a one-folder bundle (often safer than onefile for many assets)
# --windowed: do not provide a console window for a standard GUI app
# --icon: set the icon
# --add-data: include data files

Pyinstaller --noconfirm `
    --onefile `
    --windowed `
    --name "CLARIRY" `
    --icon "public\assets\CLARIRY_LOGO.ico" `
    --add-data "public;public" `
    --add-data "study_engine;study_engine" `
    --add-data "ui;ui" `
    --hidden-import "study_engine" `
    --hidden-import "study_engine.explainer" `
    --hidden-import "study_engine.explainer.ai_explainer" `
    --hidden-import "study_engine.explainer.prompt_templates" `
    --hidden-import "study_engine.gui_player" `
    --hidden-import "study_engine.paragraph_store" `
    --hidden-import "study_engine.persistence" `
    --hidden-import "study_engine.persistence.progress_store" `
    --hidden-import "study_engine.state_manager" `
    --hidden-import "google.generativeai" `
    --hidden-import "fitz" `
    main.py

Write-Host "Build complete! Check the 'dist' folder."
