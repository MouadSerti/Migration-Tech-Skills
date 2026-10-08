# Contrat du composant code-documentation

## Fichiers concernés

```text
src/app/main/pages/code-documentation/
├── code-documentation.component.ts       # navSections, snippets, données API affichées
├── code-documentation.component.html     # sections de contenu
├── code-documentation.component.scss     # classes CSS
├── README.md                             # résumé de lecture
├── docs/*.md                             # documentation détaillée
├── examples/*                            # exemples copiables
├── schemas/*.json                        # contrats de configuration
└── documentation.angular-style.json      # conventions de style documentaire
```

## Structure du composant TypeScript

### navSections

Tableau `NavSection[]` défini dans la classe. Chaque entrée :

```typescript
{
  id: string;
  label: string;
  icon: string;
  children?: { id: string; label: string }[];
}
```

Règles :
- ajouter une nouvelle entrée à la fin du tableau, avant `];` ;
- garder les IDs en kebab-case ;
- chaque `children[].id` doit correspondre exactement à un `id` HTML ;
- ne pas créer deux entrées pour le même sujet ; mettre à jour l'entrée existante.

### Snippets

Les snippets sont des propriétés `string` de la classe, nommées en camelCase :

```typescript
snippet<NomSujet><Suffixe> = `...`;
```

Règles :
- ajouter les snippets juste avant `scrollToSection()` ;
- utiliser des backticks ;
- ne jamais référencer dans le HTML un snippet absent du TS ;
- garder les snippets courts, copiables et alignés avec les exemples Markdown.

## Structure HTML

### Point d'insertion

Insérer une nouvelle section avant la fin du contenu principal :

```html
      </section>

    </div>
  </main>
</div>
```

### Anatomie d'une section

```html
<section id="<id-section>" class="docs-section">
  <div class="page-header">
    <div class="page-header-badge">Badge</div>
    <h1 class="page-title">Titre</h1>
    <p class="page-lead">Description courte.</p>
  </div>

  <h2 id="<id-section>-overview" class="section-title">
    <mat-icon>info_outline</mat-icon> Vue d'ensemble
  </h2>
</section>
```

### Composants visuels disponibles

#### callout

```html
<div class="callout callout-info">
  <mat-icon>lightbulb</mat-icon>
  <div><strong>Titre :</strong> texte explicatif.</div>
</div>
```

Variantes : `callout-info`, `callout-warning`, `callout-success`, `callout-tip`.

#### props-grid

```html
<div class="props-grid m-t-20">
  <div class="prop-card">
    <mat-icon class="prop-card-icon">folder_copy</mat-icon>
    <div class="prop-card-title">Titre carte</div>
    <div class="prop-card-desc">Description.</div>
  </div>
</div>
```

#### steps

```html
<div class="steps">
  <div class="step">
    <div class="step-num">1</div>
    <div class="step-body">
      <div class="step-title">Titre étape</div>
      <p class="step-desc">Description.</p>
    </div>
  </div>
</div>
```

#### code-block-wrapper

```html
<div class="code-block-wrapper">
  <div class="code-header">
    <span class="code-lang">TypeScript</span>
    <button mat-icon-button class="copy-btn" (click)="copyCode(snippetNom)" matTooltip="Copier">
      <mat-icon>content_copy</mat-icon>
    </button>
  </div>
  <pre class="code-pre"><code>{{ snippetNom }}</code></pre>
</div>
```

#### modules-grid

```html
<div class="modules-grid m-t-20">
  <div class="module-card">
    <div class="module-card-header">
      <mat-icon>description</mat-icon>
      <div>
        <div class="module-name">nom-fichier.md</div>
        <div class="module-path">docs/</div>
      </div>
    </div>
    <p class="module-desc">Description du fichier.</p>
  </div>
</div>
```

#### tableau API

```html
<table class="api-table">
  <thead><tr><th>Col1</th><th>Col2</th></tr></thead>
  <tbody>
    <tr><td><code>valeur</code></td><td>description</td></tr>
  </tbody>
</table>
```

## Règles critiques

1. **Accolades dans le HTML** : `{token}` doit s'écrire `{{ '{' }}token{{ '}' }}` pour éviter `NG5002`.
2. **Apostrophes dans les children TS** : `label: 'Vue d\'ensemble'`.
3. **Classes CSS** : utiliser les classes existantes. Ajouter au SCSS seulement si nécessaire.
4. **IDs uniques** : vérifier qu'aucun `id` existant dans le HTML ne crée un doublon.
5. **Ancres nav ↔ HTML** : chaque child du TS doit pointer vers un `<h2>` ou `<h3>` réel.
6. **Snippets TS ↔ HTML** : chaque `(click)="copyCode(snippetX)"` et `{{ snippetX }}` doit avoir une propriété TS.
7. **Markdown ↔ Angular** : si un concept est changé dans la page Angular, vérifier s'il existe aussi dans `docs/*.md`.
