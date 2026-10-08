# Comment utiliser le skill `webforms-rules-doc`

Ce skill Claude Code sert à analyser un module ASP.NET WebForms / VB.NET existant et à classer les règles sur trois niveaux, puis à générer :

1. **Backend** — `backend-api-rules.md` pour l'équipe Backend API (génération de l'API).
2. **Frontend** — `frontend-rules.md` pour la génération des interfaces (`swagger-angular-module`).
3. **Technico-fonctionnel** — `technico-fonctionnel.md` (vue transverse), accompagné de `support-validation.md` pour l'équipe Support & Changement.

Il ne modifie pas le code source. Il lit les fichiers `.aspx`, `.ascx`, `.master`, `.vb`, `.config`, `.sql`, `.resx`, `.asmx`, `.ashx`, `.svc` et produit une documentation de règles de gestion.

## 1. Installation

Dézipper le package puis copier le dossier du skill dans le dossier des skills Claude Code.

### Installation personnelle

Linux / macOS / WSL :

```bash
mkdir -p ~/.claude/skills
cp -R webforms-rules-doc ~/.claude/skills/
```

Windows PowerShell :

```powershell
New-Item -ItemType Directory -Force $HOME\.claude\skills
Copy-Item -Recurse .\webforms-rules-doc $HOME\.claude\skills\
```

### Installation dans un projet

A la racine du projet ou du snapshot legacy :

```bash
mkdir -p .claude/skills
cp -R webforms-rules-doc .claude/skills/
```

## 2. Préparer le code IIS

Ne pas travailler directement dans le dossier IIS de production.

Créer une copie lecture seule ou un snapshot :

```text
C:\inetpub\wwwroot\LegacyApp
        -> copie
C:\analysis\LegacyAppSnapshot
```

## 3. Lancer Claude Code

Depuis le dossier de travail :

```bash
cd C:\analysis\LegacyAppSnapshot
claude
```

## 4. Utiliser le skill

Analyser un module complet :

```text
/webforms-rules-doc ./ModuleFacturation
```

Analyser un écran précis :

```text
/webforms-rules-doc ./Pages/Facture.aspx ./Pages/Facture.aspx.vb ./web.config
```

Analyser plusieurs fichiers :

```text
/webforms-rules-doc ./ClientEdit.aspx ./ClientEdit.aspx.vb ./Controls/Adresse.ascx ./web.config
```

## 5. Résultats attendus

Le skill crée un dossier de sortie similaire à :

```text
outputs/webforms-rules-doc/<module>/
├── inventory.md
├── evidence-map.md
├── analysis.json
├── support-validation.md
└── backend-api-rules.md
```

## 6. Rôle des équipes

### Support & Changement

Utilise `support-validation.md` pour valider :

- les règles de gestion actuelles ;
- les règles à corriger ;
- les règles à supprimer ;
- les règles ambiguës à clarifier.

### Backend

Utilise `backend-api-rules.md` pour implémenter :

- validations backend ;
- règles de workflow ;
- calculs ;
- erreurs fonctionnelles ;
- endpoints API ;
- dépendances SQL / configuration.

## 7. Bonnes pratiques

- Toujours analyser une copie du code IIS, jamais directement la production.
- Vérifier les règles `A confirmer` avec Support & Changement avant développement backend.
- Ne pas implémenter une règle backend uniquement à partir d'un candidat automatique.
- Garder les références fichier/ligne dans `evidence-map.md` pour assurer la traçabilité.
- Masquer les secrets avant partage hors équipe technique.

## 8. Image du workflow

Voir : `assets/workflow-usage.png`.
