from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime, date
from enum import Enum

# Modèles spécifiques pour le CEPE et la répartition

class StatutCandidat(str, Enum):
    OFFICIEL = "officiel"
    LIBRE = "libre"

class Sexe(str, Enum):
    MASCULIN = "M"
    FEMININ = "F"

# Modèle pour l'import Excel AGCEPE
class CandidatImport(BaseModel):
    codedren: str
    codeiep: str
    iep: str
    codeecole: str
    ecole: str
    matricule: str
    nom: str
    prenoms: str
    sexe: str  # M ou F
    jour: int
    mois: int
    annee: int
    nationalite: str
    localite: str
    codesp: str
    sp: str  # sous-préfecture
    pere: Optional[str] = None
    mere: Optional[str] = None
    nacte: Optional[str] = None  # numéro acte naissance
    lieuacte: Optional[str] = None
    residence: Optional[str] = None
    niveau: str  # CM2 pour CEPE
    
class CandidatCEPE(BaseModel):
    """Modèle pour un candidat au CEPE"""
    id: str
    codedren: str
    codeiep: str
    iep: str
    codeecole: str
    ecole: str
    matricule: str
    nom: str
    prenoms: str
    sexe: Sexe
    date_naissance: date
    nationalite: str
    localite: str  # lieu de naissance
    codesp: str
    sp: str
    pere: Optional[str] = None
    mere: Optional[str] = None
    nacte: Optional[str] = None
    lieuacte: Optional[str] = None
    residence: Optional[str] = None
    niveau: str
    statut: StatutCandidat = StatutCandidat.OFFICIEL
    photo_url: Optional[str] = None
    numero_table: Optional[str] = None
    centre_composition: Optional[str] = None
    salle: Optional[int] = None
    annee_scolaire: str
    date_import: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True

class CentreComposition(BaseModel):
    """Centre d'examen"""
    id: str
    nom: str
    capacite_max: int = 480
    nb_salles_fonctionnelles: int = 16
    nb_salles_utilisees: int = 0
    nb_candidats: int = 0
    ecoles_affectees: List[str] = []  # Liste des codes écoles
    annee_scolaire: str
    
    class Config:
        from_attributes = True

class AffectationEcoleCentre(BaseModel):
    """Affectation d'une école à un centre"""
    ecole: str  # code ou nom école
    centre_id: str
    annee_scolaire: str

class SalleRepartition(BaseModel):
    """Détail d'une salle dans la répartition"""
    numero_salle: int
    nb_candidats: int
    candidats: List[str] = []  # Liste des matricules

class RepartitionEcole(BaseModel):
    """Répartition d'une école dans un centre"""
    id: str
    ecole: str
    codeecole: str
    centre_id: str
    centre_nom: str
    nb_candidats_total: int
    nb_salles: int
    salles: List[SalleRepartition]
    annee_scolaire: str
    date_repartition: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True

class ParametresApp(BaseModel):
    """Paramètres globaux de l'application"""
    id: str
    annee_scolaire_actuelle: str  # Ex: "2024-2025"
    session_examen: str  # Ex: "2025"
    drena: str  # Ex: "BOUAKE 2"
    iepp: str  # Ex: "SAKASSOU"
    region: str  # Ex: "GBEKE"
    date_examen: Optional[date] = None
    logo_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class StatistiquesSecteur(BaseModel):
    """Statistiques par secteur"""
    secteur: str
    ecoles_publiques: int = 0
    ecoles_privees: int = 0
    total_ecoles: int = 0
    classes_publiques: int = 0
    classes_privees: int = 0
    total_classes: int = 0
    eleves_publics: int = 0
    eleves_prives: int = 0
    total_eleves: int = 0
    enseignants_publics: int = 0
    enseignants_prives: int = 0
    total_enseignants: int = 0
    conseillers: int = 0
    annee_scolaire: str

class DoublonInfo(BaseModel):
    """Information sur un doublon détecté"""
    matricule: str
    nom: str
    prenoms: str
    occurrences: int
    candidats_ids: List[str]
