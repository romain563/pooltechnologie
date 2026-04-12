# PoolTechnologie — Intégration Home Assistant

Intégration personnalisée Home Assistant pour les électrolyseurs et régulateurs de piscine **Pool Technologie**, via communication **Modbus TCP**.

---

## Prérequis matériel

L'électrolyseur Pool Technologie communique en **Modbus RTU** (RS-485). Pour l'intégrer à Home Assistant, une **passerelle Modbus RTU → TCP** est nécessaire.

**Exemple de passerelle compatible :** [Waveshare RS485/RS232 to Ethernet](https://www.amazon.fr/Waveshare-RS232-485-Ethernet-Industrial/dp/B0CGDXCHXV)

Branchez la passerelle entre le port RS-485 de votre électrolyseur et votre réseau local. Configurez-la en mode **Modbus TCP server** avec les paramètres série correspondant à votre appareil (baudrate, parité, stop bits).

---

## Fonctionnalités

### Capteurs (lecture)

| Entité | Description | Unité |
|---|---|---|
| pH | Mesure du pH de l'eau | — |
| Température de l'eau | Température de l'eau du bassin | °C |
| ORP | Potentiel redox | mV |
| Salinité | Taux de sel | g/L |
| Tension cellule | Tension aux bornes de la cellule d'électrolyse *(diagnostic)* | mV |

### Réglages (lecture / écriture)

| Entité | Description | Plage |
|---|---|---|
| Consigne pH | Valeur cible du pH | 6.8 – 7.6 |
| Consigne électrolyse | Puissance d'électrolyse | 10 – 100 % |
| Concentration correcteur de pH | Concentration du produit pH | 5 – 50 % |
| Volume du bassin | Volume du bassin en m³ | — |
| Consigne ORP *(optionnel)* | Valeur cible ORP si sonde présente | 400 – 900 mV |

### Interrupteurs

| Entité | Description |
|---|---|
| Régulation pH automatique | Active / désactive la régulation automatique du pH |

### Diagnostic

| Entité | Description |
|---|---|
| Connexion Modbus | État de la communication avec l'appareil (ON / OFF) |

---

## Installation

### Via HACS (recommandé)

1. Dans HACS, cliquez sur **Intégrations** → menu ⋮ → **Dépôts personnalisés**
2. Ajoutez l'URL `https://github.com/Romain563/pooltechnologie` avec la catégorie **Intégration**
3. Recherchez **PoolTechnologie** et installez
4. Redémarrez Home Assistant

### Installation manuelle

1. Copiez le dossier `pooltechnologie` dans votre répertoire `custom_components` :
   ```
   config/custom_components/pooltechnologie/
   ```
2. Redémarrez Home Assistant

---

## Configuration

1. Allez dans **Paramètres → Appareils et services → Ajouter une intégration**
2. Recherchez **PoolTechnologie**
3. Renseignez les paramètres :

| Champ | Description | Valeur par défaut |
|---|---|---|
| Nom de l'appareil | Nom affiché dans HA | PoolTechnologie |
| Adresse IP | IP de la passerelle Modbus | 192.168.0.100 |
| Port Modbus | Port TCP de la passerelle | 502 |
| ID de l'unité Modbus | Unit ID Modbus de l'appareil | 1 |
| Intervalle de rafraîchissement | Fréquence de lecture en secondes | 60 |
| Régulation avec sonde ORP | Cocher si une sonde ORP est installée | Non |

### Option après installation

L'activation/désactivation de la **régulation ORP** peut être modifiée à tout moment via **Paramètres → Appareils et services → PoolTechnologie → Configurer**. L'intégration se recharge automatiquement après modification.

---

## Compatibilité

- **Home Assistant** : 2024.4 ou supérieur
- **Python** : 3.11 ou supérieur
- **pymodbus** : 3.9.2 ou supérieur

---

## Dépannage

**Les entités sont indisponibles au démarrage**
Vérifiez que la passerelle Modbus est joignable sur le réseau et que l'adresse IP et le port sont corrects.

**Le capteur "Connexion Modbus" est OFF**
L'électrolyseur ne répond pas aux requêtes Modbus. Vérifiez le câblage RS-485 et les paramètres série de la passerelle.

**Erreur `transaction_id` dans les logs**
Certaines passerelles Modbus ne respectent pas strictement le protocole TCP. Cette erreur est généralement non bloquante.

