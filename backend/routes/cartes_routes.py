from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from database import get_db
from auth_middleware import verify_email
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from io import BytesIO
from PIL import Image
import os
from pathlib import Path

router = APIRouter(prefix="/cartes", tags=["cartes"])

# Couleurs des modèles - COULEURS VIVES
MODELES_COULEURS = {
    "standard": {
        "fond": "#FFFFFF",
        "bordure": "#0066CC",  # Bleu vif
        "titre": "#0066CC",
        "texte": "#1A1A1A",
        "accent": "#00CC66"  # Vert vif
    },
    "logo_blanc": {
        "fond": "#FFFFFF",
        "bordure": "#9C27B0",  # Violet vif
        "titre": "#6A1B9A",
        "texte": "#2C2C2C",
        "accent": "#AB47BC"
    },
    "logo_couleur": {
        "fond": "#FFF9C4",  # Jaune clair vif
        "bordure": "#FF6F00",  # Orange vif
        "titre": "#E65100",
        "texte": "#BF360C",
        "accent": "#FFB300"
    },
    "drapeau_ivoirien": {
        "fond": "#FFFFFF",
        "bordure_gauche": "#00A86B",  # Vert émeraude vif
        "bordure_droite": "#FF8C00",  # Orange vif
        "titre": "#1A5E1A",
        "texte": "#2C2C2C",
        "accent": "#FFFFFF"
    }
}

def dessiner_carte(c, x, y, largeur, hauteur, candidat, modele, logo_path=None):
    """Dessiner une carte scolaire individuelle"""
    couleurs = MODELES_COULEURS.get(modele, MODELES_COULEURS["standard"])
    
    # Fond de la carte
    c.setFillColor(HexColor(couleurs["fond"]))
    c.rect(x, y, largeur, hauteur, fill=1, stroke=0)
    
    # Bordure spéciale pour le modèle drapeau ivoirien
    if modele == "drapeau_ivoirien":
        # Bande verte à gauche
        c.setFillColor(HexColor(couleurs["bordure_gauche"]))
        c.rect(x, y, 5*mm, hauteur, fill=1, stroke=0)
        # Bande orange à droite
        c.setFillColor(HexColor(couleurs["bordure_droite"]))
        c.rect(x + largeur - 5*mm, y, 5*mm, hauteur, fill=1, stroke=0)
        # Bordure principale
        c.setStrokeColor(HexColor(couleurs["titre"]))
    else:
        c.setStrokeColor(HexColor(couleurs["bordure"]))
    
    c.setLineWidth(1.5)
    c.rect(x, y, largeur, hauteur, fill=0, stroke=1)
    
    # Logo en filigrane pour certains modèles
    if modele in ["logo_blanc", "logo_couleur"] and logo_path and os.path.exists(logo_path):
        try:
            # Dessiner le logo en filigrane au centre
            logo_size = 30*mm
            logo_x = x + (largeur - logo_size) / 2
            logo_y = y + (hauteur - logo_size) / 2
            c.saveState()
            c.setFillAlpha(0.1)  # Très transparent
            c.drawImage(logo_path, logo_x, logo_y, width=logo_size, height=logo_size, mask='auto')
            c.restoreState()
        except:
            pass
    
    # En-tête avec logo petit
    if logo_path and os.path.exists(logo_path):
        try:
            logo_size = 12*mm
            c.drawImage(logo_path, x + 5*mm, y + hauteur - 15*mm, width=logo_size, height=logo_size, mask='auto')
        except:
            pass
    
    # Titre
    c.setFillColor(HexColor(couleurs["titre"]))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x + largeur/2, y + hauteur - 8*mm, "CARTE SCOLAIRE")
    
    # Année scolaire
    c.setFont("Helvetica", 7)
    c.setFillColor(HexColor(couleurs["texte"]))
    c.drawCentredString(x + largeur/2, y + hauteur - 12*mm, candidat.get("annee_scolaire", "2024-2025"))
    
    # Photo du candidat (si disponible)
    photo_url = candidat.get("photo_url")
    if photo_url:
        photo_path = f"/app/backend{photo_url}"
        if os.path.exists(photo_path):
            try:
                photo_size = 20*mm
                photo_x = x + (largeur - photo_size) / 2
                photo_y = y + hauteur - 40*mm
                c.drawImage(photo_path, photo_x, photo_y, width=photo_size, height=photo_size, mask='auto')
            except:
                pass
    
    # Informations du candidat
    y_pos = y + hauteur - 45*mm
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(HexColor(couleurs["texte"]))
    
    # Matricule
    c.drawString(x + 5*mm, y_pos, "Matricule:")
    c.setFont("Helvetica", 8)
    c.drawString(x + 25*mm, y_pos, candidat.get("matricule", ""))
    
    # Nom
    y_pos -= 5*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 5*mm, y_pos, "Nom:")
    c.setFont("Helvetica", 8)
    nom = candidat.get("nom", "")[:20]  # Limiter la longueur
    c.drawString(x + 25*mm, y_pos, nom)
    
    # Prénoms
    y_pos -= 5*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 5*mm, y_pos, "Prénoms:")
    c.setFont("Helvetica", 8)
    prenoms = candidat.get("prenoms", "")[:18]
    c.drawString(x + 25*mm, y_pos, prenoms)
    
    # Date de naissance
    y_pos -= 5*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 5*mm, y_pos, "Né(e) le:")
    c.setFont("Helvetica", 8)
    date_naiss = candidat.get("date_naissance", "")
    c.drawString(x + 25*mm, y_pos, date_naiss)
    
    # École
    y_pos -= 5*mm
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x + 5*mm, y_pos, "École:")
    c.setFont("Helvetica", 7)
    ecole = candidat.get("ecole", "")[:25]
    c.drawString(x + 20*mm, y_pos, ecole)
    
    # Niveau
    y_pos -= 5*mm
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x + 5*mm, y_pos, "Niveau:")
    c.setFont("Helvetica", 7)
    c.drawString(x + 20*mm, y_pos, candidat.get("niveau", "CM2"))
    
    # Emplacement pour émargement directeur
    y_pos = y + 8*mm
    c.setFont("Helvetica", 6)
    c.setFillColor(HexColor(couleurs["texte"]))
    c.drawCentredString(x + largeur/2, y_pos, "Émargement Directeur")
    c.setStrokeColor(HexColor(couleurs["bordure"]))
    c.setLineWidth(0.5)
    c.line(x + 10*mm, y_pos - 3*mm, x + largeur - 10*mm, y_pos - 3*mm)

@router.post("/generer")
async def generer_cartes_pdf(
    ecole: str,
    modele: str = "standard",
    annee_scolaire: str = None,
    email: str = Depends(verify_email)
):
    """Générer un PDF avec 8 cartes scolaires par page A4"""
    db = get_db()
    
    # Récupérer les candidats de l'école
    query = {"ecole": ecole}
    if annee_scolaire:
        query["annee_scolaire"] = annee_scolaire
    
    candidats = await db.candidats_cepe.find(query, {"_id": 0}).sort("nom", 1).to_list(10000)
    
    if not candidats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun candidat trouvé pour cette école"
        )
    
    # Créer le PDF en mémoire
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Dimensions des cartes (8 par page: 2 colonnes x 4 lignes)
    marge = 10*mm
    espace_entre = 5*mm
    largeur_carte = (width - 2*marge - espace_entre) / 2
    hauteur_carte = (height - 2*marge - 3*espace_entre) / 4
    
    # Chemin du logo
    logo_path = "/app/frontend/public/logo-iepp.jpg"
    
    # Générer les cartes
    for i, candidat in enumerate(candidats):
        # Calculer la position sur la page
        page_index = i // 8
        carte_index = i % 8
        
        # Nouvelle page si nécessaire
        if carte_index == 0 and i > 0:
            c.showPage()
        
        # Position de la carte (ligne, colonne)
        ligne = carte_index // 2
        colonne = carte_index % 2
        
        x = marge + colonne * (largeur_carte + espace_entre)
        y = height - marge - (ligne + 1) * hauteur_carte - ligne * espace_entre
        
        # Dessiner la carte
        dessiner_carte(c, x, y, largeur_carte, hauteur_carte, candidat, modele, logo_path)
    
    # Finaliser le PDF
    c.save()
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=cartes_{ecole}_{modele}.pdf"
        }
    )
