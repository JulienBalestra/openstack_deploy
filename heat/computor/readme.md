# Computor Application

## Objectif

Déployer au sein d'une plateforme OpenStack une application à l'aide des fonctionnalités proposées par le catalogue OpenStack.

## Développement

Il s'agit d'une application Python capable de résoudre des équations polynomiales de degré 1 et 2.

L'application **open-source** réalisée dans le cadre de l'école informatique 42 possède son propre dépot public github : [computor](https://github.com/JulienBalestra/computor)

Initialement déployée sur le PaaS Elastic Beanstalk d'Amazon Web Services, le répertoire sysadmin permet de réaliser un *quick install & launch*

Cette application utilise le framework Flask.
Elle possède un cycle d'intégration continue sous Travis et Codeship avec près de 200 tests (unitaires et fonctionnels).



## Intégration

Un template heat générique est situé sur le dépot public github suivant : [openstack_deploy](https://github.com/JulienBalestra/openstack_deploy/tree/master/heat/computor)


Ce template est composé de plusieurs types de ressources :

### Racine heat

[computor](https://github.com/JulienBalestra/openstack_deploy/blob/master/heat/computor/computor.yaml)

#### Réseau

    * réseau (Neutron::Net)
    * sous réseau (Neutron::Subnet)
    * routeur avec gateway sur le réseau public (Neutron::Router)
    * interface sur le sous réseau (Neutron::RouterInterface)

#### Sécurité

    * Groupe de sécurité pour les bastions (Neutron::SecurityGroup)
    * Groupe de sécurité pour l'application (Neutron::SecurityGroup)
    
#### Résilience

    * Groupe d'anti-affinité pour les bastions (Nova::ServerGroup)
    * Groupe d'anti-affinité pour l'application (Nova::ServerGroup)
    * Groupe de plusieurs instances de type bastion (Heat::ResourceGroup)
    * Groupe de passage à l'échelle pour l'application (Heat::AutoScalingGroup)
    
#### Elasticité

    * Répartiteur de charge avec adresse IP publique (Neutron::LoadBalancer, Neutron::FloatingIP)
    * Procédure de répartition de charge (Neutron::Pool)
    * Point d'accès +1 au nombre d'instances applicative (Heat::ScalingPolicy)
    * Point d'accès -1 au nombre d'instances applicative (Heat::ScalingPolicy)
    
#### Gestion de configuration

    * Procédure d'installation de l'application (Heat::CloudConfig)
    * Procédure d'installation des bastions (Heat::CloudConfig)
    
### Nested Stack Bastion

[bastion_instance](https://github.com/Julienalestra/openstack_deploy/blob/master/heat/computor/bastion_instance.yaml)


#### Réseau

    * Une interface réseau connectée sur le sous-réseau créé (Neutron::Port)
    * Une adresse IP publique reliée sur le port créé ci-dessus (Neutron::FloatingIP)
    
### Nested Stack Application

[computor_instance](https://github.com/JulienBalestra/openstack_deploy/blob/master/heat/computor/computor_instance.yaml)


#### Réseau

    * Une interface réseau connectée sur le sous-réseau créé (Neutron::Port)
    * Membre du répartiteur de charge (Neutron::PoolMember)



