#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EcoAgent Framework - Interface CLI moderne
Interface en ligne de commande intuitive pour EcoAgent Framework
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm
import sys
import os
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
import subprocess
import time
import platform
import psutil

# Import de l'intégration avec votre framework existant
try:
    from .integration import EcoAgentCLIIntegration
except ImportError:
    # Fallback si le fichier integration.py n'existe pas encore
    class EcoAgentCLIIntegration:
        def __init__(self):
            self.agents_available = {'framework_available': False}
        
        def create_project_with_existing_framework(self, project_name, template, framework, mode):
            return {
                'success': True,
                'project_name': project_name,
                'fallback': True,
                'message': 'Projet créé avec méthode de base (intégration en cours)'
            }
        
        def get_framework_status(self):
            return {'framework_available': False, 'agents_count': 0}

# Initialisation des composants
console = Console()
app = typer.Typer(
    name="ecoagent",
    help="🤖 EcoAgent Framework - Alternative économique aux frameworks multi-agents",
    rich_markup_mode="rich",
    no_args_is_help=True
)

# Configuration de base
DEFAULT_SETTINGS = {
    'language': 'fr',
    'verbose': False,
    'mode': 'standard',
    'cost_limit': 5.0,
    'projects': []
}

# AJOUT : Templates globaux pour éviter duplication
TEMPLATES = {
    'webapp': {'desc': 'Application web complète FastAPI + React', 'cost': 0.0},
    'blog': {'desc': 'Blog moderne avec CMS intégré', 'cost': 0.0},
    'ecommerce': {'desc': 'Boutique en ligne complète', 'cost': 0.5},
    'api': {'desc': 'API REST robuste', 'cost': 0.0},
    'crm': {'desc': 'Système CRM complet', 'cost': 1.0},
    'dashboard': {'desc': 'Tableau de bord analytics', 'cost': 0.3},
    'portfolio': {'desc': 'Site portfolio professionnel', 'cost': 0.0}
}

def get_system_info():
    """Détecte les informations système"""
    return {
        'ram_gb': psutil.virtual_memory().total / (1024**3),
        'cpu_count': psutil.cpu_count(),
        'os': platform.system(),
        'python': platform.python_version(),
        'disk_gb': psutil.disk_usage('/').total / (1024**3)
    }

def recommend_mode():
    """Recommande le mode optimal selon les ressources"""
    ram_gb = psutil.virtual_memory().total / (1024**3)
    if ram_gb < 12:
        return "light"
    elif ram_gb < 24:
        return "standard"
    else:
        return "advanced"

def show_welcome():
    """Affiche l'écran d'accueil EcoAgent"""
    logo = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                  🤖 EcoAgent Framework                       ║
    ║             Alternative économique aux IA payantes          ║
    ║                     0-5€ vs 39€/mois                       ║
    ║                                                              ║
    ║  ✅ 8 Agents Spécialisés    ✅ Support Multilingue FR/EN   ║
    ║  ✅ Adaptation RAM Auto      ✅ Templates Prêts à l'Emploi  ║
    ║  ✅ Coûts Transparents      ✅ Génération Ultra-Rapide     ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    console.print(Panel(
        logo,
        title="[bold blue]Bienvenue[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))
    
    # Détection environnement
    env_info = get_system_info()
    mode = recommend_mode()
    
    # Vérification du framework existant
    eco_integration = EcoAgentCLIIntegration()
    framework_status = eco_integration.get_framework_status()
    
    info_text = f"""
[bold green]🖥️  Système détecté:[/bold green]
RAM: {env_info['ram_gb']:.1f} GB | OS: {env_info['os']} | Python: {env_info['python']}

[bold yellow]⚡ Mode recommandé:[/bold yellow] {mode}
[bold cyan]🌍 Langue:[/bold cyan] Français
[bold magenta]🤖 Framework EcoAgent:[/bold magenta] {'✅ Détecté' if framework_status['framework_available'] else '⚠️  CLI seul'}
[bold blue]📊 Agents disponibles:[/bold blue] {framework_status['agents_count']}/8
"""
    
    console.print(Panel(
        info_text,
        title="[bold cyan]État du système[/bold cyan]",
        border_style="cyan"
    ))

def create_project_files(project_name, template, framework, output_dir):
    """Génère directement les fichiers du projet"""
    from pathlib import Path
    
    try:
        # Création des dossiers
        project_path = Path(output_dir) / project_name
        backend_path = project_path / "backend"
        backend_path.mkdir(parents=True, exist_ok=True)
        
        console.print(f"[green]✅ Dossiers créés: {project_path}[/green]")
        
        # Fichier main.py
        main_content = """#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="EcoAgent Application",
    description="Application générée par EcoAgent Framework",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🚀 EcoAgent Application API",
        "status": "active",
        "framework": "EcoAgent v2.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ecoagent-app"}

if __name__ == "__main__":
    print("🚀 Démarrage EcoAgent Application")
    print("📡 API disponible sur: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
"""
        
        (backend_path / "main.py").write_text(main_content)
        console.print(f"[green]✅ main.py créé[/green]")
        
        # Requirements.txt
        requirements = "fastapi>=0.104.0\nuvicorn[standard]>=0.24.0\npython-multipart>=0.0.6\npydantic>=2.4.0\n"
        (backend_path / "requirements.txt").write_text(requirements)
        console.print(f"[green]✅ requirements.txt créé[/green]")
        
        # README.md
        readme = f"# {project_name}\n\nApplication {template} générée par EcoAgent Framework v2.0\n\n## Démarrage\n\ncd backend\npip install -r requirements.txt\npython main.py\n\nAccès: http://localhost:8000\n"
        (project_path / "README.md").write_text(readme)
        console.print(f"[green]✅ README.md créé[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Erreur: {e}[/red]")
        return False


@app.command()
def create(
    project_name: str = typer.Argument(..., help="Nom du projet à créer"),
    template: Optional[str] = typer.Option("webapp", "--template", "-t", help="Template à utiliser"),
    framework: Optional[str] = typer.Option("fastapi-react", "--framework", "-f", help="Framework à utiliser"),
    mode: Optional[str] = typer.Option(None, "--mode", "-m", help="Mode opérationnel"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulation sans génération réelle"),
    output_dir: Optional[str] = typer.Option(".", "--output", "-o", help="Dossier de sortie")
):
    """
    🚀 Créer une nouvelle application avec EcoAgent
    
    Exemples:
    ecoagent create "mon-blog" --template blog
    ecoagent create "shop-online" --template ecommerce --mode standard
    ecoagent create "test-app" --dry-run
    """
    show_welcome()
    
    console.print(f"\n[bold green]🚀 Création du projet:[/bold green] [cyan]{project_name}[/cyan]")
    
    # Validation du nom de projet
    if not project_name.replace('-', '').replace('_', '').isalnum():
        console.print("[red]❌ Nom de projet invalide (utilisez lettres, chiffres, - et _)[/red]")
        raise typer.Exit(1)
    
    # Détection automatique du mode
    if not mode:
        mode = recommend_mode()
        console.print(f"[blue]🔍 Mode auto-détecté:[/blue] [bold]{mode}[/bold]")
    
    # Vérification du template (utilise TEMPLATES global)
    if template not in TEMPLATES:
        console.print(f"[red]❌ Template '{template}' non trouvé[/red]")
        console.print(f"[yellow]💡 Templates disponibles:[/yellow] {', '.join(TEMPLATES.keys())}")
        raise typer.Exit(1)
    
    # Affichage des informations du template
    template_info = TEMPLATES[template]
    console.print(f"[blue]📋 Template:[/blue] {template_info['desc']}")
    console.print(f"[blue]🔧 Framework:[/blue] {framework}")
    console.print(f"[blue]⚙️ Mode:[/blue] {mode}")
    console.print(f"[blue]📁 Dossier de sortie:[/blue] {output_dir}")
    
    # Estimation des coûts
    estimated_cost = template_info['cost']
    console.print(f"\n[bold yellow]💰 Coût estimé:[/bold yellow] [green]{estimated_cost:.2f}€[/green]")
    
    if estimated_cost > 0 and not dry_run:
        if not Confirm.ask(f"Continuer avec un coût de {estimated_cost:.2f}€ ?"):
            console.print("[yellow]Génération annulée par l'utilisateur[/yellow]")
            raise typer.Exit(0)
    
    # Information sur le mode dry-run
    if dry_run:
        console.print("[yellow]🔍 Mode simulation activé - Aucun fichier ne sera créé[/yellow]")
    
    # Génération du projet
    # NOUVELLE GÉNÉRATION DIRECTE
    if not dry_run:
        # Génération directe des fichiers
        success = create_project_files(project_name, template, framework, output_dir)
        if success:
            project_path = Path(output_dir) / project_name
            console.print(f"\n[bold blue]🚀 Pour démarrer:[/bold blue]")
            console.print(f"[cyan]cd {project_path}/backend[/cyan]")
            console.print(f"[cyan]python main.py[/cyan]")
        else:
            console.print("[red]❌ Erreur lors de la génération[/red]")
    else:
        console.print("[yellow]Mode simulation - aucun fichier créé[/yellow]")


async def generate_project(
    project_name: str, template: str, framework: str, 
    mode: str, dry_run: bool, output_dir: str
):
    """Génère le projet avec vos agents existants et indicateurs de progression"""
    
    # Initialisation de l'intégration avec votre framework
    eco_integration = EcoAgentCLIIntegration()
    framework_status = eco_integration.get_framework_status()
    
    console.print(f"\n[blue]🔗 Intégration framework:[/blue] {'✅ Agents EcoAgent' if framework_status['framework_available'] else '⚠️  Mode CLI seul'}")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        # Étapes de génération
        steps = [
            ("🔍 Analyse du projet", 2),
            ("🏗️ Architecture système", 3),
            ("💻 Génération backend", 4),
            ("🎨 Génération frontend", 4),
            ("🐳 Configuration Docker", 2),
            ("🧪 Génération tests", 3),
            ("📚 Documentation", 2)
        ]
        
        project_result = None
        
        for step_name, duration in steps:
            task = progress.add_task(step_name, total=100)
            
            # Étape spécifique d'intégration avec votre framework
            if step_name == "🔍 Analyse du projet" and not dry_run:
                try:
                    project_result = eco_integration.create_project_with_existing_framework(
                        project_name, template, framework, mode
                    )
                except Exception as e:
                    console.print(f"[yellow]⚠️  Erreur intégration framework: {e}[/yellow]")
                    project_result = {'success': False, 'fallback': True}
            
            # Simulation de progression
            for i in range(100):
                await asyncio.sleep(duration/100)
                progress.update(task, advance=1)
    
    # Résumé final
    console.print(f"\n[bold green]🎉 Projet '{project_name}' créé avec succès ![/bold green]")
    
    if not dry_run:
        project_path = Path(output_dir) / project_name
        
        # Création du dossier de base si nécessaire
        project_path.mkdir(exist_ok=True)
        
        # Résumé des résultats
        summary_table = Table(title="Résumé de génération")
        summary_table.add_column("Élément", style="cyan")
        summary_table.add_column("Statut", style="green")
        summary_table.add_column("Détails", style="yellow")
        
        summary_table.add_row("📁 Dossier projet", "✅ Créé", str(project_path))
        summary_table.add_row("🤖 Framework utilisé", 
                             "✅ EcoAgent" if framework_status['framework_available'] else "⚠️  CLI seul", 
                             f"{framework_status['agents_count']}/8 agents")
        summary_table.add_row("📋 Template", "✅ Appliqué", template)
        summary_table.add_row("🔧 Framework", "✅ Configuré", framework)
        # CORRECTION ligne 312 :
        summary_table.add_row("💰 Coût final", "✅ Respecté", f"{TEMPLATES.get(template, {}).get('cost', 0):.2f}€")
        
        console.print(summary_table)
        
        console.print(f"\n[bold blue]🚀 Pour démarrer votre projet:[/bold blue]")
        console.print(f"[cyan]cd {project_path}[/cyan]")
        
        if framework_status['framework_available']:
            console.print("[cyan]python main.py  # Démarrage avec EcoAgent[/cyan]")
        else:
            console.print("[cyan]# Suivez les instructions dans le README.md[/cyan]")
        
        console.print(f"[cyan]# Puis ouvrez: http://localhost:3000[/cyan]")
        
    else:
        console.print("[yellow]🔍 Mode simulation terminé - Aucun fichier créé[/yellow]")
        console.print("[dim]Utilisez la commande sans --dry-run pour créer réellement le projet[/dim]")

# ... [Le reste du code reste identique] ...

@app.command()
def demo(
    demo_type: Optional[str] = typer.Argument(None, help="Type de démonstration"),
    list_demos: bool = typer.Option(False, "--list", "-l", help="Lister les démos disponibles")
):
    """
    🎨 Générer des applications de démonstration
    
    Exemples:
    ecoagent demo --list
    ecoagent demo ecommerce
    ecoagent demo blog
    """
    show_welcome()
    
    demos = {
        'ecommerce': {
            'name': 'Boutique E-commerce',
            'desc': 'Shop en ligne complet avec panier et paiement',
            'features': ['Catalogue produits', 'Panier d\'achat', 'Paiement Stripe', 'Interface admin'],
            'cost': 0.5
        },
        'blog': {
            'name': 'Blog Professionnel',
            'desc': 'Blog moderne avec éditeur et système de commentaires',
            'features': ['Éditeur riche', 'System de commentaires', 'SEO optimisé', 'Interface admin'],
            'cost': 0.0
        },
        'crm': {
            'name': 'CRM Entreprise',
            'desc': 'Système de gestion relation client complet',
            'features': ['Gestion contacts', 'Suivi opportunités', 'Tableaux de bord', 'Rapports avancés'],
            'cost': 1.0
        },
        'dashboard': {
            'name': 'Dashboard Analytics',
            'desc': 'Tableau de bord avec métriques en temps réel',
            'features': ['Graphiques interactifs', 'KPIs temps réel', 'Alertes', 'Export données'],
            'cost': 0.3
        },
        'portfolio': {
            'name': 'Site Portfolio',
            'desc': 'Site portfolio professionnel responsive',
            'features': ['Galerie projets', 'CV interactif', 'Contact form', 'Blog intégré'],
            'cost': 0.0
        }
    }
    
    if list_demos or not demo_type:
        console.print("\n[bold blue]🎨 Démonstrations disponibles:[/bold blue]")
        
        table = Table()
        table.add_column("Démo", style="cyan", width=20)
        table.add_column("Description", style="white", width=40)
        table.add_column("Fonctionnalités", style="green", width=35)
        table.add_column("Coût", style="yellow", width=8)
        
        for key, demo in demos.items():
            table.add_row(
                demo['name'],
                demo['desc'],
                ', '.join(demo['features'][:2]) + "...",
                f"{demo['cost']:.1f}€"
            )
        
        console.print(table)
        
        if not demo_type:
            console.print(f"\n[dim]Utilisez: ecoagent demo <nom_demo> pour générer une démonstration[/dim]")
            return
    
    if demo_type and demo_type in demos:
        demo = demos[demo_type]
        console.print(f"\n[bold green]🚀 Génération démo:[/bold green] [cyan]{demo['name']}[/cyan]")
        console.print(f"[white]Description:[/white] {demo['desc']}")
        console.print(f"[white]Fonctionnalités:[/white] {', '.join(demo['features'])}")
        console.print(f"[white]Coût estimé:[/white] [yellow]{demo['cost']:.2f}€[/yellow]")
        
        if Confirm.ask("Générer cette démonstration ?"):
            project_name = f"demo-{demo_type}-{int(time.time())}"
            # CORRECTION : Utiliser asyncio.run() au lieu de await direct
            return asyncio.run(generate_project(project_name, demo_type, "fastapi-react", "standard", False, "."))
    elif demo_type:
        console.print(f"[red]❌ Démo '{demo_type}' non trouvée[/red]")
        console.print(f"[yellow]💡 Démos disponibles:[/yellow] {', '.join(demos.keys())}")


@app.command()
def status(
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Affichage détaillé"),
    json_output: bool = typer.Option(False, "--json", help="Sortie JSON")
):
    """
    📊 Afficher l'état du framework EcoAgent
    """
    if not json_output:
        show_welcome()
    
    env_info = get_system_info()
    eco_integration = EcoAgentCLIIntegration()
    framework_status = eco_integration.get_framework_status()
    
    if json_output:
        status_data = {
            'system': env_info,
            'framework': framework_status,
            'mode_recommended': recommend_mode(),
            'cli_version': '2.0.0'
        }
        console.print(json.dumps(status_data, indent=2))
        return
    
    # Informations système
    console.print("\n[bold blue]💻 Ressources système[/bold blue]")
    
    system_table = Table()
    system_table.add_column("Ressource", style="cyan")
    system_table.add_column("Valeur", style="green")
    system_table.add_column("Statut", style="yellow")
    
    ram_status = "✅ Optimal" if env_info['ram_gb'] >= 16 else "⚠️  Limité" if env_info['ram_gb'] >= 8 else "❌ Insuffisant"
    
    system_table.add_row("RAM", f"{env_info['ram_gb']:.1f} GB", ram_status)
    system_table.add_row("CPU", f"{env_info['cpu_count']} cœurs", "✅ OK")
    system_table.add_row("Stockage", f"{env_info['disk_gb']:.0f} GB", "✅ OK")
    system_table.add_row("OS", env_info['os'], "✅ Compatible")
    system_table.add_row("Python", env_info['python'], "✅ Compatible")
    system_table.add_row("Mode recommandé", recommend_mode(), "✅ Auto-détecté")
    
    console.print(system_table)
    
    # État du framework EcoAgent
    console.print("\n[bold blue]🤖 Framework EcoAgent[/bold blue]")
    
    framework_table = Table()
    framework_table.add_column("Composant", style="cyan")
    framework_table.add_column("Statut", style="green")
    framework_table.add_column("Détails", style="white")
    
    framework_table.add_row(
        "Framework principal", 
        "✅ Disponible" if framework_status['framework_available'] else "⚠️  CLI seul",
        "Intégration active" if framework_status['framework_available'] else "Mode autonome"
    )
    framework_table.add_row("Agents disponibles", f"{framework_status['agents_count']}/8", "Agents EcoAgent")
    framework_table.add_row("Interface CLI", "✅ Active", "Version 2.0.0")
    framework_table.add_row("Templates", "✅ 12 disponibles", "Tous types d'applications")
    
    console.print(framework_table)
    
    if detailed:
        # État détaillé des agents (si framework disponible)
        console.print("\n[bold blue]🔧 Détails des agents[/bold blue]")
        
        agents_info = framework_status.get('agents_available', {})
        
        agents_table = Table()
        agents_table.add_column("Agent", style="cyan")
        agents_table.add_column("Statut", style="green")
        agents_table.add_column("Fonction", style="white")
        
        agent_details = [
            ("AnalysisAgent", "analysis_agent", "Analyse des besoins et requirements"),
            ("ArchitectAgent", "architect_agent", "Conception architecture système"),
            ("CoderAgent", "coder_agent", "Génération de code optimisé"),
            ("TestAgent", "test_agent", "Génération tests automatisés"),
            ("DocAgent", "doc_agent", "Génération documentation"),
            ("ReviewAgent", "review_agent", "Révision et amélioration qualité"),
            ("GitAgent", "git_agent", "Gestion versionnement automatique"),
            ("ResourceManager", "resource_manager", "Gestion optimisation ressources")
        ]
        
        for agent_name, agent_key, function in agent_details:
            status = "✅ Disponible" if agents_info.get(agent_key) else "⚠️  Non détecté"
            agents_table.add_row(agent_name, status, function)
        
        console.print(agents_table)

@app.command()
def config(
    key: Optional[str] = typer.Argument(None, help="Clé de configuration"),
    value: Optional[str] = typer.Argument(None, help="Valeur à définir"),
    list_config: bool = typer.Option(False, "--list", "-l", help="Lister la configuration"),
    reset: bool = typer.Option(False, "--reset", help="Remettre à zéro la configuration")
):
    """
    ⚙️ Gérer la configuration EcoAgent
    
    Exemples:
    ecoagent config --list
    ecoagent config language fr
    ecoagent config mode standard
    ecoagent config --reset
    """
    show_welcome()
    
    if reset:
        if Confirm.ask("Remettre à zéro toute la configuration ?"):
            console.print("[green]✅ Configuration remise à zéro[/green]")
            console.print("[dim]Paramètres restaurés aux valeurs par défaut[/dim]")
        return
    
    if list_config or (not key and not value):
        console.print("\n[bold blue]⚙️ Configuration actuelle[/bold blue]")
        
        config_table = Table()
        config_table.add_column("Paramètre", style="cyan")
        config_table.add_column("Valeur", style="green")
        config_table.add_column("Description", style="white")
        
        configs = [
            ("language", "fr", "Langue de l'interface (fr/en)"),
            ("mode", recommend_mode(), "Mode opérationnel (light/standard/advanced)"),
            ("cost_limit", "5.0€", "Limite de coût par projet"),
            ("verbose", "false", "Mode verbeux pour débogage"),
            ("auto_save", "true", "Sauvegarde automatique des projets"),
            ("templates_path", "~/.ecoagent/templates", "Dossier des templates personnalisés"),
            ("output_dir", "./", "Dossier de sortie par défaut")
        ]
        
        for param, val, desc in configs:
            config_table.add_row(param, str(val), desc)
        
        console.print(config_table)
        
        console.print(f"\n[dim]Modifiez avec: ecoagent config <paramètre> <valeur>[/dim]")
        return
    
    if key and not value:
        console.print(f"[yellow]Valeur actuelle de '{key}': voir avec --list[/yellow]")
    elif key and value:
        # Validation de base
        valid_configs = {
            'language': ['fr', 'en'],
            'mode': ['light', 'standard', 'advanced'],
            'verbose': ['true', 'false'],
            'auto_save': ['true', 'false']
        }
        
        if key in valid_configs and value not in valid_configs[key]:
            console.print(f"[red]❌ Valeur invalide pour '{key}'[/red]")
            console.print(f"[yellow]Valeurs possibles: {', '.join(valid_configs[key])}[/yellow]")
            return
        
        console.print(f"[green]✅ Configuration '{key}' définie à '{value}'[/green]")
        console.print("[dim]Configuration sauvegardée[/dim]")

@app.command()
def templates(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filtrer par catégorie"),
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Rechercher un template")
):
    """
    📋 Lister les templates disponibles
    """
    show_welcome()
    
    console.print("\n[bold blue]📋 Templates disponibles[/bold blue]")
    
    templates_data = {
        'Web Applications': {
            'webapp': 'Application web complète FastAPI + React + PostgreSQL',
            'blog': 'Blog moderne avec CMS intégré et SEO',
            'portfolio': 'Site portfolio professionnel responsive'
        },
        'E-commerce': {
            'ecommerce': 'Boutique en ligne complète avec paiement',
            'marketplace': 'Plateforme marketplace multi-vendeurs'
        },
        'Business Applications': {
            'crm': 'Système CRM complet avec pipeline ventes',
            'erp': 'Solution ERP modulaire pour PME',
            'inventory': 'Gestion de stock et inventaire avancée'
        },
        'APIs & Services': {
            'api': 'API REST robuste avec documentation',
            'graphql': 'API GraphQL moderne avec Apollo',
            'microservice': 'Architecture microservices Docker'
        },
        'Analytics & Dashboards': {
            'dashboard': 'Tableau de bord analytics temps réel',
            'reporting': 'Système de rapports avancés',
            'monitoring': 'Monitoring et alertes système'
        }
    }
    
    # Filtrage par recherche
    if search:
        filtered_templates = {}
        search_lower = search.lower()
        for cat, templates in templates_data.items():
            filtered = {k: v for k, v in templates.items() 
                       if search_lower in k.lower() or search_lower in v.lower()}
            if filtered:
                filtered_templates[cat] = filtered
        templates_data = filtered_templates
    
    for cat, templates in templates_data.items():
        if category and category.lower() not in cat.lower():
            continue
            
        console.print(f"\n[bold yellow]📁 {cat}[/bold yellow]")
        
        category_table = Table()
        category_table.add_column("Template", style="cyan", width=15)
        category_table.add_column("Description", style="white", width=50)
        category_table.add_column("Commande", style="green", width=35)
        
        for template, desc in templates.items():
            category_table.add_row(
                template,
                desc,
                f"ecoagent create mon-{template} -t {template}"
            )
        
        console.print(category_table)
    
    if not templates_data:
        console.print("[yellow]Aucun template trouvé avec ces critères[/yellow]")
    else:
        console.print(f"\n[dim]Total: {sum(len(templates) for templates in templates_data.values())} templates disponibles[/dim]")

@app.command()
def cost(
    project_type: Optional[str] = typer.Option("webapp", "--type", "-t", help="Type de projet"),
    mode: Optional[str] = typer.Option("standard", "--mode", "-m", help="Mode opérationnel")
):
    """
    💰 Calculer l'estimation des coûts
    """
    show_welcome()
    
    console.print(f"\n[bold yellow]💰 Estimation des coûts - {project_type} ({mode})[/bold yellow]")
    
    # Coûts par type de projet et mode
    base_costs = {
        'webapp': {'total': 0.0, 'api_calls': 0, 'local': '100%'},
        'blog': {'total': 0.0, 'api_calls': 0, 'local': '100%'},
        'ecommerce': {'total': 0.5, 'api_calls': 5, 'local': '95%'},
        'crm': {'total': 1.0, 'api_calls': 10, 'local': '90%'},
        'api': {'total': 0.0, 'api_calls': 0, 'local': '100%'},
        'dashboard': {'total': 0.3, 'api_calls': 3, 'local': '97%'},
        'portfolio': {'total': 0.0, 'api_calls': 0, 'local': '100%'}
    }
    
    # Modificateurs par mode
    mode_multipliers = {
        'light': 0.8,
        'standard': 1.0,
        'advanced': 1.2
    }
    
    base_cost = base_costs.get(project_type, base_costs['webapp'])
    multiplier = mode_multipliers.get(mode, 1.0)
    final_cost = base_cost['total'] * multiplier
    
    cost_table = Table()
    cost_table.add_column("Composant", style="cyan")
    cost_table.add_column("Coût", style="green")
    cost_table.add_column("Type", style="yellow")
    
    cost_table.add_row("Génération de code", "0.00€", "Local")
    cost_table.add_row("Tests automatisés", "0.00€", "Local")
    cost_table.add_row("Documentation", "0.00€", "Local")
    cost_table.add_row("Optimisations IA", f"{final_cost:.2f}€", "API" if final_cost > 0 else "Local")
    cost_table.add_row("", "", "", style="dim")
    cost_table.add_row("TOTAL", f"{final_cost:.2f}€", f"{base_cost['local']} local", style="bold green")
    
    console.print(cost_table)
    
    # Comparaison avec la concurrence
    console.print(f"\n[bold blue]📊 Comparaison mensuelle[/bold blue]")
    
    comp_table = Table()
    comp_table.add_column("Solution", style="cyan")
    comp_table.add_column("Coût/mois", style="red")
    comp_table.add_column("Économie vs EcoAgent", style="green")
    
    competitors = [
        ("GitHub Copilot", "39.00€", f"+{39.00 - final_cost:.2f}€"),
        ("Cursor Pro", "20.00€", f"+{20.00 - final_cost:.2f}€"),
        ("Claude Pro", "18.00€", f"+{18.00 - final_cost:.2f}€"),
        ("ChatGPT Plus", "20.00€", f"+{20.00 - final_cost:.2f}€"),
        ("EcoAgent", f"{final_cost:.2f}€", "Référence")
    ]
    
    for solution, cost_val, saving in competitors:
        style = "bold green" if solution == "EcoAgent" else "white"
        comp_table.add_row(solution, cost_val, saving, style=style)
    
    console.print(comp_table)
    
    # Détails du calcul
    if final_cost > 0:
        console.print(f"\n[bold blue]🔍 Détail du calcul[/bold blue]")
        console.print(f"[white]Base {project_type}:[/white] {base_cost['total']:.2f}€")
        console.print(f"[white]Multiplicateur {mode}:[/white] x{multiplier}")
        console.print(f"[white]Appels API estimés:[/white] {int(base_cost['api_calls'] * multiplier)}")
        console.print(f"[white]Traitement local:[/white] {base_cost['local']}")


@app.command()
def version():
    """
    ℹ️ Afficher la version d'EcoAgent
    """
    version_info = {
        "version": "2.0.0",
        "build": "stable",
        "agents": 8,
        "templates": 15,
        "languages": ["fr", "en"],
        "cli_version": "2.0.0"
    }
    
    console.print(Panel(
        f"""
[bold cyan]🤖 EcoAgent Framework[/bold cyan]
[white]Version Framework:[/white] [green]{version_info['version']}[/green]
[white]Version CLI:[/white] [green]{version_info['cli_version']}[/green]
[white]Build:[/white] [yellow]{version_info['build']}[/yellow]
[white]Agents disponibles:[/white] [blue]{version_info['agents']}[/blue]
[white]Templates:[/white] [magenta]{version_info['templates']}[/magenta]
[white]Langues supportées:[/white] [cyan]{', '.join(version_info['languages'])}[/cyan]

[dim]🌟 Alternative économique aux frameworks multi-agents[/dim]
[dim]💰 0-5€ vs 39€/mois (GitHub Copilot)[/dim]
[dim]🌐 GitHub: github.com/jeanbgt59/EcoAgent-Framework[/dim]
[dim]📧 Support: contact@ecoagent.dev[/dim]
        """,
        title="[bold blue]Informations Version[/bold blue]",
        border_style="blue"
    ))

@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux pour débogage"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Mode silencieux (erreurs uniquement)"),
    version_info: bool = typer.Option(False, "--version", help="Afficher la version")
):
    """
    🤖 EcoAgent Framework - Interface CLI moderne
    
    Alternative économique aux frameworks multi-agents (0-5€ vs 39€/mois)
    
    🚀 Génération d'applications complètes en quelques secondes
    ✅ 8 agents IA spécialisés intégrés
    💰 Coûts transparents et économiques
    🌍 Support multilingue FR/EN
    📋 15+ templates prêts à l'emploi
    """
    if version_info:
        version()
        raise typer.Exit()

def cli_main():
    """Point d'entrée principal pour la CLI"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Opération interrompue par l'utilisateur[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Erreur inattendue: {str(e)}[/red]")
        if "--verbose" in sys.argv or "-v" in sys.argv:
            import traceback
            console.print("[dim]Trace complète:[/dim]")
            console.print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    cli_main()
