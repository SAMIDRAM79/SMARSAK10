from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict
from datetime import datetime, date
from enum import Enum

# Enums
class StudentLevel(str, Enum):
    PRE_PRIMAIRE = "pre_primaire"
    MATERNELLE = "maternelle"
    PRIMAIRE = "primaire"

class Gender(str, Enum):
    MASCULIN = "masculin"
    FEMININ = "feminin"

class PaymentStatus(str, Enum):
    PAID = "paid"
    PARTIAL = "partial"
    UNPAID = "unpaid"

class ExamType(str, Enum):
    DEVOIR = "devoir"
    COMPOSITION = "composition"
    EXAMEN_BLANC = "examen_blanc"

# Student Models
class StudentBase(BaseModel):
    matricule: str
    nom: str
    prenoms: str
    date_naissance: date
    lieu_naissance: str
    genre: Gender
    niveau: StudentLevel
    classe: str
    nom_pere: Optional[str] = None
    nom_mere: Optional[str] = None
    telephone_tuteur: str
    adresse: str
    photo_url: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: str
    annee_scolaire: str
    date_inscription: datetime = Field(default_factory=datetime.utcnow)
    statut: str = "actif"

    class Config:
        from_attributes = True

# Class Models
class ClasseBase(BaseModel):
    nom: str
    niveau: StudentLevel
    effectif_max: int = 40
    annee_scolaire: str

class ClasseCreate(ClasseBase):
    pass

class Classe(ClasseBase):
    id: str
    effectif_actuel: int = 0

    class Config:
        from_attributes = True

# Subject Models
class MatiereBase(BaseModel):
    nom: str
    note_sur: int  # 20 ou 50
    niveau: StudentLevel
    coefficient: float = 1.0

class MatiereCreate(MatiereBase):
    pass

class Matiere(MatiereBase):
    id: str

    class Config:
        from_attributes = True

# Note Models
class NoteBase(BaseModel):
    student_id: str
    matiere_id: str
    type_examen: ExamType
    note: float
    note_sur: int
    periode: str  # "trimestre_1", "trimestre_2", "trimestre_3"
    annee_scolaire: str
    observation: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: str
    date_saisie: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

# Bulletin Models
class BulletinBase(BaseModel):
    student_id: str
    classe: str
    periode: str
    annee_scolaire: str
    notes: List[Dict]  # Liste des notes avec matières
    moyenne_generale: float
    rang: Optional[int] = None
    appreciation: Optional[str] = None

class BulletinCreate(BulletinBase):
    pass

class Bulletin(BulletinBase):
    id: str
    date_generation: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

# Teacher Models
class EnseignantBase(BaseModel):
    matricule: str
    nom: str
    prenoms: str
    genre: Gender
    telephone: str
    email: Optional[EmailStr] = None
    specialite: str
    date_embauche: date

class EnseignantCreate(EnseignantBase):
    pass

class Enseignant(EnseignantBase):
    id: str
    statut: str = "actif"

    class Config:
        from_attributes = True

# Fee Models
class FraisBase(BaseModel):
    libelle: str
    montant: float
    niveau: Optional[StudentLevel] = None
    annee_scolaire: str

class FraisCreate(FraisBase):
    pass

class Frais(FraisBase):
    id: str

    class Config:
        from_attributes = True

# Payment Models
class PaiementBase(BaseModel):
    student_id: str
    frais_id: str
    montant_paye: float
    mode_paiement: str  # "especes", "cheque", "virement"
    numero_recu: str

class PaiementCreate(PaiementBase):
    pass

class Paiement(PaiementBase):
    id: str
    date_paiement: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

# Timetable Models
class EmploiDuTempsBase(BaseModel):
    classe: str
    jour: str  # "lundi", "mardi", etc.
    heure_debut: str  # "08:00"
    heure_fin: str  # "10:00"
    matiere: str
    enseignant_id: str
    salle: Optional[str] = None

class EmploiDuTempsCreate(EmploiDuTempsBase):
    pass

class EmploiDuTemps(EmploiDuTempsBase):
    id: str
    annee_scolaire: str

    class Config:
        from_attributes = True

# EPS Card Models
class FicheEPSBase(BaseModel):
    student_id: str
    periode: str
    annee_scolaire: str
    taille: Optional[float] = None  # en cm
    poids: Optional[float] = None  # en kg
    note_eps: Optional[float] = None
    observations: Optional[str] = None

class FicheEPSCreate(FicheEPSBase):
    pass

class FicheEPS(FicheEPSBase):
    id: str
    date_creation: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

# School Card Models
class CarteBase(BaseModel):
    student_id: str
    annee_scolaire: str
    numero_carte: str
    date_emission: date
    date_expiration: date

class CarteCreate(CarteBase):
    pass

class Carte(CarteBase):
    id: str

    class Config:
        from_attributes = True

# Statistics Models
class StatistiquesClasse(BaseModel):
    classe: str
    effectif_total: int
    effectif_garcons: int
    effectif_filles: int
    moyenne_classe: float
    taux_reussite: float

class StatistiquesEcole(BaseModel):
    annee_scolaire: str
    effectif_total: int
    total_pre_primaire: int
    total_maternelle: int
    total_primaire: int
    total_recettes: float
    total_paiements: float
    taux_paiement: float
