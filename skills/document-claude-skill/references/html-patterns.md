# Patterns HTML de la page code-documentation

Utiliser ces patterns pour ajouter ou mettre à jour des sections dans `code-documentation.component.html`.

## Séparateur de section

```html
      <!-- ╔══════════════════════════════════════════════════════╗
           ║  TITRE DE SECTION                                   ║
           ╚══════════════════════════════════════════════════════╝ -->
      <section id="<id-section>" class="docs-section">
```

## Bloc page-header

```html
<div class="page-header">
  <div class="page-header-badge">Badge</div>
  <h1 class="page-title">Titre</h1>
  <p class="page-lead">
    Description courte : ce que le développeur doit comprendre avant d'utiliser cette partie.
  </p>
</div>
```

## Vue d'ensemble avec cartes

```html
<h2 id="<id>-overview" class="section-title">
  <mat-icon>info_outline</mat-icon> Vue d'ensemble
</h2>

<div class="callout callout-info">
  <mat-icon>lightbulb</mat-icon>
  <div>
    <strong>À retenir :</strong> résumé concret du comportement réel du projet.
  </div>
</div>

<div class="props-grid m-t-20">
  <div class="prop-card">
    <mat-icon class="prop-card-icon">account_tree</mat-icon>
    <div class="prop-card-title">Structure</div>
    <div class="prop-card-desc">Ce qui a changé dans l'organisation des fichiers.</div>
  </div>
  <div class="prop-card">
    <mat-icon class="prop-card-icon">code</mat-icon>
    <div class="prop-card-title">Code</div>
    <div class="prop-card-desc">API publique, types, services ou composants impactés.</div>
  </div>
  <div class="prop-card">
    <mat-icon class="prop-card-icon">schema</mat-icon>
    <div class="prop-card-title">Conception</div>
    <div class="prop-card-desc">Pattern ou responsabilité modifiée.</div>
  </div>
  <div class="prop-card">
    <mat-icon class="prop-card-icon">rule</mat-icon>
    <div class="prop-card-title">Standardisation</div>
    <div class="prop-card-desc">Convention ou règle à appliquer désormais.</div>
  </div>
</div>
```

## Bloc snippet copiables

```html
<div class="code-block-wrapper">
  <div class="code-header">
    <span class="code-lang">Shell</span>
    <button mat-icon-button class="copy-btn" (click)="copyCode(snippetNom)" matTooltip="Copier">
      <mat-icon>content_copy</mat-icon>
    </button>
  </div>
  <pre class="code-pre"><code>{{ snippetNom }}</code></pre>
</div>
```

## Workflow numéroté

```html
<h2 id="<id>-workflow" class="section-title m-t-40">
  <mat-icon>account_tree</mat-icon> Workflow
</h2>

<div class="steps">
  <div class="step">
    <div class="step-num">1</div>
    <div class="step-body">
      <div class="step-title">Détecter</div>
      <p class="step-desc">Identifier les fichiers changés et leur impact documentaire.</p>
    </div>
  </div>
</div>
```

## Tableau de paramètres ou de contrat

```html
<table class="api-table m-t-20">
  <thead>
    <tr><th>Élément</th><th>Type</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><code>columns</code></td>
      <td><code>ColumnConfig[]</code></td>
      <td>Colonnes utilisées par la table, les filtres et les formulaires.</td>
    </tr>
  </tbody>
</table>
```

## Grille de fichiers documentation

```html
<div class="modules-grid m-t-20">
  <div class="module-card">
    <div class="module-card-header">
      <mat-icon>description</mat-icon>
      <div>
        <div class="module-name">10-best-practices.md</div>
        <div class="module-path">docs/</div>
      </div>
    </div>
    <p class="module-desc">Conventions et règles d'équipe à maintenir après les changements.</p>
  </div>

  <div class="module-card module-special">
    <div class="module-card-header">
      <mat-icon>terminal</mat-icon>
      <div>
        <div class="module-name">project_change_inventory.py</div>
        <div class="module-path">scripts/</div>
      </div>
    </div>
    <p class="module-desc">Génère l'inventaire des fichiers modifiés et les classe par impact documentaire.</p>
  </div>
</div>
```

## Callout résumé final

```html
<div class="callout callout-success m-t-30">
  <mat-icon>task_alt</mat-icon>
  <div>
    <strong>Documentation synchronisée :</strong>
    le code, les exemples, les schémas et la page Angular décrivent maintenant le même comportement.
  </div>
</div>
```

## Pattern section skill ciblé

```html
<h2 id="<id>-usage" class="section-title m-t-40">
  <mat-icon>terminal</mat-icon> Invocation
</h2>

<p>Taper dans Claude Code :</p>

<div class="code-block-wrapper">
  <div class="code-header">
    <span class="code-lang">Cas minimal</span>
    <button mat-icon-button class="copy-btn" (click)="copyCode(snippetSkillInvoke)" matTooltip="Copier">
      <mat-icon>content_copy</mat-icon>
    </button>
  </div>
  <pre class="code-pre"><code>{{ snippetSkillInvoke }}</code></pre>
</div>
```
